from pathlib import Path
import pytest
from hyperborea.chargen import DB


def test_db():
    assert Path(DB).is_file()
