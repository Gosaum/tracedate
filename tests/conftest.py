import datetime
import struct

from PIL import Image

import pytest

@pytest.fixture
def make_jpeg(tmp_path):

    def _make(name:str, taken:datetime.datetime|None=None):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (8, 8))
        if taken:
            exif = Image.Exif()
            exif[306] = taken.strftime("%Y:%m:%d %H:%M:%S")
            img.save(path, exif=exif)
        else:
            img.save(path)
        return path
    return _make

@pytest.fixture
def make_mov(tmp_path):

    def _make(name:str, created:datetime.datetime):
        secs = int((created - datetime.datetime(1904, 1, 1)).total_seconds())
        payload = b"\x00\x00\x00\x00" + struct.pack(">I", secs) + b"\x00" * 92
        mvhd = struct.pack(">I", 8 + len(payload)) + b"mvhd" + payload
        moov = struct.pack(">I", 8 + len(mvhd)) + b"moov" + mvhd
        path = tmp_path / name
        path.write_bytes(moov)
        return path
    return _make