from typing import Any, Dict, List

from hyperborea3.chargen import ac_to_aac
from hyperborea3.db import execute_query_all

# from hyperborea3.valid_data import VALID_MONSTER_IDS


def get_all_monsters(ac_type: str = "descending") -> List[Dict[str, Any]]:
    """Get all monsters from database."""
    sql = """
        SELECT *
        FROM monsters
        ORDER BY monster_id;
    """
    monster_data = execute_query_all(sql)
    if ac_type == "ascending":
        for m in monster_data:
            m["ac"] = ac_to_aac(m["ac"])
    return monster_data
