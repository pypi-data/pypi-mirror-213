import pathlib
import unittest

from altcos import ostree


class TestStream(unittest.TestCase):
    SR = "<some-path>" # STREAMS_ROOT
    VALID_STREAM = ostree.Stream.from_ostree_ref(SR, "altcos/x86_64/sisyphus")
    VALID_SUBSTREAM = ostree.Stream.from_ostree_ref(SR, "altcos/x86_64/Sisyphus/k8s")

    def test_like_ostree_ref(self):
        good = "altcos/x86_64/sisyphus"
        self.assertEqual(good, self.VALID_STREAM.like_ostree_ref())

    def test_like_ostree_ref_for_subref(self):
        good = "altcos/x86_64/Sisyphus/k8s"
        self.assertEqual(good, self.VALID_SUBSTREAM.like_ostree_ref())

    def test_valid_stream_init_from_ref(self):
        ref = "altcos/x86_64/sisyphus"
        try:
            ostree.Stream.from_ostree_ref(self.SR, ref)
        except ValueError as e:
            self.fail(e)

    def test_valid_stream_init_from_subref(self):
        ref = "altcos/x86_64/Sisyphus/k8s"
        try:
            ostree.Stream.from_ostree_ref(self.SR, ref)
        except ValueError as e:
            self.fail(e)

    def test_invalid_stream_init_from_ref(self):
        ref = "altcos/x86_4/branch"
        try:
            ostree.Stream.from_ostree_ref(self.SR, ref)
        except ValueError:
            pass

    def test_invalid_stream_init_from_subref(self):
        ref = "altcos/x86_65/Lol/k8s"
        try:
            ostree.Stream.from_ostree_ref(self.SR, ref)
        except ValueError:
            pass

    def test_stream_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64")
        self.assertEqual(good, self.VALID_STREAM.stream_dir)

    def test_stream_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s")
        self.assertEqual(good, self.VALID_SUBSTREAM.stream_dir)

    def test_rootfs_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/rootfs")
        self.assertEqual(good, self.VALID_STREAM.rootfs_dir)

    def test_rootfs_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/rootfs")
        self.assertEqual(good, self.VALID_SUBSTREAM.rootfs_dir)

    def test_ostree_bare_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/ostree/bare")
        self.assertEqual(good, self.VALID_STREAM.ostree_bare_dir)

    def test_ostree_bare_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/ostree/bare")
        self.assertEqual(good, self.VALID_SUBSTREAM.ostree_bare_dir)

    def test_ostree_archive_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/ostree/archive")
        self.assertEqual(good, self.VALID_STREAM.ostree_archive_dir)

    def test_ostree_archive_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/ostree/archive")
        self.assertEqual(good, self.VALID_SUBSTREAM.ostree_archive_dir)

    def test_vars_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/vars")
        self.assertEqual(good, self.VALID_STREAM.vars_dir)

    def test_vars_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/vars")
        self.assertEqual(good, self.VALID_SUBSTREAM.vars_dir)

    def test_work_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/work")
        self.assertEqual(good, self.VALID_STREAM.work_dir)

    def test_work_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/work")
        self.assertEqual(good, self.VALID_SUBSTREAM.work_dir)

    def test_merged_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/work/merged")
        self.assertEqual(good, self.VALID_STREAM.merged_dir)

    def test_merged_dir_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/work/merged")
        self.assertEqual(good, self.VALID_SUBSTREAM.merged_dir)


class TestVersion(unittest.TestCase):
    def test_valid_version_init_from_str(self):
        try:
            ostree.Version.from_str("sisyphus_base.20230101.1.0")
        except ValueError as e:
            self.fail(e)

    def test_str(self):
        good = "20230101.1.0"
        version = ostree.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, str(version))

    def test_full_version(self):
        good = "sisyphus_base.20230101.1.0"
        version = ostree.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, version.full_version)

    def test_full_version_for_subref(self):
        good = "sisyphus_k8s.20230101.1.0"
        version = ostree.Version.from_str("sisyphus_k8s.20230101.1.0")
        self.assertEqual(good, version.full_version)

    def test_like_path(self):
        good = pathlib.Path("20230101/1/0")
        version = ostree.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, version.like_path)


if __name__ == "__main__":
    unittest.main()
