import logging
import random
from typing import Any, Dict, List, Optional, Tuple

from hyperborea3.db import execute_query_all, execute_query_one
from hyperborea3.valid_data import (
    VALID_ABILITIES,
    VALID_ABILITY_SCORES,
    VALID_ALIGMENTS_SHORT,
    VALID_CLASS_IDS,
    VALID_GENDERS,
    VALID_LEVELS,
    VALID_SCHOOLS,
    VALID_SPELL_LEVELS,
)

logger = logging.getLogger(__name__)


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
    result = execute_query_all(sql)
    class_map = {r["class_id"]: r["class_name"] for r in result}
    return class_map


def class_id_to_name(class_id: int) -> str:
    sql = "SELECT class_name FROM classes WHERE class_id = ?;"
    class_name: str = execute_query_one(sql, (class_id,))["class_name"]
    return class_name


def get_class_requirements(class_id: int):
    sql = "SELECT * FROM class_attr_req WHERE class_id = ?;"
    result = execute_query_all(sql, (class_id,))
    return result


def roll_stats(method: int = 3, class_id: int = 0) -> Dict[str, Dict[str, int]]:
    """Roll stats using the various methods in the Player's Manual"""
    attr = {ability: {"score": 0} for ability in VALID_ABILITIES}
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
    stat = stat.lower()
    if stat not in VALID_ABILITIES:
        raise ValueError(f"Invalid value for stat: {stat}")
    tbl_map = {
        "st": "t001_strength",
        "dx": "t002_dexterity",
        "cn": "t003_constitution",
        "in": "t004_intelligence",
        "ws": "t005_wisdom",
        "ch": "t006_charisma",
    }
    tbl = tbl_map[stat]
    result = execute_query_one(f"SELECT * FROM {tbl} WHERE score = ?;", (score,))
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
        sql = "SELECT * FROM class_attr_req;"
    # principal classes and subclasses
    elif subclasses == 1:
        sql = """
            SELECT car.*
            FROM classes c
            JOIN class_attr_req car
            ON c.class_id = car.class_id
            WHERE c.class_type IN ('P', 'S');
        """
    # principal classes only
    elif subclasses == 0:
        sql = """
            SELECT car.*
            FROM classes c
            JOIN class_attr_req car
            ON c.class_id = car.class_id
            WHERE c.class_type = 'P';
        """
    else:
        raise ValueError(f"Unrecognized value for subclasses: {subclasses}")
    class_req = execute_query_all(sql)
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
    sql = """
        SELECT Max(level) as level
        FROM class_level
        WHERE class_id = ?
        AND xp <= ?
    """
    level: int = execute_query_one(sql, (class_id, xp))["level"]
    return level


def get_xp_to_next(class_id: int, level: int) -> Optional[int]:
    """Get XP need to reach next level."""
    # if level is 12, there is no "next level"
    if level == 12:
        return None
    next_level = level + 1
    sql = "SELECT xp FROM class_level WHERE class_id = ? AND level = ?;"
    xp_to_next: int = execute_query_one(sql, (class_id, next_level))["xp"]
    return xp_to_next


def get_xp_bonus(class_id: int, attr: Dict[str, Dict[str, int]]) -> bool:
    """Determine if character qualifies for +10% XP bonus."""
    sql = "SELECT attr FROM class_prime_attr WHERE class_id = ?;"
    result: List[Dict[str, str]] = execute_query_all(sql, (class_id,))
    prime_attrs = [x["attr"] for x in result]
    xp_bonus = all([attr[p]["score"] >= 16 for p in prime_attrs])
    return xp_bonus


def get_save_bonuses(class_id: int) -> Dict[str, int]:
    sql = """
        SELECT death
             , transformation
             , device
             , avoidance
             , sorcery
          FROM classes
         WHERE class_id = ?
    """
    sv_bonus = execute_query_one(sql, (class_id,))
    return sv_bonus


def get_class_level_data(class_id: int, level: int) -> Dict[str, Any]:
    sql = """
        SELECT *
          FROM classes c
          JOIN class_level cl
            ON c.class_id = cl.class_id
         WHERE c.class_id = ?
           AND cl.level = ?
    """
    result = execute_query_one(sql, (class_id, level))
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
    sql = """
        SELECT a.*
          FROM class_alignment ca
          JOIN alignment a
            ON ca.align_id = a.align_id
         WHERE ca.class_id = ?
    """
    allowed_alignments = execute_query_all(sql, (class_id,))
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
    sql = """
        SELECT *
          FROM deities
         WHERE primary_alignment = ?;
    """
    deities = execute_query_all(sql, (lkp_align,))
    if short_alignment in ["CE", "LE"]:
        lkp_align = "Evil"
        deities.extend(execute_query_all(sql, (lkp_align,)))
    deity = random.choice(deities)
    return deity


def get_race_id() -> int:
    """Roll on race tables to get a randomly selected race."""
    d100_roll = roll_dice(1, 100)
    sql = """SELECT race_id
             FROM t066_primary_races
            WHERE ? BETWEEN d100_min AND d100_max;
    """
    race_id: int = execute_query_one(sql, (d100_roll,))["race_id"]
    if race_id == 99:
        d12_roll = roll_dice(1, 12)
        sql_a = """SELECT race_id
                 FROM t067_ancillary_races
                WHERE d12_roll = ?;
        """
        race_id = execute_query_one(sql_a, (d12_roll,))["race_id"]
    return race_id


def get_race(race_id: int) -> str:
    sql = """
        SELECT race
        FROM v_race_lkp
        WHERE race_id = ?;
    """
    race: str = execute_query_one(sql, (race_id,))["race"]
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
    sql = f"""
        SELECT {lookup_gender.lower()}_height AS height_range
             , {lookup_gender.lower()}_avg_weight AS avg_weight
          FROM t069_height_and_weight
         WHERE id = ?
    """
    result = execute_query_one(sql, (lookup_roll,))
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

    sql = """
        SELECT eye_colour
        FROM t070a_eye_colour
        WHERE ? BETWEEN roll_min AND roll_max;
    """
    eye_colour: str = execute_query_one(sql, (roll,))["eye_colour"]
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

    sql = """
        SELECT hair_colour
        FROM t070b_hair_colour
        WHERE ? BETWEEN roll_min AND roll_max;
    """
    hair_colour: str = execute_query_one(sql, (roll,))["hair_colour"]
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

    sql = """
        SELECT complexion
        FROM t070c_complexion
        WHERE ? BETWEEN roll_min AND roll_max;
    """
    complexion: str = execute_query_one(sql, (roll,))["complexion"]
    return complexion


def get_languages(race_id: int, bonus_languages: int) -> List[str]:
    """Get known languages."""
    languages = []
    sql1 = """
        SELECT language_dialect
          FROM t071_languages
         WHERE language_id = ?
    """
    language = execute_query_one(sql1, (1,))["language_dialect"]
    languages.append(language)
    # racial language, if applicable
    racial_languages = {
        2: 6,
        3: 7,
        # 4: random.choice([3, 4]),
        5: 9,
        6: 19,
        7: 11,
        # 8: random.choice([10, 20]),
        # 9: random.choice([10, 11]),
        10: 12,
        11: 12,
        12: 17,
        13: 16,
        14: 13,
        15: 5,
        16: 8,
        17: 22,
        18: 14,
        19: 2,
        20: 15,
        21: 18,
        22: 13,
        23: 21,
        24: 23,
    }
    racial_languages[4] = random.choice([3, 4])
    racial_languages[8] = random.choice([10, 20])
    racial_languages[9] = random.choice([10, 11])
    if race_id in racial_languages:
        language_id = racial_languages[race_id]
        language = execute_query_one(sql1, (language_id,))["language_dialect"]
        languages.append(language)
    if bonus_languages > 0:
        new_languages_learned = 0
        while new_languages_learned < bonus_languages:
            d100_roll = roll_dice(1, 100)
            sql2 = """
                SELECT language_dialect
                FROM t071_languages
                WHERE ? BETWEEN d100_min AND d100_max
            """
            language = execute_query_one(sql2, (d100_roll,))["language_dialect"]
            if language not in languages:
                languages.append(language)
                new_languages_learned += 1
    return languages


def get_starting_armour(class_id: int) -> Dict[str, Any]:
    """Get starting armour by class.
    The SQL should always return one and only one result.
    """
    sql = """
        SELECT a.*
          FROM starting_armour s
          JOIN t074_armour a
            ON s.armour_id = a.armour_id
         WHERE s.class_id = ?
    """
    armour = execute_query_one(sql, (class_id,))
    return armour


def get_starting_shield(class_id: int) -> Optional[Dict[str, Any]]:
    """Get starting shield by class.
    SQL should return one or zero results.
    """
    sql = """
        SELECT ts.*
          FROM starting_shield ss
          JOIN t075_shields ts
            ON ss.shield_id = ts.shield_id
         WHERE ss.class_id = ?
    """
    shield = execute_query_one(sql, (class_id,))
    return shield


def get_starting_weapons_melee(class_id: int) -> List[Dict[str, Any]]:
    """Get starting melee weapons by class."""
    sql = """
        SELECT w.*
             , sw.qty
          FROM starting_weapons_melee sw
          JOIN t076_melee_weapons w
            ON sw.weapon_id = w.weapon_id
         WHERE sw.class_id = ?;
    """
    melee_weapons = execute_query_all(sql, (class_id,))
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
    sql = """
        SELECT w.*
             , sw.qty
             , sw.ammunition
          FROM starting_weapons_missile sw
          JOIN t077_missile_weapons w
            ON sw.weapon_id = w.weapon_id
         WHERE sw.class_id = ?;
    """
    missile_weapons = execute_query_all(sql, (class_id,))
    for mw in missile_weapons:
        mw["hurled"] = bool(mw["hurled"])
        mw["launched"] = bool(mw["launched"])
        mw["missile_atk"] = 0
        mw["dmg_adj"] = 0
        mw["mastery"] = False
    return missile_weapons


def get_unskilled_weapon_penalty(class_id: int) -> int:
    """Get penalty when using a weapon not in the favoured list."""
    sql = """
        SELECT attack_penalty
          FROM t134_unskilled_weapon_attack_penalty
         WHERE class_id = ?;
    """
    unskilled_penalty: int = execute_query_one(sql, (class_id,))["attack_penalty"]
    return unskilled_penalty


def get_favoured_weapons(class_id: int) -> Dict[str, Any]:
    """Get list of favoured weapons for a given class_id."""
    # get favoured melee weapons
    melee_sql = """
        SELECT tmw.*
          FROM class_favoured_weapons_melee cfwm
          JOIN t076_melee_weapons tmw
            ON cfwm.weapon_id = tmw.weapon_id
         WHERE cfwm.class_id = ?
        ORDER BY tmw.weapon_id;
    """
    fav_wpns_melee: List[Dict[str, Any]] = execute_query_all(melee_sql, (class_id,))
    # get favoured missile weapons
    missile_sql = """
        SELECT tmw.*
          FROM class_favoured_weapons_missile cfwm
          JOIN t077_missile_weapons tmw
            ON cfwm.weapon_id = tmw.weapon_id
         WHERE cfwm.class_id = ?
        ORDER BY tmw.weapon_id;
    """
    fav_wpns_missile: List[Dict[str, Any]] = execute_query_all(missile_sql, (class_id,))
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
    sql = """
        SELECT item
          FROM starting_gear
         WHERE class_id = ?;
    """
    equipment = [x["item"] for x in execute_query_all(sql, (class_id,))]
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
    if atk_prog_idx >= len(atk_progression):
        raise ValueError(f"Cannot progress attack rate '{atk_rate}' any further.")
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
    if class_id not in VALID_CLASS_IDS:
        raise ValueError(f"Invalid class_id: {class_id}")
    if level not in VALID_LEVELS:
        raise ValueError(f"Invalid value for level: {level}")
    if dx_score not in VALID_ABILITY_SCORES:
        raise ValueError(f"Invalid value for dx_score: {dx_score}")
    if in_score not in VALID_ABILITY_SCORES:
        raise ValueError(f"Invalid value for in_score: {in_score}")
    if ws_score not in VALID_ABILITY_SCORES:
        raise ValueError(f"Invalid value for ws_score: {ws_score}")

    # get the skills for this class
    class_thief_abilities_sql = """
        SELECT thief_skill
        FROM class_thief_abilities
        WHERE class_id = ?;
    """
    skills_list = execute_query_all(class_thief_abilities_sql, (class_id,))
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
        thief_abilities_sql = f"""
            SELECT {sk['thief_skill']}
            FROM t016_thief_abilities
            WHERE level = ?;
        """
        skill_roll = execute_query_one(thief_abilities_sql, (level,))[sk["thief_skill"]]
        sk.update({"skill_roll": skill_roll})

    # apply bonuses (if any)
    for sk in skills_list:
        thief_ability_bonuses_sql = """
            SELECT stat
            FROM thief_ability_bonuses
            WHERE thief_skill = ?;
        """
        stat = execute_query_one(
            thief_ability_bonuses_sql,
            (sk["thief_skill"],),
        )["stat"]
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
    sql = """
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
    """
    turn_undead_matrix = execute_query_one(sql, (ta,))
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
    sql = "SELECT school_code FROM classes WHERE class_id = ?;"
    school_code: Optional[str] = execute_query_one(sql, (class_id,))["school_code"]
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
    assert school in VALID_SCHOOLS
    assert spell_level in VALID_SPELL_LEVELS
    assert d100_roll in range(1, 101)
    sql = """
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
    """
    result = execute_query_one(sql, (school, spell_level, d100_roll))
    if result["reversible"] is not None:
        result["reversible"] = bool(result["reversible"])
    return result


def get_spells(class_id: int, level: int, ca: int) -> Optional[Dict[str, Any]]:
    """Return the list of spells known for the character."""
    if ca == 0:
        return None
    schools = get_caster_schools(class_id)
    spells: Dict[str, Any] = {}
    for school in schools:
        spells[school] = {}
        sql = """
            SELECT *
              FROM class_spells_by_level
             WHERE class_id = ?
               AND level = ?
               AND school = ?;
        """
        class_spells = execute_query_one(sql, (class_id, level, school))
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
                if spells[school].get("spells_per_day", {}).get(lvl_key, 0) > 0:
                    spells[school]["spells_per_day"][lvl_key] += 1
        elif school == "run":
            # no bonus for runegravers
            continue
        # else:
        #     raise ValueError(f"Invalid value for school: {school}")
    return spells


def get_class_abilities(class_id: int, level: int) -> List[Dict[str, Any]]:
    """Get class abilities from class abilities table."""
    sql = """
        SELECT *
          FROM class_abilities
         WHERE class_id = ?
           AND level <= ?
        ORDER BY level, ability_title;
    """
    class_abilities = execute_query_all(sql, (class_id, level))
    return class_abilities


def get_random_familiar() -> str:
    """Roll 2d8 to get a random familiar."""
    roll = roll_dice(2, 8)
    sql = """
        SELECT animal
          FROM t010_familiars
         WHERE roll_2d8 = ?;
    """
    animal: str = execute_query_one(sql, (roll,))["animal"]
    return animal


def get_priest_abilities(deity_id: int, level: int) -> List[Dict[str, Any]]:
    """Get priest Specialized Faith abilities."""
    sql = """
        SELECT *
          FROM t047_priest_abilities
         WHERE deity_id = ?
           AND level <= ?
        ORDER BY level;
    """
    priest_abilities = execute_query_all(sql, (deity_id, level))
    return priest_abilities


def get_secondary_skill() -> str:
    roll = roll_dice(1, 60)
    sql = """
        SELECT *
          FROM t072_secondary_skills
         WHERE id = ?;
    """
    secondary_skill: str = execute_query_one(sql, (roll,))["skill_name"]
    return secondary_skill
