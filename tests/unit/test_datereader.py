import datetime
import pytest

from services.datereader import DateReader

D = datetime.datetime

@pytest.fixture
def reader():
    return DateReader()

@pytest.mark.parametrize("filename, expected", [
    ("IMG_2024_05_01_123456.jpg", D(2024, 5, 1)),
    ("IMG20240501123456.jpg", None), # no separator, illegible
    ("IMG-2024-05-01-123456.jpg", D(2024, 5, 1)),
    ("2024 05 01 vacances.jpg", D(2024, 5, 1)),
    ("img.jpg", None), # undated
    ("IMG_20241301.jpg", None), # 13th month: not in calendar
    ("IMG_20240230.jpg", None), # 30 februar: not in calendar
    ("IMG_19990501.jpg", None), # 1999: too old
])

def test_read_from_filename(reader, filename, expected):
    assert reader.read_from_filename(filename) == expected

def test_read_from_metadata_jpeg(reader, make_jpeg):
    path = make_jpeg("a.jpg", D(2024, 5, 1, 10, 30, 0))
    assert reader.read_from_metadata(str(path)) == D(2024, 5, 1, 10, 30, 0)

def test_read_from_metadata_without_exif(reader, make_jpeg):
    assert reader.read_from_metadata(str(make_jpeg("a.jpg"))) is None

def test_read_from_metadata_mov(reader, make_mov):
    path = make_mov("clip.mov", D(2024, 5, 1, 8, 15, 0))
    assert reader.read_from_metadata(str(path)) == D(2024, 5, 1, 8, 15, 0)

def test_read_from_metadata_corrupted_file(reader, tmp_path):
    bad = tmp_path / "bad.jpg"
    bad.write_bytes(b"this is not a valid image file")
    assert reader.read_from_metadata(str(bad)) is None