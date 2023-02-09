from hyperborea3.db import (
    execute_query_all,
    execute_query_one,
    get_count_from_table,
    list_tables,
    list_views,
    table_exists,
)
from hyperborea3.valid_data import (
    VALID_SQL_TABLES,
    VALID_SQL_VIEWS,
)


def test_execute_query_one_no_params():
    sql = """
        SELECT *
        FROM deities
        WHERE deity_id = 1
    """
    actual = execute_query_one(sql)
    expected = {
        "deity_id": 1,
        "deity_name": "Apollo",
        "primary_alignment": "Lawful",
    }
    assert actual == expected


def test_execute_query_one_with_params():
    sql = """
        SELECT *
        FROM deities
        WHERE deity_id = ?
    """
    actual = execute_query_one(sql, (1,))
    expected = {
        "deity_id": 1,
        "deity_name": "Apollo",
        "primary_alignment": "Lawful",
    }
    assert actual == expected


def test_execute_query_all_no_params():
    sql = """
        SELECT *
        FROM alignment
    """
    actual = execute_query_all(sql)
    expected = [
        {
            "align_id": 1,
            "short_name": "CE",
            "long_name": "Chaotic Evil",
        },
        {
            "align_id": 2,
            "short_name": "CG",
            "long_name": "Chaotic Good",
        },
        {
            "align_id": 3,
            "short_name": "LE",
            "long_name": "Lawful Evil",
        },
        {
            "align_id": 4,
            "short_name": "LG",
            "long_name": "Lawful Good",
        },
        {
            "align_id": 5,
            "short_name": "N",
            "long_name": "Neutral",
        },
    ]
    assert actual == expected


def test_execute_query_all_with_params():
    sql = """
        SELECT *
        FROM t010_familiars
        WHERE roll_2d8 BETWEEN ? AND ?
    """
    actual = execute_query_all(sql, (2, 3))
    expected = [
        {
            "roll_2d8": 2,
            "animal": "Archæopteryx",
        },
        {
            "roll_2d8": 3,
            "animal": "Ice Toad",
        },
    ]
    assert actual == expected


def test_table_exists_true():
    assert table_exists("alignment") is True


def test_table_exists_false():
    assert table_exists("fake_table") is False


# @pytest.mark.skip(
#     reason=(
#         "Currently failing on github "
#         "'sqlite3.OperationalError: no such table: sqlite_schema'"
#     )
# )
def test_db_tables():
    assert list_tables() == VALID_SQL_TABLES


# @pytest.mark.skip(
#     reason=(
#         "Currently failing on github "
#         "'sqlite3.OperationalError: no such table: sqlite_schema'"
#     )
# )
def test_db_views():
    assert list_views() == VALID_SQL_VIEWS


def test_get_count_from_table():
    actual = get_count_from_table("alignment")
    expected = 5
    assert actual == expected
