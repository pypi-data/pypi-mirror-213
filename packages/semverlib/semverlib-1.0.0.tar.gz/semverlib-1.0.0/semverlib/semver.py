from dataclasses import dataclass
from functools import total_ordering
from typing import Self, Optional
from re import compile, ASCII, MULTILINE

PARSER_RE = compile(
    "^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    ASCII | MULTILINE,
)


@dataclass(frozen=True)
@total_ordering
class SemVer:
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None
    build: Optional[str] = None

    @classmethod
    def parse(cls, semver_string: str) -> Self:
        match = PARSER_RE.match(semver_string)
        if not match:
            raise SemverException(f"wrong SemVer formar: {semver_string!r}")
        return cls(
            int(match.group("major")),
            int(match.group("minor")),
            int(match.group("patch")),
            match.group("prerelease"),
            match.group("buildmetadata"),
        )

    def __str__(self) -> str:
        string = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            string += f"-{self.pre_release}"
        if self.build:
            string += f"-{self.build}"
        return string

    def __lt__(self, other: Self) -> bool:
        if self.major < other.major:
            return True
        if self.major > other.major:
            return False
        if self.minor < other.minor:
            return True
        if self.minor > other.minor:
            return False
        if self.patch < other.patch:
            return True
        if self.patch > other.patch:
            return False
        if self.pre_release == other.pre_release:
            return False
        if self.pre_release and not other.pre_release:
            return True
        pre_self = self.pre_release.split(".") if self.pre_release else []
        pre_other = other.pre_release.split(".") if other.pre_release else []
        for i in range(min(len(pre_self), len(pre_other))):
            pre_self_part = pre_self[i]
            pre_other_part = pre_other[i]
            if pre_self_part == pre_other_part:
                continue
            try:
                return int(pre_self_part) < int(pre_other_part)
            except ValueError:
                pass
            if pre_self_part < pre_other_part:
                return True
            else:
                return False
        if len(pre_self) < len(pre_other):
            return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.pre_release == other.pre_release
        )

    def next_major(self) -> Self:
        return self.__class__(self.major + 1, 0, 0)

    def next_minor(self) -> Self:
        return self.__class__(self.major, self.minor + 1, 0)

    def next_patch(self) -> Self:
        return self.__class__(self.major, self.minor, self.patch + 1)


class SemverException(Exception):
    pass
