import logging
from typing import Any, Dict, List

from hyperborea3.db import execute_query_all, execute_query_one
from hyperborea3.valid_data import VALID_SPELL_IDS

logger = logging.getLogger(__name__)


def get_all_spells() -> List[Dict[str, Any]]:
    """Get all spells from database."""
    all_spells_sql = """
        SELECT spell_id
             , spell_name
             , NULL as level
             , rng
             , dur
             , reversible
             , pp
             , spell_desc
          FROM spells;
    """
    spell_list = execute_query_all(all_spells_sql)
    school_sql = """
        SELECT spell_id
             , school
             , spell_level
          FROM v_complete_spell_list
         WHERE school != 'run'
        ORDER BY school;
    """
    school_data = execute_query_all(school_sql)
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
    get_spell_sql = """
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
    """
    spell_data = execute_query_one(get_spell_sql, (spell_id,))
    school_sql = """
        SELECT school
             , spell_level
          FROM v_complete_spell_list
         WHERE spell_id = ?
           AND school != 'run'
        ORDER BY school;
    """
    schools = execute_query_all(school_sql, (spell_id,))
    spell_data.update(
        {
            "level": (", ").join(
                [f"{x['school']} {x['spell_level']}" for x in schools]
            ),
            "reversible": bool(spell_data["reversible"]),
        }
    )
    return spell_data
