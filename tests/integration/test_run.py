import datetime
import re

from main import run

from services.datereader import DateReader
from services.filenamer import GenerationMode

D = datetime.datetime
SETTINGS = {"separator": "-", "identifier": GenerationMode.Paddedint}

def test_run_renames_by_date_and_orders_by_time(tmp_path, make_jpeg):
    make_jpeg("a.jpg", D(2024, 5, 1, 10, 0, 0))
    make_jpeg("b.jpg", D(2024, 5, 1, 9, 0, 0))
    make_jpeg("IMG_20240502.jpg")
    make_jpeg("undated.jpg")
    run(str(tmp_path), SETTINGS)

    names = sorted(p.name for p in tmp_path.iterdir())
    assert "2024-05-01-00001.jpg" in names
    assert "2024-05-01-00002.jpg" in names
    assert "2024-05-02-00001.jpg" in names
    assert any(re.fullmatch(r"undated-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}\.jpg", n) for n in names)

    first = tmp_path / "2024-05-01-00001.jpg"
    assert DateReader().read_from_metadata(str(first)) == D(2024, 5, 1, 9, 0, 0)


def test_run_twice_is_stable_with_padded_ids(tmp_path, make_jpeg):
    make_jpeg("a.jpg", D(2024, 5, 1, 10, 0, 0))
    make_jpeg("b.jpg", D(2024, 5, 1, 9, 0, 0))
    run(str(tmp_path), SETTINGS)
    after_first = sorted(p.name for p in tmp_path.iterdir())
    run(str(tmp_path), SETTINGS)
    assert sorted(p.name for p in tmp_path.iterdir()) == after_first