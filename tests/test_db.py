from hyperborea3.db import (
    execute_query_all,
    execute_query_one,
    table_exists,
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
