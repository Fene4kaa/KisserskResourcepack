"""Update only the five badge entries without recompressing any existing assets.

Run with Python 3: python -B scripts/update_badges.py
The source font and PNG files under assets/ are authoritative. Repeated runs
with identical sources produce identical ZIP bytes. This handles the repository's
single-disk, non-ZIP64 archive; managed badge entries remain an appended suffix.
"""
import argparse
import hashlib
import io
from pathlib import Path
import struct
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MANAGED_PATHS = (
    "assets/kissersk/font/badges.json",
    "assets/kissersk/textures/font/badges/miner.png",
    "assets/kissersk/textures/font/badges/farmer.png",
    "assets/kissersk/textures/font/badges/blacksmith.png",
    "assets/kissersk/textures/font/badges/mage.png",
)


def directory_records(raw, archive):
    """Read central-directory records verbatim, including all extra metadata."""
    cursor = archive.start_dir
    records = []
    for info in archive.infolist():
        if raw[cursor:cursor + 4] != b"PK\x01\x02":
            raise ValueError("Unsupported ZIP central directory")
        name_size, extra_size, comment_size = struct.unpack_from("<HHH", raw, cursor + 28)
        end = cursor + 46 + name_size + extra_size + comment_size
        records.append((info, raw[cursor:end]))
        cursor = end
    return records, cursor


def update_archive(archive_path, source_root):
    """Preserve original local/central records and replace the managed suffix."""
    archive_path = Path(archive_path)
    source_root = Path(source_root)
    raw = archive_path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as original:
        records, end = directory_records(raw, original)
        trailer = bytearray(raw[end:])
        if len(trailer) < 22 or trailer[:4] != b"PK\x05\x06":
            raise ValueError("Only a standard non-ZIP64 archive is supported")
        disk, directory_disk, disk_count, count, size, offset, comment_size = struct.unpack_from(
            "<4H2IH", trailer, 4
        )
        if (disk or directory_disk or disk_count != count or count != len(records)
                or offset != original.start_dir or size != end - original.start_dir
                or len(trailer) != 22 + comment_size):
            raise ValueError("Unsupported multi-disk, ZIP64 or prefixed archive")
        managed = [(info, record) for info, record in records if info.filename in MANAGED_PATHS]
        kept = [(info, record) for info, record in records if info.filename not in MANAGED_PATHS]
        suffix_start = min((info.header_offset for info, _ in managed), default=original.start_dir)
        if any(info.header_offset >= suffix_start for info, _ in kept):
            raise ValueError("Badge entries must follow all original archive entries")
        prefix = raw[:suffix_start]

    generated = io.BytesIO()
    with zipfile.ZipFile(generated, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as badges:
        for name in MANAGED_PATHS:
            info = zipfile.ZipInfo(name, (2026, 10, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            badges.writestr(info, (source_root / name).read_bytes(), compresslevel=9)
    badge_raw = generated.getvalue()
    with zipfile.ZipFile(generated) as badges:
        badge_records, _ = directory_records(badge_raw, badges)
        local_badges = badge_raw[:badges.start_dir]
    directory = bytearray(b"".join(record for _, record in kept))
    for info, record in badge_records:
        adjusted = bytearray(record)
        struct.pack_into("<I", adjusted, 42, len(prefix) + info.header_offset)
        directory.extend(adjusted)
    total = len(kept) + len(badge_records)
    directory_offset = len(prefix) + len(local_badges)
    if total >= 65535 or directory_offset >= 0xFFFFFFFF:
        raise ValueError("ZIP64 is not supported")
    struct.pack_into("<HHII", trailer, 8, total, total, len(directory), directory_offset)
    updated = prefix + local_badges + directory + trailer
    if updated != raw:
        temporary = archive_path.with_name(archive_path.name + ".tmp")
        temporary.write_bytes(updated)
        temporary.replace(archive_path)
    return hashlib.sha1(updated).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path, default=ROOT / "KisserskPack.zip")
    args = parser.parse_args()
    print(f"{update_archive(args.archive, ROOT)}  {args.archive.name}")


if __name__ == "__main__":
    main()
