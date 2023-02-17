from importlib.resources import as_file, files
import logging
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from hyperborea3.valid_data import VALID_SQL_TABLES

logger = logging.getLogger(__name__)


with as_file(files("hyperborea3")) as db_path:
    DB_LOCATION = db_path


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


with sqlite3.connect(
    f"file:{DB_LOCATION}/hyperborea.sqlite3?mode=ro",
    check_same_thread=False,
    uri=True,
) as conn:
    conn.row_factory = dict_factory
    CUR = conn.cursor()


def get_cursor() -> sqlite3.Cursor:
    ## Currently runs very slowly during heavy load using the below code.
    ## Just keeping an open cursor CUR with the above code block for now
    ## until I can learn more about it.
    # with sqlite3.connect(
    #     f"file:{DB_LOCATION}/hyperborea.sqlite3?mode=ro",
    #     check_same_thread=False,
    #     uri=True,
    # ) as conn:
    #     conn.row_factory = dict_factory
    #     cur = conn.cursor()
    #     return cur
    return CUR


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


def list_tables() -> List[str]:
    """List all tables in sqlite database."""
    sql = """
        SELECT name
        FROM main.sqlite_schema
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """
    tables: List[str] = [x["name"] for x in execute_query_all(sql)]
    return tables


def list_views() -> List[str]:
    """List all views in sqlite database."""
    sql = """
        SELECT name
        FROM main.sqlite_schema
        WHERE type = 'view'
        ORDER BY name;
    """
    views: List[str] = [x["name"] for x in execute_query_all(sql)]
    return views


def get_count_from_table(table_name: str) -> int:
    """Get the row count of a table in sqlite database."""
    assert table_name in VALID_SQL_TABLES
    sql = f"""
        SELECT Count(1) AS row_count
        FROM {table_name};
    """
    row_count: int = execute_query_one(sql)["row_count"]
    return row_count
