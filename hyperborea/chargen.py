from pathlib import Path
import random
import sqlite3
from typing import Dict, List


DB = f"{Path(__file__).parent}/hyperborea.sqlite3"
con = sqlite3.connect(DB, check_same_thread=False)
con.row_factory = sqlite3.Row
c = con.cursor()


def roll_dice(qty: int, sides: int) -> int:
    result = 0
    for i in range(qty):
        result += random.randint(1, sides)
    return result


def roll_ndn_drop_lowest(qty: int, sides: int, drop_qty: int) -> int:
    result = []
    for i in range(qty):
        result.append(roll_dice(1, sides))
    result.sort()
    return sum(result[drop_qty:])


def get_class_list(subclasses: bool = True):
    sql = """
            SELECT class_id
                 , class_name
                 , class_type
                 , subclass_of
              FROM classes
          """
    if subclasses is False:
        sql += " WHERE class_type = 'P'"
    c.execute(f"{sql};")
    result = [dict(x) for x in c.fetchall()]
    return result


def class_name_to_id(class_name: str):
    if class_name.lower() == "random":
        class_id = 0
    else:
        class_list = get_class_list()
        class_names = [x["class_name"].lower() for x in class_list]
        if class_name.lower() not in class_names:
            raise ValueError(f"class name not recognized: {class_name}")
        class_id_list = [
            x["class_id"]
            for x in class_list
            if x["class_name"].lower() == class_name.lower()
        ]
        assert len(class_id_list) == 1, "Ambiguous result"
        class_id = class_id_list[0]
    return class_id


def class_id_to_name(class_id: int) -> str:
    c.execute("SELECT class_name FROM classes WHERE class_id = ?;", (class_id,))
    return dict(c.fetchone())["class_name"]


def get_class_requirements(class_id: int):
    c.execute("SELECT * FROM class_attr_req WHERE class_id = ?;", (class_id,))
    return [dict(x) for x in c.fetchall()]


def roll_stats(method: int = 3, class_id: int = 0) -> Dict:
    """Roll stats using the various methods in the Player's Manual"""
    attr = {
        "st": {},
        "dx": {},
        "cn": {},
        "in": {},
        "ws": {},
        "ch": {},
    }
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
        are your character’s attribute scores.
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


def get_attr_mod(stat: str, score: int):
    match stat:
        case "st":
            tbl = "t001_strength"
        case "dx":
            tbl = "t002_dexterity"
        case "cn":
            tbl = "t003_constitution"
        case "in":
            tbl = "t004_intelligence"
        case "ws":
            tbl = "t005_wisdom"
        case "ch":
            tbl = "t006_charisma"
        case _:
            raise ValueError(f"Unrecognized value for stat: {stat}")
    c.execute(f"SELECT * FROM {tbl} WHERE score = ?;", (score,))
    result = dict(c.fetchone())
    return result


def get_attr(method: int = 3, class_id: int = 0) -> Dict:
    attr = roll_stats(method, class_id)
    for stat in attr.keys():
        score = attr[stat]["score"]
        mods = get_attr_mod(stat, score)
        attr[stat] = mods
    return attr


def get_qualifying_classes(attr: Dict, subclasses: bool) -> List[int]:
    """Return list of class_ids that can be used given the attr."""
    # Okay, this isn't the easiest code to parse. ¯\_(ツ)_/¯
    if subclasses is True:
        c.execute("SELECT * FROM class_attr_req;")
    else:
        c.execute(
            """
            SELECT car.*
              FROM classes c
              JOIN class_attr_req car
                ON c.class_id = car.class_id
             WHERE c.class_type = 'P';
        """
        )
    class_req = [dict(x) for x in c.fetchall()]
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
    return qual_classes


def select_random_class(attr: Dict, subclasses: bool) -> int:
    """Given a set of stats, determine an appropriate class.
    1. Find all qualifying classes by checking stat requirements.
    2. Randomly choose from among them.
    TODO: Might decide to add weighting based on primary attributes.
    """
    qual_classes = get_qualifying_classes(attr, subclasses)
    class_id = random.choice(qual_classes)
    return class_id


def get_level(class_id: int, xp: int) -> int:
    c.execute(
        """
        SELECT Max(level) as level
          FROM class_level
         WHERE class_id = ?
           AND xp <= ?
    """,
        (class_id, xp),
    )
    level = dict(c.fetchone())["level"]
    return level


def get_save_bonuses(class_id: int) -> Dict:
    c.execute(
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
    sv_bonus = dict(c.fetchone())
    return sv_bonus


def get_class_level_data(class_id: int, level: int) -> Dict:
    c.execute(
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
    result = dict(c.fetchone())
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
    hp = roll_dice(hd_qty, hd_size) + hp_plus + (level * hp_adj)
    # TODO: If we want to get pedantic about this, it should actually be a minimum
    # of 1 hp on each die roll. We can do an accumulator instead, although this
    # is likely an edge case where no one would actually be playing a PC this bad.
    if hp < level:
        hp = level
    return hp


def get_alignment(class_id: int) -> Dict:
    """Choose a random alignment based on the options available to a given class."""
    c.execute(
        """
        SELECT a.*
          FROM class_alignment ca
          JOIN alignment a
            ON ca.align_id = a.align_id
         WHERE ca.class_id = ?
    """,
        (class_id,),
    )
    allowed_alignments = [dict(x) for x in c.fetchall()]
    alignment = random.choice(allowed_alignments)
    return alignment


def get_starting_armour(class_id: int) -> List[Dict]:
    """Get starting armour by class.
    The SQL should always return one and only one result.
    """
    c.execute(
        """
        SELECT a.*
          FROM starting_armour s
          JOIN t074_armour a
            ON s.armour_id = a.armour_id
         WHERE s.class_id = ?
    """,
        (class_id,),
    )
    result = c.fetchone()
    armour = dict(result) if result is not None else result
    return armour


def get_starting_shield(class_id: int) -> List[Dict]:
    """Get starting shield by class.
    SQL should return one or zero results.
    """
    c.execute(
        """
        SELECT ts.*
          FROM starting_shield ss
          JOIN t075_shields ts
            ON ss.shield_id = ts.shield_id
         WHERE ss.class_id = ?
    """,
        (class_id,),
    )
    result = c.fetchone()
    shield = dict(result) if result is not None else result
    return shield


def calculate_ac(armour_ac: int, shield_def_mod: int, dx_def_adj: int) -> int:
    ac = armour_ac
    ac -= shield_def_mod
    ac -= dx_def_adj
    return ac


def ac_to_aac(ac: int) -> int:
    aac = 19 - ac
    return aac
