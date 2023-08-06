import os
import shutil
import subprocess
import unittest

import pytest

from ...constants import *  # NOQA
from .. import changedir
from . import (
    ArchiverTestCaseBase,
    RemoteArchiverTestCaseBase,
    ArchiverTestCaseBinaryBase,
    RK_ENCRYPTION,
    requires_hardlinks,
    BORG_EXES,
)


def have_gnutar():
    if not shutil.which("tar"):
        return False
    popen = subprocess.Popen(["tar", "--version"], stdout=subprocess.PIPE)
    stdout, stderr = popen.communicate()
    return b"GNU tar" in stdout


class ArchiverTestCase(ArchiverTestCaseBase):
    requires_gnutar = pytest.mark.skipif(not have_gnutar(), reason="GNU tar must be installed for this test.")
    requires_gzip = pytest.mark.skipif(not shutil.which("gzip"), reason="gzip must be installed for this test.")

    @requires_gnutar
    def test_export_tar(self):
        self.create_test_files()
        os.unlink("input/flagfile")
        self.cmd(f"--repo={self.repository_location}", "rcreate", RK_ENCRYPTION)
        self.cmd(f"--repo={self.repository_location}", "create", "test", "input")
        self.cmd(
            f"--repo={self.repository_location}", "export-tar", "test", "simple.tar", "--progress", "--tar-format=GNU"
        )
        with changedir("output"):
            # This probably assumes GNU tar. Note -p switch to extract permissions regardless of umask.
            subprocess.check_call(["tar", "xpf", "../simple.tar", "--warning=no-timestamp"])
        self.assert_dirs_equal("input", "output/input", ignore_flags=True, ignore_xattrs=True, ignore_ns=True)

    @requires_gnutar
    @requires_gzip
    def test_export_tar_gz(self):
        if not shutil.which("gzip"):
            pytest.skip("gzip is not installed")
        self.create_test_files()
        os.unlink("input/flagfile")
        self.cmd(f"--repo={self.repository_location}", "rcreate", RK_ENCRYPTION)
        self.cmd(f"--repo={self.repository_location}", "create", "test", "input")
        list = self.cmd(
            f"--repo={self.repository_location}", "export-tar", "test", "simple.tar.gz", "--list", "--tar-format=GNU"
        )
        assert "input/file1\n" in list
        assert "input/dir2\n" in list
        with changedir("output"):
            subprocess.check_call(["tar", "xpf", "../simple.tar.gz", "--warning=no-timestamp"])
        self.assert_dirs_equal("input", "output/input", ignore_flags=True, ignore_xattrs=True, ignore_ns=True)

    @requires_gnutar
    def test_export_tar_strip_components(self):
        if not shutil.which("gzip"):
            pytest.skip("gzip is not installed")
        self.create_test_files()
        os.unlink("input/flagfile")
        self.cmd(f"--repo={self.repository_location}", "rcreate", RK_ENCRYPTION)
        self.cmd(f"--repo={self.repository_location}", "create", "test", "input")
        list = self.cmd(
            f"--repo={self.repository_location}",
            "export-tar",
            "test",
            "simple.tar",
            "--strip-components=1",
            "--list",
            "--tar-format=GNU",
        )
        # --list's path are those before processing with --strip-components
        assert "input/file1\n" in list
        assert "input/dir2\n" in list
        with changedir("output"):
            subprocess.check_call(["tar", "xpf", "../simple.tar", "--warning=no-timestamp"])
        self.assert_dirs_equal("input", "output/", ignore_flags=True, ignore_xattrs=True, ignore_ns=True)

    @requires_hardlinks
    @requires_gnutar
    def test_export_tar_strip_components_links(self):
        self._extract_hardlinks_setup()
        self.cmd(
            f"--repo={self.repository_location}",
            "export-tar",
            "test",
            "output.tar",
            "--strip-components=2",
            "--tar-format=GNU",
        )
        with changedir("output"):
            subprocess.check_call(["tar", "xpf", "../output.tar", "--warning=no-timestamp"])
            assert os.stat("hardlink").st_nlink == 2
            assert os.stat("subdir/hardlink").st_nlink == 2
            assert os.stat("aaaa").st_nlink == 2
            assert os.stat("source2").st_nlink == 2

    @requires_hardlinks
    @requires_gnutar
    def test_extract_hardlinks_tar(self):
        self._extract_hardlinks_setup()
        self.cmd(
            f"--repo={self.repository_location}", "export-tar", "test", "output.tar", "input/dir1", "--tar-format=GNU"
        )
        with changedir("output"):
            subprocess.check_call(["tar", "xpf", "../output.tar", "--warning=no-timestamp"])
            assert os.stat("input/dir1/hardlink").st_nlink == 2
            assert os.stat("input/dir1/subdir/hardlink").st_nlink == 2
            assert os.stat("input/dir1/aaaa").st_nlink == 2
            assert os.stat("input/dir1/source2").st_nlink == 2

    def test_import_tar(self, tar_format="PAX"):
        self.create_test_files(create_hardlinks=False)  # hardlinks become separate files
        os.unlink("input/flagfile")
        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "create", "src", "input")
        self.cmd(f"--repo={self.repository_location}", "export-tar", "src", "simple.tar", f"--tar-format={tar_format}")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", "simple.tar")
        with changedir(self.output_path):
            self.cmd(f"--repo={self.repository_location}", "extract", "dst")
        self.assert_dirs_equal("input", "output/input", ignore_ns=True, ignore_xattrs=True)

    def test_import_unusual_tar(self):
        # Contains these, unusual entries:
        # /foobar
        # ./bar
        # ./foo2/
        # ./foo//bar
        # ./
        tar_archive = os.path.join(os.path.dirname(__file__), "unusual_paths.tar")

        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", tar_archive)
        files = self.cmd(f"--repo={self.repository_location}", "list", "dst", "--format", "{path}{NL}").splitlines()
        self.assert_equal(set(files), {"foobar", "bar", "foo2", "foo/bar", "."})

    def test_import_tar_with_dotdot(self):
        # Contains this file:
        # ../../../../etc/shadow
        tar_archive = os.path.join(os.path.dirname(__file__), "dotdot_path.tar")

        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        with pytest.raises(ValueError, match="unexpected '..' element in path '../../../../etc/shadow'"):
            self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", tar_archive, exit_code=2)

    @requires_gzip
    def test_import_tar_gz(self, tar_format="GNU"):
        if not shutil.which("gzip"):
            pytest.skip("gzip is not installed")
        self.create_test_files(create_hardlinks=False)  # hardlinks become separate files
        os.unlink("input/flagfile")
        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "create", "src", "input")
        self.cmd(f"--repo={self.repository_location}", "export-tar", "src", "simple.tgz", f"--tar-format={tar_format}")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", "simple.tgz")
        with changedir(self.output_path):
            self.cmd(f"--repo={self.repository_location}", "extract", "dst")
        self.assert_dirs_equal("input", "output/input", ignore_ns=True, ignore_xattrs=True)

    @requires_gnutar
    def test_import_concatenated_tar_with_ignore_zeros(self):
        self.create_test_files(create_hardlinks=False)  # hardlinks become separate files
        os.unlink("input/flagfile")
        with changedir("input"):
            subprocess.check_call(["tar", "cf", "file1.tar", "file1"])
            subprocess.check_call(["tar", "cf", "the_rest.tar", "--exclude", "file1*", "."])
            with open("concatenated.tar", "wb") as concatenated:
                with open("file1.tar", "rb") as file1:
                    concatenated.write(file1.read())
                # Clean up for assert_dirs_equal.
                os.unlink("file1.tar")

                with open("the_rest.tar", "rb") as the_rest:
                    concatenated.write(the_rest.read())
                # Clean up for assert_dirs_equal.
                os.unlink("the_rest.tar")

        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "--ignore-zeros", "dst", "input/concatenated.tar")
        # Clean up for assert_dirs_equal.
        os.unlink("input/concatenated.tar")

        with changedir(self.output_path):
            self.cmd(f"--repo={self.repository_location}", "extract", "dst")
        self.assert_dirs_equal("input", "output", ignore_ns=True, ignore_xattrs=True)

    @requires_gnutar
    def test_import_concatenated_tar_without_ignore_zeros(self):
        self.create_test_files(create_hardlinks=False)  # hardlinks become separate files
        os.unlink("input/flagfile")
        with changedir("input"):
            subprocess.check_call(["tar", "cf", "file1.tar", "file1"])
            subprocess.check_call(["tar", "cf", "the_rest.tar", "--exclude", "file1*", "."])
            with open("concatenated.tar", "wb") as concatenated:
                with open("file1.tar", "rb") as file1:
                    concatenated.write(file1.read())
                with open("the_rest.tar", "rb") as the_rest:
                    concatenated.write(the_rest.read())
                os.unlink("the_rest.tar")

        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", "input/concatenated.tar")

        with changedir(self.output_path):
            self.cmd(f"--repo={self.repository_location}", "extract", "dst")

        # Negative test -- assert that only file1 has been extracted, and the_rest has been ignored
        # due to zero-filled block marker.
        self.assert_equal(os.listdir("output"), ["file1"])

    def test_roundtrip_pax_borg(self):
        self.create_test_files()
        self.cmd(f"--repo={self.repository_location}", "rcreate", "--encryption=none")
        self.cmd(f"--repo={self.repository_location}", "create", "src", "input")
        self.cmd(f"--repo={self.repository_location}", "export-tar", "src", "simple.tar", "--tar-format=BORG")
        self.cmd(f"--repo={self.repository_location}", "import-tar", "dst", "simple.tar")
        with changedir(self.output_path):
            self.cmd(f"--repo={self.repository_location}", "extract", "dst")
        self.assert_dirs_equal("input", "output/input")


class RemoteArchiverTestCase(RemoteArchiverTestCaseBase, ArchiverTestCase):
    """run the same tests, but with a remote repository"""


@unittest.skipUnless("binary" in BORG_EXES, "no borg.exe available")
class ArchiverTestCaseBinary(ArchiverTestCaseBinaryBase, ArchiverTestCase):
    """runs the same tests, but via the borg binary"""

    @unittest.skip("does not work with binaries")
    def test_import_tar_with_dotdot(self):
        # the test checks for a raised exception. that can't work if the code runs in a separate process.
        pass
