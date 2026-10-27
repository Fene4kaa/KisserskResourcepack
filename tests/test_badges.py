"""Badge updater regressions: raw preservation, replacement and reproducibility."""
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "update_badges", ROOT / "scripts" / "update_badges.py"
)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


class BadgeArchiveTests(unittest.TestCase):
    def test_update_preserves_original_local_bytes_and_metadata(self):
        # Recompressing old entries or normalizing ZipInfo would lose these bytes.
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "pack.zip"
            info = zipfile.ZipInfo("pack.mcmeta", (2024, 2, 3, 4, 5, 6))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100640 << 16
            info.extra = b"\xfe\xca\x02\x00ok"
            info.comment = b"entry comment"
            with zipfile.ZipFile(archive, "w", compresslevel=1) as output:
                output.comment = b"archive comment"
                output.writestr(info, b'{"pack":{"min_format":[88,0]}}')
            original = archive.read_bytes()
            with zipfile.ZipFile(io.BytesIO(original)) as source:
                start = source.start_dir
                metadata = source.getinfo("pack.mcmeta")
                before = {key: getattr(metadata, key) for key in metadata.__slots__}
            UPDATER.update_archive(archive, ROOT)
            updated = archive.read_bytes()
            self.assertEqual(original[:start], updated[:start])
            with zipfile.ZipFile(archive) as result:
                self.assertEqual(b"archive comment", result.comment)
                self.assertEqual(b'{"pack":{"min_format":[88,0]}}', result.read("pack.mcmeta"))
                actual = result.getinfo("pack.mcmeta")
                self.assertEqual(before, {key: getattr(actual, key) for key in actual.__slots__})
                self.assertEqual(6, len(result.infolist()))
                self.assertEqual(
                    (ROOT / "assets/kissersk/font/badges.json").read_bytes(),
                    result.read("assets/kissersk/font/badges.json"),
                )

    def test_repeat_update_is_byte_identical_and_changed_badge_replaces_old_entry(self):
        # Appending duplicate names or keeping obsolete local records breaks this.
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            archive = base / "pack.zip"
            sources = base / "sources"
            for name in UPDATER.MANAGED_PATHS:
                target = sources / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / name).read_bytes())
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("pack.mcmeta", b"original")
            UPDATER.update_archive(archive, sources)
            first = archive.read_bytes()
            UPDATER.update_archive(archive, sources)
            self.assertEqual(first, archive.read_bytes())
            miner = sources / "assets/kissersk/textures/font/badges/miner.png"
            replacement = (ROOT / "assets/kissersk/textures/font/badges/mage.png").read_bytes()
            miner.write_bytes(replacement)
            UPDATER.update_archive(archive, sources)
            with zipfile.ZipFile(archive) as result:
                self.assertEqual(6, len(result.infolist()))
                self.assertEqual(replacement, result.read("assets/kissersk/textures/font/badges/miner.png"))
                self.assertEqual(b"original", result.read("pack.mcmeta"))
            changed = archive.read_bytes()
            UPDATER.update_archive(archive, sources)
            self.assertEqual(changed, archive.read_bytes())


if __name__ == "__main__":
    unittest.main()
