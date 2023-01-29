from importlib.resources import path
import logging
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_cursor() -> sqlite3.Cursor:
    with path("hyperborea3", "hyperborea.sqlite3") as db_path:
        with sqlite3.connect(
            f"file:{str(db_path)}?mode=ro",
            check_same_thread=False,
            uri=True,
        ) as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            return cur


def execute_query_one(sql: str, params: Tuple[Any, ...] = ()) -> Dict[str, Any]:
    cur = get_cursor()
    cur.execute(sql, params)
    result: Dict[str, Any] = cur.fetchone()
    logger.debug(f"{result = }")
    return result


def execute_query_all(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
    cur = get_cursor()
    cur.execute(sql, params)
    result: List[Dict[str, Any]] = cur.fetchall()
    logger.debug(f"{result = }")
    return result


def table_exists(table_name: str) -> bool:
    sql = """
        SELECT Count(1) AS table_exists
        FROM sqlite_master
        WHERE type='table'
        AND name = ?
    """
    result: Optional[int] = execute_query_one(sql, (table_name,)).get("table_exists")
    logger.debug(f"{result = }")
    exists = bool(result)
    return exists
