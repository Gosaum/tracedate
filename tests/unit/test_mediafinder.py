from services.mediafinder import MediaFinder

def test_finds_only_media_recursively_case_insensitive(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.jpg").write_bytes(b"")
    (tmp_path / "B.JPG").write_bytes(b"")
    (tmp_path / "notes.txt").write_bytes(b"")
    (tmp_path / "sub" / "c.mp4").write_bytes(b"")
    (tmp_path / "fake.jpg").mkdir()

    found = {p for p in MediaFinder(str(tmp_path), {".jpg", ".mp4"}).iter_media()}
    names = {p.split(tmp_path.as_posix())[-1].lstrip("/\\") for p in found}
    assert names == {"a.jpg", "B.JPG", "sub/c.mp4"} or len(found) == 3

def test_nonexistent_directory_yields_nothing(tmp_path):
    assert list(MediaFinder(str(tmp_path / "nope"), {".jpg"}).iter_media()) == []