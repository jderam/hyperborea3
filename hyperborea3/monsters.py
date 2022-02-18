from importlib.resources import path
import sqlite3
from typing import Any, Dict, List

from hyperborea3.chargen import ac_to_aac

# from hyperborea3.valid_data import VALID_MONSTER_IDS

with path("hyperborea3", "hyperborea.sqlite3") as p:
    DBPATH = p
URI = f"file:{str(DBPATH)}?mode=ro"
con = sqlite3.connect(URI, check_same_thread=False, uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()


def get_all_monsters(ac_type: str = "descending") -> List[Dict[str, Any]]:
    """Get all monsters from database."""
    cur.execute(
        """
        SELECT *
          FROM monsters
        ORDER BY monster_id;
        """,
    )
    monster_data: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    if ac_type == "ascending":
        for m in monster_data:
            m["ac"] = ac_to_aac(m["ac"])
    return monster_data
