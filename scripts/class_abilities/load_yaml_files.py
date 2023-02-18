# mypy: ignore-errors

from contextlib import contextmanager
import os
import sqlite3
import yaml

cwd = os.getcwd()
assert cwd.split("/")[-1] == "class_abilities"


@contextmanager
def db_cur():
    URI = "../../hyperborea3/hyperborea.sqlite3"
    con = sqlite3.connect(URI, check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    yield cur
    con.commit()
    con.close()


yaml_files = os.listdir("yaml")

for yf in yaml_files:
    with open(f"yaml/{yf}", "r") as f:
        payload = yaml.safe_load(f)
    id = payload["id"]
    desc = payload["desc"]
    print(f"{id = }")
    print(f"{desc = }")
    with db_cur() as cur:
        sql = """
            UPDATE class_abilities
            SET ability_desc = ?
            WHERE class_ability_id = ?
        """
        cur.execute(sql, (desc, id))
