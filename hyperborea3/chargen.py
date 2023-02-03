from importlib.resources import path
import logging
import random
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from hyperborea3.valid_data import (
    VALID_ALIGMENTS_SHORT,
    VALID_GENDERS,
    VALID_SQL_TABLES,
)

logger = logging.getLogger(__name__)

with path("hyperborea3", "hyperborea.sqlite3") as p:
    DBPATH = p
URI = f"file:{str(DBPATH)}?mode=ro"
con = sqlite3.connect(URI, check_same_thread=False, uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()


def list_tables() -> List[str]:
    """List all tables in sqlite database."""
    cur.execute(
        """
        SELECT name
          FROM sqlite_schema
         WHERE type = 'table'
           AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
        """
    )
    tables: List[str] = [dict(x)["name"] for x in cur.fetchall()]
    return tables


def list_views() -> List[str]:
    """List all views in sqlite database."""
    cur.execute(
        """
        SELECT name
          FROM sqlite_schema
         WHERE type = 'view'
        ORDER BY name;
        """
    )
    views: List[str] = [dict(x)["name"] for x in cur.fetchall()]
    return views


def get_count_from_table(table_name: str) -> int:
    """Get the row count of a table in sqlite database."""
    assert table_name in VALID_SQL_TABLES
    cur.execute(
        f"""
        SELECT Count(1) AS row_count
          FROM {table_name};
        """
    )
    row_count: int = cur.fetchone()["row_count"]
    return row_count


def roll_dice(qty: int, sides: int, reroll: List[int] = []) -> int:
    assert all([x in reroll for x in range(1, sides + 1)]) is not True
    result = 0
    for i in range(qty):
        die_roll = 0
        while die_roll == 0 or die_roll in reroll:
            die_roll = random.randint(1, sides)
        result += die_roll
    return result


def roll_ndn_drop_lowest(qty: int, sides: int, drop_qty: int) -> int:
    result = []
    for i in range(qty):
        result.append(roll_dice(1, sides))
    result.sort()
    return sum(result[drop_qty:])


def roll_ndn_drop_highest(qty: int, sides: int, drop_qty: int) -> int:
    result = []
    for i in range(qty):
        result.append(roll_dice(1, sides))
    result.sort()
    return sum(result[:-drop_qty])


def get_class_id_map():
    """Get mapping between class_id and class_name"""
    sql = """
            SELECT class_id
                 , class_name
              FROM classes
          """
    cur.execute(f"{sql};")
    result = [dict(x) for x in cur.fetchall()]
    class_map = {}
    for r in result:
        class_map[r["class_id"]] = r["class_name"]
    return class_map


def class_id_to_name(class_id: int) -> str:
    cur.execute("SELECT class_name FROM classes WHERE class_id = ?;", (class_id,))
    class_name = str(cur.fetchone()["class_name"])
    return class_name


def get_class_requirements(class_id: int):
    cur.execute("SELECT * FROM class_attr_req WHERE class_id = ?;", (class_id,))
    return [dict(x) for x in cur.fetchall()]


def roll_stats(method: int = 3, class_id: int = 0) -> Dict[str, Dict[str, int]]:
    """Roll stats using the various methods in the Player's Manual"""
    attr = {
        "st": {
            "score": 0,
        },
        "dx": {
            "score": 0,
        },
        "cn": {
            "score": 0,
        },
        "in": {
            "score": 0,
        },
        "ws": {
            "score": 0,
        },
        "ch": {
            "score": 0,
        },
    }
    # Ensure scores at least qualify for one of the principal classes
    while (
        attr["st"]["score"] < 9
        and attr["dx"]["score"] < 9
        and attr["in"]["score"] < 9
        and attr["ws"]["score"] < 9
    ):
        if method == 1:
            """Roll 3d6 for each attribute in order of strength, dexterity,
            constitution, intelligence, wisdom, and charisma; the results
            are your character's attribute scores.
            """
            for stat in attr.keys():
                attr[stat]["score"] = roll_dice(qty=3, sides=6)

        elif method == 2:
            """Roll 3d6 for each attribute in order of strength, dexterity,
            constitution, intel- ligence, wisdom, and charisma. Repeat
            these steps twice more, producing three sets of scores. Choose
            the set that best suits the type of character you would like
            to play.
            """
            max_total = 0
            for s in range(3):
                scores = [roll_dice(qty=3, sides=6) for x in range(6)]
                # print(s, scores, sum(scores))  # debug
                if sum(scores) > max_total:
                    max_total = sum(scores)
                    best_set = scores
            for stat in attr.keys():
                attr[stat]["score"] = best_set.pop(0)

        elif method == 3:
            """Roll 4d6 and discard the lowest die roll. Generate six scores
            using this method. Assign scores to attributes as desired.
            """
            for stat in attr.keys():
                attr[stat]["score"] = roll_ndn_drop_lowest(qty=4, sides=6, drop_qty=1)

        elif method == 4:
            """Roll 3d6 three times for each attribute in order of
            strength, dexterity, constitution, intelligence, wisdom,
            and charisma. Select the best result for each attribute.
            """
            for stat in attr.keys():
                attr[stat]["score"] = max([roll_dice(qty=3, sides=6) for i in range(3)])

        elif method == 5:
            """Roll 2d6+6 for each attribute in order of strength, dexterity,
            constitution, intelligence, wisdom, and charisma; the results
            are your character's attribute scores.
            """
            for stat in attr.keys():
                attr[stat]["score"] = roll_dice(qty=2, sides=6) + 6

        elif method == 6:
            """Choose your character class first (see Chapter 4: Classes),
            and then use the following technique:
                * Roll 3d6 for each attribute that does not have a
                required minimum score.
            * Roll 4d6 (discard low die result) for each attribute
            that does have a minimum requirement score, rerolling
            until you achieve the requisite minimum.
            """
            if class_id == 0:
                raise ValueError(
                    "If rolling with Method VI, you must select a specific class"
                )

            class_req = get_class_requirements(class_id)
            for stat in attr.keys():
                req = [x["min_score"] for x in class_req if x["attr"] == stat]
                if len(req) == 0:
                    attr[stat]["score"] = roll_dice(qty=3, sides=6)
                else:
                    min_score = req[0]
                    score = 0
                    while score < min_score:
                        score = roll_ndn_drop_lowest(qty=4, sides=6, drop_qty=1)
                    attr[stat]["score"] = score

        else:
            raise ValueError(f"Invalid value for method: {method}")
    return attr


def get_attr_mod(stat: str, score: int) -> Dict[str, int]:
    """Get the mods for a given stat."""
    if stat.lower() not in ["st", "dx", "cn", "in", "ws", "ch"]:
        raise ValueError(f"Invalid value for stat: {stat}")
    stat = stat.lower()
    tbl_map = {
        "st": "t001_strength",
        "dx": "t002_dexterity",
        "cn": "t003_constitution",
        "in": "t004_intelligence",
        "ws": "t005_wisdom",
        "ch": "t006_charisma",
    }
    tbl = tbl_map[stat]
    cur.execute(f"SELECT * FROM {tbl} WHERE score = ?;", (score,))
    result = dict(cur.fetchone())
    return result


def get_attr(method: int = 3, class_id: int = 0) -> Dict[str, Dict[str, int]]:
    attr = roll_stats(method, class_id)
    for stat in attr.keys():
        score = attr[stat]["score"]
        mods = get_attr_mod(stat, score)
        attr[stat] = mods
    return attr


def get_qualifying_classes(
    attr: Dict[str, Dict[str, int]], subclasses: int
) -> List[int]:
    """Return list of class_ids that can be used given the attr."""
    # principal classes, subclasses, and sub-subclasses
    if subclasses == 2:
        cur.execute("SELECT * FROM class_attr_req;")
    # principal classes and subclasses
    elif subclasses == 1:
        cur.execute(
            """
            SELECT car.*
              FROM classes c
              JOIN class_attr_req car
                ON c.class_id = car.class_id
             WHERE c.class_type IN ('P', 'S');
            """
        )
    # principal classes only
    elif subclasses == 0:
        cur.execute(
            """
            SELECT car.*
              FROM classes c
              JOIN class_attr_req car
                ON c.class_id = car.class_id
             WHERE c.class_type = 'P';
            """
        )
    class_req = [dict(x) for x in cur.fetchall()]
    not_met = list(
        set(
            [
                x["class_id"]
                for x in class_req
                if x["min_score"] > attr[x["attr"]]["score"]
            ]
        )
    )
    qual_classes = list(
        set([x["class_id"] for x in class_req if x["class_id"] not in not_met])
    )
    assert len(qual_classes) > 0, "There are no qualifying classes to choose from"
    return qual_classes


def select_random_class(attr: Dict[str, Dict[str, int]], subclasses: int) -> int:
    """Given a set of stats, determine an appropriate class.
    1. Find all qualifying classes by checking stat requirements.
    2. Randomly choose from among them.
    TODO: Might decide to add weighting based on primary attributes.
    """
    qual_classes = get_qualifying_classes(attr, subclasses)
    class_id = random.choice(qual_classes)
    return class_id


def get_level(class_id: int, xp: int) -> int:
    cur.execute(
        """
        SELECT Max(level) as level
          FROM class_level
         WHERE class_id = ?
           AND xp <= ?
        """,
        (class_id, xp),
    )
    level: int = cur.fetchone()["level"]
    return level


def get_xp_to_next(class_id: int, level: int) -> Optional[int]:
    """Get XP need to reach next level."""
    # if level is 12, there is no "next level"
    if level == 12:
        return None
    next_level = level + 1
    cur.execute(
        "SELECT xp FROM class_level WHERE class_id = ? AND level = ?;",
        (class_id, next_level),
    )
    xp_to_next: int = cur.fetchone()["xp"]
    return xp_to_next


def get_xp_bonus(class_id: int, attr: Dict[str, Dict[str, int]]) -> bool:
    """Determine if character qualifies for +10% XP bonus."""
    cur.execute(
        "SELECT attr FROM class_prime_attr WHERE class_id = ?;",
        (class_id,),
    )
    prime_attrs = [dict(x)["attr"] for x in cur.fetchall()]
    xp_bonus = all([attr[p]["score"] >= 16 for p in prime_attrs])
    return xp_bonus


def get_save_bonuses(class_id: int) -> Dict[str, int]:
    cur.execute(
        """
        SELECT death
             , transformation
             , device
             , avoidance
             , sorcery
          FROM classes
         WHERE class_id = ?
        """,
        (class_id,),
    )
    sv_bonus = dict(cur.fetchone())
    return sv_bonus


def get_class_level_data(class_id: int, level: int) -> Dict[str, Any]:
    cur.execute(
        """
        SELECT *
          FROM classes c
          JOIN class_level cl
            ON c.class_id = cl.class_id
         WHERE c.class_id = ?
           AND cl.level = ?
        """,
        (class_id, level),
    )
    result = dict(cur.fetchone())
    return result


def get_hd(class_id: int, level: int) -> str:
    """Returns string form of HD, e.g. '4d8' or '9d10+3'"""
    cl_data = get_class_level_data(class_id, level)
    hd_qty = cl_data["hd_qty"]
    hd_size = cl_data["hd_size"]
    hp_plus = cl_data["hp_plus"]
    hd = f"{hd_qty}d{hd_size}"
    if hp_plus > 0:
        hd += f"+{hp_plus}"
    return hd


def roll_hit_points(class_id: int, level: int, hp_adj: int) -> int:
    """Roll hit points for the PC.
    Minimum 1 hp per level.
    """
    cl_data = get_class_level_data(class_id, level)
    hd_qty = cl_data["hd_qty"]
    hd_size = cl_data["hd_size"]
    hp_plus = cl_data["hp_plus"]
    hp: int = roll_dice(hd_qty, hd_size) + hp_plus + (level * hp_adj)
    # TODO: If we want to get pedantic about this, it should actually be a minimum
    # of 1 hp on each die roll. We can do an accumulator instead, although this
    # is likely an edge case where no one would actually be playing a PC this bad.
    if hp < level:
        hp = level
    return hp


def get_combat_matrix(fa: int) -> Dict[int, int]:
    """Return combat matrix based on FA."""
    combat_matrix = {}
    for k in range(-9, 10):
        combat_matrix[k] = 20 - k - fa
    return combat_matrix


def get_alignment(class_id: int) -> Dict[str, Any]:
    """Choose a random alignment based on the options available to a given class."""
    cur.execute(
        """
        SELECT a.*
          FROM class_alignment ca
          JOIN alignment a
            ON ca.align_id = a.align_id
         WHERE ca.class_id = ?
        """,
        (class_id,),
    )
    allowed_alignments = [dict(x) for x in cur.fetchall()]
    alignment = random.choice(allowed_alignments)
    return alignment


def get_deity(short_alignment: str) -> Dict[str, Any]:
    """Randomly select a deity based on alignment."""
    assert (
        short_alignment in VALID_ALIGMENTS_SHORT
    ), f"Invalid alignment: {short_alignment}"
    if short_alignment[0] == "C":
        lkp_align = "Chaotic"
    elif short_alignment[0] == "L":
        lkp_align = "Lawful"
    elif short_alignment[0] == "N":
        lkp_align = "Neutral"
    cur.execute(
        """
        SELECT *
          FROM deities
         WHERE primary_alignment = ?;
        """,
        (lkp_align,),
    )
    deities = [dict(x) for x in cur.fetchall()]
    if short_alignment in ["CE", "LE"]:
        lkp_align = "Evil"
        cur.execute(
            """
            SELECT *
            FROM deities
            WHERE primary_alignment = ?;
            """,
            (lkp_align,),
        )
        deities.extend([dict(x) for x in cur.fetchall()])
    deity = random.choice(deities)
    return deity


def get_race_id() -> int:
    """Roll on race tables to get a randomly selected race."""
    d100_roll = roll_dice(1, 100)
    cur.execute(
        """SELECT race_id
             FROM t066_primary_races
            WHERE ? BETWEEN d100_min AND d100_max;
        """,
        (d100_roll,),
    )
    race_id: int = cur.fetchone()["race_id"]
    if race_id == 99:
        d12_roll = roll_dice(1, 12)
        cur.execute(
            """SELECT race_id
                 FROM t067_ancillary_races
                WHERE d12_roll = ?;
            """,
            (d12_roll,),
        )
        race_id = cur.fetchone()["race_id"]
    if race_id not in range(1, 25):
        raise ValueError(f"Unexpected race_id value: {race_id}. d100_roll={d100_roll}")
    return race_id


def get_race(race_id: int) -> str:
    cur.execute(
        """SELECT race
             FROM v_race_lkp
            WHERE race_id = ?;
        """,
        (race_id,),
    )
    race: str = cur.fetchone()["race"]
    return race


def get_gender() -> str:
    genders = ["Male", "Female", "Non-Binary"]
    gender = random.choices(genders, weights=[47.5, 47.5, 5.0])[0]
    return gender


def get_age(race_id: int) -> int:
    grouping_roll = roll_dice(1, 6)
    if 1 <= grouping_roll <= 3:
        # age_grouping = "Young Adult"
        age = 13 + roll_dice(1, 7)
    elif 4 <= grouping_roll <= 6:
        # age_grouping = "Adult"
        # hyperboreans are different
        if race_id == 5:
            age = 20 + roll_dice(1, 80)
        else:
            age = 20 + roll_dice(1, 24)
    else:
        ValueError(f"Result from d6 roll was outside the range 1-6: {grouping_roll}")
    return age


def inches_to_feet(inches: int) -> str:
    feet = inches // 12
    leftover_inches = inches % 12
    feet_inches = f'''{feet}'{leftover_inches}"'''
    return feet_inches


def get_height_weight_lookup_vals(race_id: int, gender: str) -> Tuple[int, str]:
    # Use random Male or Female for lookup if Non-Binary
    if gender not in VALID_GENDERS[:2]:
        lookup_gender = random.choice(VALID_GENDERS[:2])
    else:
        lookup_gender = gender
    # 3d6, reroll 1's
    # Amazon Female
    if race_id == 2 and lookup_gender == "Female":
        lookup_roll = roll_dice(3, 6, reroll=[1])
    # 4d6 drop lowest
    # Anglo-Saxons, Esquimaux-Ixians, Ixians, Kimmerians, Vikings, Yakuts
    elif race_id in [6, 8, 12, 13, 15, 24]:
        lookup_roll = roll_ndn_drop_lowest(4, 6, 1)
    # 4d6 drop highest
    # Esquimaux, Lemurians, Tlingits
    elif race_id in [4, 18, 23]:
        lookup_roll = roll_ndn_drop_highest(4, 6, 1)
    # 17 or 18
    # Hyperboreans
    elif race_id == 5:
        d6_roll = roll_dice(1, 6)
        if d6_roll in [1, 2]:
            lookup_roll = 17
        else:
            lookup_roll = 18
    # 3d6, reroll 6's
    # Lapps, Mu, Picts, Half-Blood Picts
    elif race_id in [10, 11, 17, 20]:
        lookup_roll = roll_dice(3, 6, reroll=[6])
    # Use average roll 9-12
    # Oon
    elif race_id == 21:
        lookup_roll = 10
    # Standard procedure: 3d6 roll
    # Everyone else
    else:
        lookup_roll = roll_dice(3, 6)
    return lookup_roll, lookup_gender


def get_height_and_weight(race_id: int, gender: str) -> Tuple[str, str]:
    lookup_roll, lookup_gender = get_height_weight_lookup_vals(race_id, gender)
    cur.execute(
        f"""
        SELECT {lookup_gender.lower()}_height AS height_range
             , {lookup_gender.lower()}_avg_weight AS avg_weight
          FROM t069_height_and_weight
         WHERE id = ?
        """,
        (lookup_roll,),
    )
    result = dict(cur.fetchone())
    height_range = [int(x) for x in result["height_range"].split("-")]
    height_inches = random.randint(height_range[0], height_range[1])
    height = inches_to_feet(height_inches)
    base_weight = result["avg_weight"]
    weight_variability_roll = roll_dice(1, 10)
    if weight_variability_roll in [1, 2, 3]:
        weight_multiplier = 1 - (roll_dice(1, 4) * 0.05)
        weight = round(base_weight * weight_multiplier)
    elif weight_variability_roll in [4, 5, 6, 7]:
        weight = base_weight
    elif weight_variability_roll in [8, 9, 10]:
        weight_multiplier = 1 + (roll_dice(1, 4) * 0.1)
        weight = round(base_weight * weight_multiplier)
    else:
        raise ValueError(
            "weight_variability_roll out of expected range (1-10): "
            f"{weight_variability_roll}"
        )
    return height, f"{weight} lbs."


def get_eye_colour(race_id: int, gender: str) -> str:
    # Common
    if race_id == 1:
        roll = roll_dice(1, 100) + 10
    # Amazon
    elif race_id == 2:
        roll = roll_dice(1, 20) + 58
    # Anglo-Saxon
    elif race_id == 13:
        roll = roll_dice(1, 50) + 58
    # Atlantean
    elif race_id == 3:
        roll = roll_dice(1, 6) + 4
    # Carolingian Frank
    elif race_id == 14:
        roll = roll_dice(1, 50) + 58
    # Esquimaux
    elif race_id == 4:
        roll = roll_dice(1, 50) + 10
    # Esquimaux-Ixian
    elif race_id == 15:
        roll = roll_dice(1, 50) + 10
    # Greek
    elif race_id == 16:
        roll = roll_dice(1, 50) + 12
    # Hyperborean
    elif race_id == 5:
        roll = roll_dice(1, 4) + 110
    # Ixian
    elif race_id == 6:
        if gender == "Non-Binary":
            gender = random.choice(["Male", "Female"])
        if gender == "Female":
            roll = roll_dice(1, 4)
        elif gender == "Male":
            return "Black"
        else:
            raise ValueError(f"Unrecognized value for gender: '{gender}'")
    # Kelt
    elif race_id == 7:
        roll = roll_dice(1, 30) + 58
    # Kimmerian
    elif race_id == 8:
        return "Grey, Dark"
    # Kimmeri-Kelt
    elif race_id == 9:
        roll = roll_dice(1, 50) + 58
    # Lapp
    elif race_id == 17:
        roll = roll_dice(1, 50) + 58
    # Lemurian
    elif race_id == 18:
        roll = roll_dice(1, 50) + 10
    # Moor
    elif race_id == 19:
        roll = roll_dice(1, 50) + 34
    # Mu
    elif race_id == 20:
        roll = roll_dice(1, 30) + 12
    # Oon
    elif race_id == 21:
        return "Grey, Dark"
    # Pict
    elif race_id == 10:
        roll = roll_dice(1, 6) + 79
    # Pict (Half-Blood)
    elif race_id == 11:
        roll = roll_dice(1, 50) + 10
    # Roman
    elif race_id == 22:
        roll = roll_dice(1, 50) + 58
    # Tlingit
    elif race_id == 23:
        roll = roll_dice(1, 50) + 10
    # Viking
    elif race_id == 12:
        roll = roll_dice(1, 20) + 58
    # Yakut
    elif race_id == 24:
        roll = roll_dice(1, 30) + 12

    cur.execute(
        """SELECT eye_colour
             FROM t070a_eye_colour
            WHERE ? BETWEEN roll_min AND roll_max;
        """,
        (roll,),
    )
    eye_colour: str = cur.fetchone()["eye_colour"]
    return eye_colour


def get_hair_colour(race_id: int, gender: str) -> str:
    # Common
    if race_id == 1:
        roll = roll_dice(1, 100) + 20
    # Amazon
    elif race_id == 2:
        roll = roll_dice(1, 50) + 40
    # Anglo-Saxon
    elif race_id == 13:
        roll = roll_dice(1, 50) + 50
    # Atlantean
    elif race_id == 3:
        roll = roll_dice(1, 20) + 20
    # Carolingian Frank
    elif race_id == 14:
        roll = roll_dice(1, 50) + 50
    # Esquimaux
    elif race_id == 4:
        roll = roll_dice(1, 30) + 40
    # Esquimaux-Ixian
    elif race_id == 15:
        return "Black"
    # Greek
    elif race_id == 16:
        roll = roll_dice(1, 20) + 40
    # Hyperborean
    elif race_id == 5:
        if gender == "Non-Binary":
            gender = random.choice(["Male", "Female"])
        if gender == "Female":
            roll = roll_dice(1, 12) + 120
        elif gender == "Male":
            roll = roll_dice(1, 10) + 122
        else:
            raise ValueError(f"Unrecognized value for gender: '{gender}'")
    # Ixian
    elif race_id == 6:
        return "Black"
    # Kelt
    elif race_id == 7:
        roll = roll_dice(1, 30) + 66
    # Kimmerian
    elif race_id == 8:
        return "Black"
    # Kimmeri-Kelt
    elif race_id == 9:
        roll = roll_dice(1, 50) + 40
    # Lapp
    elif race_id == 17:
        roll = roll_dice(1, 50) + 65
    # Lemurian
    elif race_id == 18:
        roll = roll_dice(1, 20) + 40
    # Moor
    elif race_id == 19:
        return "Black"
    # Mu
    elif race_id == 20:
        return "Black"
    # Oon
    elif race_id == 21:
        return "Black"
    # Pict
    elif race_id == 10:
        roll = roll_dice(1, 20)
    # Pict (Half-Blood)
    elif race_id == 11:
        roll = roll_dice(1, 10) + 18
    # Roman
    elif race_id == 22:
        roll = roll_dice(1, 20) + 40
    # Tlingit
    elif race_id == 23:
        return "Black"
    # Viking
    elif race_id == 12:
        roll = roll_dice(1, 30) + 90
    # Yakut
    elif race_id == 24:
        roll = roll_dice(1, 30) + 40

    cur.execute(
        """SELECT hair_colour
             FROM t070b_hair_colour
            WHERE ? BETWEEN roll_min AND roll_max;
        """,
        (roll,),
    )
    hair_colour: str = cur.fetchone()["hair_colour"]
    return hair_colour


def get_complexion(race_id: int, gender: str) -> str:
    # Common
    if race_id == 1:
        roll = roll_dice(1, 30) + 70
    # Amazon
    elif race_id == 2:
        roll = roll_dice(1, 30) + 70
    # Anglo-Saxon
    elif race_id == 13:
        roll = roll_dice(1, 20) + 80
    # Atlantean
    elif race_id == 3:
        roll = roll_dice(1, 10)
    # Carolingian Frank
    elif race_id == 14:
        roll = roll_dice(1, 20) + 80
    # Esquimaux
    elif race_id == 4:
        return "Jaundiced"
    # Esquimaux-Ixian
    elif race_id == 15:
        return "Dusky"
    # Greek
    elif race_id == 16:
        roll = roll_dice(1, 30) + 70
    # Hyperborean
    elif race_id == 5:
        return "Milky white"
    # Ixian
    elif race_id == 6:
        return "Dusky"
    # Kelt
    elif race_id == 7:
        roll = roll_dice(1, 20) + 80
    # Kimmerian
    elif race_id == 8:
        roll = roll_dice(1, 30) + 65
    # Kimmeri-Kelt
    elif race_id == 9:
        roll = roll_dice(1, 30) + 70
    # Lapp
    elif race_id == 17:
        roll = roll_dice(1, 30) + 65
    # Lemurian
    elif race_id == 18:
        roll = roll_dice(1, 20) + 40
    # Moor
    elif race_id == 19:
        roll = roll_dice(1, 20) + 10
    # Mu
    elif race_id == 20:
        return "Ebony"
    # Oon
    elif race_id == 21:
        return "Albino"
    # Pict
    elif race_id == 10:
        if gender == "Non-Binary":
            gender = random.choice(["Male", "Female"])
        if gender == "Female":
            roll = roll_dice(1, 12) + 88
        elif gender == "Male":
            roll = roll_dice(1, 12) + 80
        else:
            raise ValueError(f"Unrecognized value for gender: '{gender}'")
    # Pict (Half-Blood)
    elif race_id == 11:
        roll = roll_dice(1, 10) + 45
    # Roman
    elif race_id == 22:
        roll = roll_dice(1, 30) + 70
    # Tlingit
    elif race_id == 23:
        roll = roll_dice(1, 10) + 30
    # Viking
    elif race_id == 12:
        roll = roll_dice(1, 20) + 80
    # Yakut
    elif race_id == 24:
        roll = roll_dice(1, 50) + 50

    cur.execute(
        """SELECT complexion
             FROM t070c_complexion
            WHERE ? BETWEEN roll_min AND roll_max;
        """,
        (roll,),
    )
    complexion: str = cur.fetchone()["complexion"]
    return complexion


def get_languages(bonus_languages: int) -> List[str]:
    """Get known languages."""
    languages = []
    cur.execute(
        """
        SELECT language_dialect
          FROM t071_languages
         WHERE language_id = 1
        """
    )
    language = cur.fetchone()["language_dialect"]
    languages.append(language)
    if bonus_languages > 0:
        new_languages_learned = 0
        while new_languages_learned < bonus_languages:
            d100_roll = roll_dice(1, 100)
            cur.execute(
                """
                SELECT language_dialect
                FROM t071_languages
                WHERE ? BETWEEN d100_min AND d100_max
                """,
                (d100_roll,),
            )
            language = cur.fetchone()["language_dialect"]
            if language not in languages:
                languages.append(language)
                new_languages_learned += 1
    return languages


def get_starting_armour(class_id: int) -> Dict[str, Any]:
    """Get starting armour by class.
    The SQL should always return one and only one result.
    """
    cur.execute(
        """
        SELECT a.*
          FROM starting_armour s
          JOIN t074_armour a
            ON s.armour_id = a.armour_id
         WHERE s.class_id = ?
        """,
        (class_id,),
    )
    armour = dict(cur.fetchone())
    return armour


def get_starting_shield(class_id: int) -> Optional[Dict[str, Any]]:
    """Get starting shield by class.
    SQL should return one or zero results.
    """
    cur.execute(
        """
        SELECT ts.*
          FROM starting_shield ss
          JOIN t075_shields ts
            ON ss.shield_id = ts.shield_id
         WHERE ss.class_id = ?
        """,
        (class_id,),
    )
    result = cur.fetchone()
    shield = dict(result) if result is not None else result
    return shield


def get_starting_weapons_melee(class_id: int) -> List[Dict[str, Any]]:
    """Get starting melee weapons by class."""
    cur.execute(
        """
        SELECT w.*
             , sw.qty
          FROM starting_weapons_melee sw
          JOIN t076_melee_weapons w
            ON sw.weapon_id = w.weapon_id
         WHERE sw.class_id = ?;
        """,
        (class_id,),
    )
    melee_weapons = [dict(x) for x in cur.fetchall()]
    for mw in melee_weapons:
        mw["hurlable"] = bool(mw["hurlable"])
        mw["atk_rate"] = "1/1"
        mw["melee_atk"] = 0
        mw["hurled_atk"] = 0 if mw["hurlable"] else None
        mw["dmg_adj"] = 0
        mw["mastery"] = False
    return melee_weapons


def get_starting_weapons_missile(class_id: int) -> List[Dict[str, Any]]:
    """Get starting missile weapons by class."""
    cur.execute(
        """
        SELECT w.*
             , sw.qty
             , sw.ammunition
          FROM starting_weapons_missile sw
          JOIN t077_missile_weapons w
            ON sw.weapon_id = w.weapon_id
         WHERE sw.class_id = ?;
        """,
        (class_id,),
    )
    missile_weapons = [dict(x) for x in cur.fetchall()]
    for mw in missile_weapons:
        mw["hurled"] = bool(mw["hurled"])
        mw["launched"] = bool(mw["launched"])
        mw["missile_atk"] = 0
        mw["dmg_adj"] = 0
        mw["mastery"] = False
    return missile_weapons


def get_unskilled_weapon_penalty(class_id: int) -> int:
    """Get penalty when using a weapon not in the favoured list."""
    cur.execute(
        """
        SELECT attack_penalty
          FROM t134_unskilled_weapon_attack_penalty
         WHERE class_id = ?;
        """,
        (class_id,),
    )
    unskilled_penalty: int = cur.fetchone()["attack_penalty"]
    return unskilled_penalty


def get_favoured_weapons(class_id: int) -> Dict[str, Any]:
    """Get list of favoured weapons for a given class_id."""
    # get favoured melee weapons
    cur.execute(
        """
        SELECT tmw.*
          FROM class_favoured_weapons_melee cfwm
          JOIN t076_melee_weapons tmw
            ON cfwm.weapon_id = tmw.weapon_id
         WHERE cfwm.class_id = ?
        ORDER BY tmw.weapon_id;
        """,
        (class_id,),
    )
    fav_wpns_melee: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    # get favoured missile weapons
    cur.execute(
        """
        SELECT tmw.*
          FROM class_favoured_weapons_missile cfwm
          JOIN t077_missile_weapons tmw
            ON cfwm.weapon_id = tmw.weapon_id
         WHERE cfwm.class_id = ?
        ORDER BY tmw.weapon_id;
        """,
        (class_id,),
    )
    fav_wpns_missile: List[Dict[str, Any]] = [dict(x) for x in cur.fetchall()]
    # get unskilled penalty
    unskilled_penalty = get_unskilled_weapon_penalty(class_id)
    # get "any" (set True for classes proficient in any/all weapons)
    favoured_any: bool = True if unskilled_penalty == 0 else False
    favoured_weapons = {
        "any": favoured_any,
        "weapons_melee": fav_wpns_melee,
        "weapons_missile": fav_wpns_missile,
        "unskilled_penalty": unskilled_penalty,
    }
    return favoured_weapons


def get_starting_gear(class_id: int) -> List[str]:
    """Get starting equipment items by class."""
    cur.execute(
        """
        SELECT item
          FROM starting_gear
         WHERE class_id = ?;
        """,
        (class_id,),
    )
    equipment = [x["item"] for x in cur.fetchall()]
    return equipment


def get_starting_money() -> Dict[str, int]:
    """Get starting money."""
    gp = roll_dice(1, 4) + 1
    money = {
        "pp": 0,
        "gp": gp,
        "ep": 0,
        "sp": 0,
        "cp": 0,
    }
    return money


def calculate_ac(armour_ac: int, shield_def_mod: int, dx_def_adj: int) -> int:
    ac = armour_ac
    ac -= shield_def_mod
    ac -= dx_def_adj
    return ac


def get_next_atk_rate(atk_rate: str) -> str:
    atk_progression = [
        "1/1",
        "3/2",
        "2/1",
        "5/2",
        "3/1",
    ]
    atk_prog_idx = atk_progression.index(atk_rate)
    atk_prog_idx += 1
    return atk_progression[atk_prog_idx]


def ac_to_aac(ac: int) -> int:
    aac = 19 - ac
    return aac


def get_thief_skills(
    class_id: int,
    level: int,
    dx_score: int,
    in_score: int,
    ws_score: int,
) -> Optional[List[Dict[str, Any]]]:
    """Returns a list of dictionaries of thief skills.
    thief_skill (str): The key value for the skill used in db lookups
    skill_name  (str): The user-friendly name of the skill for display
    skill_roll  (int): The x in 12 chance of success
    stat        (str): The associated ability, which grats a +1 bonus for 16+
    """
    # input validation
    if class_id not in range(1, 34):
        raise ValueError(f"Invalid class_id: {class_id}")
    if level not in range(1, 13):
        raise ValueError(f"Invalid value for level: {level}")
    if dx_score not in range(1, 19):
        raise ValueError(f"Invalid value for dx_score: {dx_score}")
    if in_score not in range(1, 19):
        raise ValueError(f"Invalid value for in_score: {in_score}")
    if ws_score not in range(1, 19):
        raise ValueError(f"Invalid value for ws_score: {ws_score}")

    # get the skills for this class
    cur.execute(
        """SELECT thief_skill
             FROM class_thief_abilities
            WHERE class_id = ?;
        """,
        (class_id,),
    )
    skills_list = [dict(x) for x in cur.fetchall()]
    if len(skills_list) == 0:
        return None

    # get friendly skill names, with special rule for Huntsman
    # ("Manipulate Traps" becomes "Wilderness Traps" for Huntsman only)
    for sk in skills_list:
        if class_id == 8 and sk["thief_skill"] == "manipulate_traps":
            skill_name = "Wilderness Traps"
        else:
            skill_name = sk["thief_skill"].replace("_", " ").title()
        sk.update({"skill_name": skill_name})

    # get thief skill scores
    for sk in skills_list:
        sql = f"SELECT {sk['thief_skill']} FROM t016_thief_abilities WHERE level = ?;"
        cur.execute(sql, (level,))
        skill_roll = dict(cur.fetchone())[sk["thief_skill"]]
        sk.update({"skill_roll": skill_roll})

    # apply bonuses (if any)
    for sk in skills_list:
        sql = "SELECT stat FROM thief_ability_bonuses WHERE thief_skill = ?;"
        cur.execute(sql, (sk["thief_skill"],))
        stat = dict(cur.fetchone())["stat"]
        sk.update({"stat": stat})
        if stat == "dx" and dx_score >= 16:
            sk["skill_roll"] += 1
        if stat == "in" and in_score >= 16 and sk["skill_roll"] is not None:
            sk["skill_roll"] += 1
        if stat == "ws" and ws_score >= 16:
            sk["skill_roll"] += 1

    return skills_list


def get_turn_undead_matrix(ta: int, turn_adj: int) -> Optional[Dict[str, str]]:
    """Get turn undead matrix. Apply CH turning adjustment if applicable."""
    if ta == 0:
        return None
    cur.execute(
        """
        SELECT undead_type_00
             , undead_type_01
             , undead_type_02
             , undead_type_03
             , undead_type_04
             , undead_type_05
             , undead_type_06
             , undead_type_07
             , undead_type_08
             , undead_type_09
             , undead_type_10
             , undead_type_11
             , undead_type_12
             , undead_type_13
          FROM t013_turn_undead
         WHERE ta = ?;
        """,
        (ta,),
    )
    turn_undead_matrix = dict(cur.fetchone())
    if turn_adj != 0:
        for k, v in turn_undead_matrix.items():
            if ":" in v:
                turn_roll = int(v.split(":")[0])
                turn_roll += turn_adj
                if turn_roll > 0:
                    turn_undead_matrix[k] = f"{turn_roll}:12"
                else:
                    turn_undead_matrix[k] = "NT"
    return turn_undead_matrix


def get_caster_schools(class_id: int) -> List[str]:
    """Get the school(s) the character will get their spells known from."""
    cur.execute(
        "SELECT school_code FROM classes WHERE class_id = ?;",
        (class_id,),
    )
    school_code: Optional[str] = cur.fetchone()["school_code"]
    if school_code is None:
        return []
    schools = [x.strip() for x in school_code.split(",")]
    # need to make a random school selection for shaman
    if len(schools) > 1:
        for i in range(len(schools)):
            school_choices = schools[i].split("/")
            if len(school_choices) > 1:
                schools[i] = random.choice(school_choices)
    return schools


def get_random_spell(
    school: str,
    spell_level: int,
    d100_roll: Optional[int] = None,
) -> Dict[str, Any]:
    """Get a randomly rolled-for spell."""
    if d100_roll is None:
        d100_roll = roll_dice(1, 100)
    assert d100_roll in range(1, 101)
    cur.execute(
        """
        SELECT school
             , spell_level
             , spell_id
             , spell_name
             , rng as 'range'
             , dur as duration
             , reversible
             , pp
             , spell_desc
          FROM v_complete_spell_list
         WHERE school = ?
           AND spell_level = ?
           AND ? BETWEEN d100_min AND d100_max;
        """,
        (school, spell_level, d100_roll),
    )
    try:
        result = dict(cur.fetchone())
    except TypeError:
        print(f"Got no result back. {school=} {spell_level=} {d100_roll=}")
        raise
    if result["reversible"] is not None:
        result["reversible"] = bool(result["reversible"])
    return result


def get_spells(class_id: int, level: int, ca: int) -> Optional[Dict[str, Any]]:
    """Return the list of spells known for the character."""
    if ca == 0:
        return None
    schools = get_caster_schools(class_id)
    if len(schools) == 0:
        return None
    else:
        spells: Dict[str, Any] = {}
    for school in schools:
        spells[school] = {}
        cur.execute(
            """
            SELECT *
            FROM class_spells_by_level
            WHERE class_id = ?
              AND level = ?
              AND school = ?;
            """,
            (class_id, level, school),
        )
        result = cur.fetchone()
        if result is None:
            continue
        try:
            class_spells = dict(result)
        except TypeError:
            print(
                "No entry found in class_spells_by_level."
                f" {class_id=} {level=} {school=}"
            )
            raise
        spells[school]["spells_per_day"] = {
            "lvl1": class_spells["spells_per_day1"],
            "lvl2": class_spells["spells_per_day2"],
            "lvl3": class_spells["spells_per_day3"],
            "lvl4": class_spells["spells_per_day4"],
            "lvl5": class_spells["spells_per_day5"],
            "lvl6": class_spells["spells_per_day6"],
        }
        spells[school]["spells_known"] = []
        for k in [
            "spells_known1",
            "spells_known2",
            "spells_known3",
            "spells_known4",
            "spells_known5",
            "spells_known6",
        ]:
            spell_level = int(k[-1])
            spell_qty = class_spells[k]
            added_counter = 0
            while added_counter < spell_qty:
                # Make a 1-99 roll for Runegravers so we don't have one of the 3
                # runes having a 1% greater chance of getting selected.
                if class_id == 20:
                    d100_roll = roll_dice(1, 99)
                    random_spell = get_random_spell(
                        school, spell_level, d100_roll=d100_roll
                    )
                else:
                    random_spell = get_random_spell(school, spell_level)
                already_known = [x["spell_id"] for x in spells[school]["spells_known"]]
                if random_spell["spell_id"] not in already_known:
                    spells[school]["spells_known"].append(random_spell)
                    added_counter += 1
    return spells


def apply_spells_per_day_bonus(
    spells: Optional[Dict[str, Any]],
    bonus_spells_in: int,
    bonus_spells_ws: int,
) -> Optional[Dict[str, Any]]:
    """Increase spells per day for high IN/WS scores. Must already have at least
    one spell per day for the given level.
    """
    if spells is None:
        return None
    for school in spells.keys():
        if school in ["clr", "drd"]:
            for i in range(bonus_spells_ws, 0, -1):
                lvl_key = f"lvl{i}"
                # if spells[school]["spells_per_day"][lvl_key] > 0:
                if spells[school].get("spells_per_day", {}).get(lvl_key, 0) > 0:
                    spells[school]["spells_per_day"][lvl_key] += 1
        elif school in [
            "mag",
            "cry",
            "ill",
            "nec",
            "pyr",
            "wch",
        ]:
            for i in range(bonus_spells_in, 0, -1):
                lvl_key = f"lvl{i}"
                # if spells[school]["spells_per_day"][lvl_key] > 0:
                if spells[school].get("spells_per_day", {}).get(lvl_key, 0) > 0:
                    spells[school]["spells_per_day"][lvl_key] += 1
        elif school == "run":
            # no bonus for runegravers
            continue
        else:
            raise ValueError(f"Invalid value for school: {school}")
    return spells


def get_class_abilities(class_id: int, level: int) -> List[Dict[str, Any]]:
    """Get class abilities from class abilities table."""
    cur.execute(
        """
        SELECT *
          FROM class_abilities
         WHERE class_id = ?
           AND level <= ?
        ORDER BY level, ability_title;
        """,
        (class_id, level),
    )
    class_abilities = [dict(x) for x in cur.fetchall()]
    return class_abilities


def get_random_familiar() -> str:
    """Roll 2d8 to get a random familiar."""
    roll = roll_dice(2, 8)
    cur.execute(
        """
        SELECT animal
          FROM t010_familiars
         WHERE roll_2d8 = ?;
        """,
        (roll,),
    )
    animal: str = cur.fetchone()["animal"]
    return animal


def get_priest_abilities(deity_id: int, level: int) -> List[Dict[str, Any]]:
    """Get priest Specialized Faith abilities."""
    cur.execute(
        """
        SELECT *
          FROM t047_priest_abilities
         WHERE deity_id = ?
           AND level <= ?
        ORDER BY level;
        """,
        (deity_id, level),
    )
    priest_abilities = [dict(x) for x in cur.fetchall()]
    return priest_abilities


def get_secondary_skill() -> str:
    roll = roll_dice(1, 60)
    cur.execute(
        """
        SELECT *
          FROM t072_secondary_skills
         WHERE id = ?;
        """,
        (roll,),
    )
    secondary_skill: str = cur.fetchone()["skill_name"]
    return secondary_skill
