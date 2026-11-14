import datetime
import re

from services.filenamer import FileNamer, GenerationMode

DAY = datetime.date(2024, 5, 1)

def test_paddedint(tmp_path):
    names = FileNamer(str(tmp_path)).generate(3, DAY, "-", GenerationMode.Paddedint)
    assert names == ["2024-05-01-00001", "2024-05-01-00002", "2024-05-01-00003"]

def test_parensint_with_space_separator(tmp_path):
    names = FileNamer(str(tmp_path)).generate(3, DAY, " ", GenerationMode.Parensint)
    assert names == ["2024 05 01 (1)", "2024 05 01 (2)", "2024 05 01 (3)"]

def test_hexstring_format_and_uniqueness(tmp_path):
    names = FileNamer(str(tmp_path)).generate(10, DAY, "-", GenerationMode.Hexstring)
    assert len(set(names)) == 10
    assert all(re.fullmatch(r"2024-05-01-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}", n) for n in names)

def test_undated_always_uses_hex(tmp_path):
    names = FileNamer(str(tmp_path)).generate(2, None, "-", GenerationMode.Paddedint)
    assert all(n.startswith("undated-") for n in names)

def test_rename_keeps_extension(tmp_path):
    src = tmp_path / "IMG_0001.JPG"
    src.write_bytes(b"x")
    FileNamer(str(tmp_path)).rename(str(src), "2024-05-01-00001")
    assert (tmp_path / "2024-05-01-00001.JPG").exists()
    assert not src.exists()

def test_rename_never_overwrites(tmp_path):
    a, b = tmp_path / "a.jpg", tmp_path / "target.jpg"
    a.write_bytes(b"A")
    b.write_bytes(b"B")
    FileNamer(str(tmp_path)).rename(str(a), "target")
    assert a.exists() and b.read_bytes() == b"B"   # comportement actuel : on ignore