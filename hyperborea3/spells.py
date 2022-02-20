from importlib.resources import path
import sqlite3
from typing import Any, Dict, List

from hyperborea3.valid_data import VALID_SPELL_IDS

with path("hyperborea3", "hyperborea.sqlite3") as p:
    DBPATH = p
URI = f"file:{str(DBPATH)}?mode=ro"
con = sqlite3.connect(URI, check_same_thread=False, uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()


def get_all_spells() -> List[Dict[str, Any]]:
    """Get all spells from database."""
    cur.execute(
        """
        SELECT spell_id
             , spell_name
             , NULL as level
             , rng
             , dur
             , reversible
             , pp
             , spell_desc
          FROM spells;
        """,
    )
    spell_list: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    cur.execute(
        """
        SELECT spell_id
             , school
             , spell_level
          FROM v_complete_spell_list
         WHERE school != 'run'
        ORDER BY school;
        """,
    )
    school_data: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    for spell in spell_list:
        level = (", ").join(
            [
                f"{x['school']} {x['spell_level']}"
                for x in school_data
                if x["spell_id"] == spell["spell_id"]
            ]
        )
        spell["level"] = level
        if spell["reversible"] is not None:
            spell["reversible"] = bool(spell["reversible"])
    return spell_list


def get_spell(spell_id: int) -> Dict[str, Any]:
    """Get a spell from database."""
    if spell_id not in VALID_SPELL_IDS:
        raise ValueError(f"{spell_id=} is invalid.")
    cur.execute(
        """
        SELECT spell_id
             , spell_name
             , NULL as level
             , rng
             , dur
             , reversible
             , pp
             , spell_desc
          FROM spells
         WHERE spell_id = ?;
        """,
        (spell_id,),
    )
    spell_data: Dict[str, Any] = dict(cur.fetchone())
    cur.execute(
        """
        SELECT school
             , spell_level
          FROM v_complete_spell_list
         WHERE spell_id = ?
           AND school != 'run'
        ORDER BY school;
        """,
        (spell_id,),
    )
    schools: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    spell_data.update(
        {
            "level": (", ").join(
                [f"{x['school']} {x['spell_level']}" for x in schools]
            ),
            "reversible": bool(spell_data["reversible"]),
        }
    )
    return spell_data
