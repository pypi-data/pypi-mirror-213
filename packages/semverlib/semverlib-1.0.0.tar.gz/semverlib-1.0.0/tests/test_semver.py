from unittest import TestCase
from semverlib import SemVer, SemverException

# Based on https://semver.org/spec/v2.0.0.html


class TestParse(TestCase):
    def test_simple(self):
        self.assertSemVer(SemVer.parse("1.2.3"), 1, 2, 3)

    def test_extensions(self):
        self.assertSemVer(
            SemVer.parse("1.2.3-alpha.1+99ef51a"), 1, 2, 3, "alpha.1", "99ef51a"
        )
        self.assertSemVer(SemVer.parse("1.2.3-alpha.0"), 1, 2, 3, "alpha.0")
        self.assertSemVer(SemVer.parse("1.2.3+99ef51a"), 1, 2, 3, build="99ef51a")

    def test_wrong_format(self):
        with self.assertRaises(SemverException):
            SemVer.parse("1.2")
        with self.assertRaises(SemverException):
            SemVer.parse("-1.2.3")
        with self.assertRaises(SemverException):
            SemVer.parse("1.2.-3")

    def assertSemVer(
        self,
        version: SemVer,
        major: int,
        minor: int,
        patch: int,
        pre_release: str = None,
        build: str = None,
    ) -> None:
        self.assertEqual(version.major, major)
        self.assertEqual(version.minor, minor)
        self.assertEqual(version.patch, patch)
        self.assertEqual(version.pre_release, pre_release)
        self.assertEqual(version.build, build)


class TestPrecedence(TestCase):
    def test_equality(self):
        self.assertEqual(SemVer(1, 2, 3, "a"), SemVer(1, 2, 3, "a", "x"))
        self.assertNotEqual(SemVer(1, 2, 3), SemVer(1, 0, 3))

    def test_order(self):
        self.assertLess(SemVer(1, 0, 0), SemVer(2, 0, 0))
        self.assertLess(SemVer(2, 0, 0), SemVer(2, 1, 0))
        self.assertLess(SemVer(2, 1, 0), SemVer(2, 1, 1))
        self.assertLess(SemVer(1, 0, 0, "alpha"), SemVer(1, 0, 0))
        self.assertLess(SemVer(1, 0, 0, "alpha"), SemVer(1, 0, 0, "alpha.1"))
        self.assertLess(SemVer(1, 0, 0, "alpha.1"), SemVer(1, 0, 0, "alpha.beta"))
        self.assertLess(SemVer(1, 0, 0, "alpha.beta"), SemVer(1, 0, 0, "beta"))
        self.assertLess(SemVer(1, 0, 0, "beta"), SemVer(1, 0, 0, "beta.2"))
        self.assertLess(SemVer(1, 0, 0, "beta.2"), SemVer(1, 0, 0, "beta.11"))
        self.assertLess(SemVer(1, 0, 0, "beta.11"), SemVer(1, 0, 0, "rc.1"))
        self.assertLess(SemVer(1, 0, 0, "rc.1"), SemVer(1, 0, 0))


class TestIncrement(TestCase):
    def test_increments(self):
        base = SemVer(1, 2, 3, "alpha.0", "99ef51a")
        self.assertEqual(base.next_major(), SemVer(2, 0, 0))
        self.assertEqual(base.next_minor(), SemVer(1, 3, 0))
        self.assertEqual(base.next_patch(), SemVer(1, 2, 4))
