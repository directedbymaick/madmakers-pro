"""
MP4 faststart: rewrite a non-streamable MP4 (moov at end) into a streamable one
(moov immediately after ftyp). Adjusts the chunk-offset tables (stco / co64)
inside moov so they still point into the relocated mdat.
Pure stdlib, no ffmpeg.
"""
import struct
import sys
import os
import shutil


def read_box_header(data, pos):
    if pos + 8 > len(data):
        return None
    size = struct.unpack(">I", data[pos:pos + 4])[0]
    btype = data[pos + 4:pos + 8].decode("latin1")
    header = 8
    if size == 1:
        size = struct.unpack(">Q", data[pos + 8:pos + 16])[0]
        header = 16
    elif size == 0:
        size = len(data) - pos
    return btype, size, header


def find_top_box(data, name):
    pos = 0
    while pos < len(data) - 8:
        b = read_box_header(data, pos)
        if b is None:
            break
        btype, size, _ = b
        if btype == name:
            return pos, size
        if size <= 0:
            break
        pos += size
    return None, None


def shift_offsets(moov_bytes, delta):
    """Walk moov recursively. Whenever we hit stco/co64, add delta to every
    entry. Returns a fresh bytearray (same length) with patched offsets."""
    buf = bytearray(moov_bytes)
    container_types = {
        b"moov", b"trak", b"mdia", b"minf", b"stbl",
        b"edts", b"udta", b"mvex", b"moof", b"traf",
    }

    def walk(start, end):
        pos = start
        while pos < end - 8:
            size = struct.unpack(">I", buf[pos:pos + 4])[0]
            btype = bytes(buf[pos + 4:pos + 8])
            header = 8
            if size == 1:
                size = struct.unpack(">Q", buf[pos + 8:pos + 16])[0]
                header = 16
            elif size == 0:
                size = end - pos
            if size <= 0 or pos + size > end:
                return

            if btype == b"stco":
                # version(1) + flags(3) + entry_count(4) + entries(4 each)
                cnt = struct.unpack(">I", buf[pos + header + 4:pos + header + 8])[0]
                base = pos + header + 8
                for i in range(cnt):
                    o = base + i * 4
                    val = struct.unpack(">I", buf[o:o + 4])[0]
                    struct.pack_into(">I", buf, o, val + delta)
            elif btype == b"co64":
                cnt = struct.unpack(">I", buf[pos + header + 4:pos + header + 8])[0]
                base = pos + header + 8
                for i in range(cnt):
                    o = base + i * 8
                    val = struct.unpack(">Q", buf[o:o + 8])[0]
                    struct.pack_into(">Q", buf, o, val + delta)
            elif btype in container_types:
                walk(pos + header, pos + size)

            pos += size

    walk(0, len(buf))
    return bytes(buf)


def faststart(src, dst):
    with open(src, "rb") as f:
        data = f.read()

    ftyp_pos, ftyp_size = find_top_box(data, "ftyp")
    moov_pos, moov_size = find_top_box(data, "moov")
    mdat_pos, mdat_size = find_top_box(data, "mdat")

    if ftyp_pos is None or moov_pos is None or mdat_pos is None:
        raise RuntimeError("missing ftyp/moov/mdat box")

    if moov_pos < mdat_pos:
        print(f"  already faststart (moov at {moov_pos}, mdat at {mdat_pos}). copying as-is.")
        shutil.copy2(src, dst)
        return False

    # delta = how much chunk offsets must shift.
    # In the new file: ftyp | moov | mdat. Original mdat was at mdat_pos.
    # New mdat_pos = ftyp_size + moov_size. So delta = (ftyp_size + moov_size) - mdat_pos
    new_mdat_pos = ftyp_size + moov_size
    delta = new_mdat_pos - mdat_pos
    print(f"  ftyp={ftyp_size}B moov={moov_size}B mdat={mdat_size}B delta={delta:+d}")

    moov_bytes = data[moov_pos:moov_pos + moov_size]
    moov_patched = shift_offsets(moov_bytes, delta)

    # Build new file: ftyp | moov(patched) | mdat | (any tail beyond mdat we ignore)
    # Note: we drop intermediate `free` boxes between mdat and moov; safe.
    with open(dst, "wb") as f:
        f.write(data[ftyp_pos:ftyp_pos + ftyp_size])
        f.write(moov_patched)
        f.write(data[mdat_pos:mdat_pos + mdat_size])

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python faststart.py <input.mp4> [output.mp4]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src + ".fast.mp4"
    print(f"faststart: {src} -> {dst}")
    changed = faststart(src, dst)
    if changed:
        print("  OK (rewrote with moov first)")
