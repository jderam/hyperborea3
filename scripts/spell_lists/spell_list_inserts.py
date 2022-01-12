import sys
import sqlite3


con = sqlite3.connect("../../hyperborea/hyperborea.sqlite3")
con.row_factory = sqlite3.Row
cur = con.cursor()

input_file = sys.argv[1]

# parse config options based on input file name
school = input_file[0:3]
assert school in [
    "mag",
    "cry",
    "ill",
    "nec",
    "pyr",
    "wch",
    "clr",
    "drd",
], f"Invalid school: {school}"

lvl_range = input_file[3:6]
assert lvl_range in ["1-3", "4-6"], f"Can't determine level range: {lvl_range}"

tbl_map = {
    "mag": "t093_mag_spell_list",
    "cry": "t094_cry_spell_list",
    "ill": "t095_ill_spell_list",
    "nec": "t096_nec_spell_list",
    "pyr": "t097_pyr_spell_list",
    "wch": "t098_wch_spell_list",
    "clr": "t099_clr_spell_list",
    "drd": "t100_drd_spell_list",
}
tbl = tbl_map[school]

# Delete existing data from target table
sql = f"DELETE FROM {tbl} WHERE spell_level BETWEEN ? AND ?;"
cur.execute(sql, (int(lvl_range[0]), int(lvl_range[2])))
con.commit()

with open(input_file, "r") as f:
    lines = f.readlines()


def col_to_spell_lvl(col_idx: int, lvl_range: str) -> int:
    if lvl_range == "1-3":
        spell_level = col_idx + 1
    elif lvl_range == "4-6":
        spell_level = col_idx + 4
    else:
        raise ValueError(f"Invalid value for lvl_range: {lvl_range}")
    return spell_level


for line in lines:
    line = line.replace("\n", "")
    line = line.split(")")
    for col_idx in range(len(line) - 1):
        spell_level = col_to_spell_lvl(col_idx, lvl_range)
        assert spell_level in range(
            1, 7
        ), f"Invalid calculated spell_level: {spell_level}"

        spell_info = line[col_idx]

        spell_name = spell_info.split("(")[0].strip()

        cur.execute("SELECT spell_id FROM spells WHERE spell_name = ?", (spell_name,))
        result = cur.fetchone()
        try:
            spell_id = dict(result)["spell_id"]
        except Exception:
            raise Exception(f"Failure to look up spell_id by name: {spell_name}")

        roll_range = spell_info.split("(")[1]
        roll_range = roll_range.replace("-", "–")
        r_min = int(roll_range.split("–")[0])
        r_max = int(roll_range.split("–")[1])
        if r_max == 0:
            r_max = 100

        print(f"INSERTING SPELL: {spell_name}")

        sql = f"INSERT INTO {tbl} (spell_level, spell_id, d100_min, d100_max) VALUES (?, ?, ?, ?);"  # noqa E501
        print(sql)

        values = (spell_level, spell_id, r_min, r_max)
        print(values)

        cur.execute(sql, values)
        print()

con.commit()
con.close()
