import logging
import random
import re
from typing import Callable, Dict, Union

from hyperborea3.db import (
    execute_query_one,
    table_exists,
)
from hyperborea3.chargen import roll_dice
from hyperborea3.valid_data import VALID_RACES_BY_ID

logger = logging.getLogger(__name__)


def get_name_sql(table_name: str) -> str:
    if table_exists(table_name):
        return f"""
            SELECT name
            FROM {table_name}
            WHERE id = ?
        """
    else:
        raise NameError(f"No table named '{table_name}' found in database.")


def process_gender(gender: str) -> str:
    logger.debug(f"input {gender = }")
    gender = gender.title()
    if gender not in ["Female", "Male"]:
        gender = random.choice(["Female", "Male"])
        logger.debug(f"randomized {gender = }")
    return gender


def limit_repeating_chars(string: str) -> str:
    return re.sub(r"(.)\1{2,}", r"\1\1", string)


def generate_epithet() -> str:
    sql = get_name_sql("t197_epithets")
    roll = roll_dice(1, 36)
    epithet = execute_query_one(sql, (roll,)).get("name")
    return f"“{epithet}”"


def generate_common_name(gender: str) -> str:
    gender = process_gender(gender)

    def _common_name():
        num_elements = random.choice([1, 2])
        name_elements = []
        query_sql = """
            SELECT name_element
            FROM t150_common_name_elements
            WHERE id = ?
        """
        for _ in range(num_elements):
            roll = roll_dice(1, 100)
            result = execute_query_one(query_sql, (roll,))["name_element"]
            name_elements.append(result)
        logger.debug(f"{name_elements = }")
        raw_name = ("").join(name_elements)
        cleaned_name = limit_repeating_chars(raw_name).title()
        return cleaned_name

    first_name = _common_name()
    if gender == "Female":
        female_suffixes = ["a", "esta", "ia"]
        first_name += random.choice(female_suffixes)
    last_name = _common_name()
    last_name += random.choice(["os", "tos", "tose"])
    return f"{first_name} {last_name}"


def generate_amazon_name(gender: str) -> str:
    gender = process_gender(gender)
    female_sql = get_name_sql("t152_amazon_female_names")
    roll = roll_dice(1, 50)
    matronymic = execute_query_one(female_sql, (roll,))["name"]
    matronymic_suffix_map = [
        (r"dra$", "doros"),
        (r"e$", "edoros"),
        (r"ia$", "idoros"),
        (r"o$", "odoros"),
    ]
    for pattern, replacement in matronymic_suffix_map:
        matronymic = re.sub(pattern, replacement, matronymic)
    if gender == "Male":
        male_sql = get_name_sql("t153_amazon_male_names")
        roll = roll_dice(1, 20)
        first_name = execute_query_one(male_sql, (roll,)).get("name")
    else:
        roll = roll_dice(1, 50)
        first_name = execute_query_one(female_sql, (roll,)).get("name")
    return f"{first_name} {matronymic}"


def generate_anglosaxon_name(gender: str) -> str:
    gender = process_gender(gender)
    if gender == "Female":
        sql = get_name_sql("t155_anglosaxon_female_names")
    else:
        sql = get_name_sql("t156_anglosaxon_male_names")
    roll = roll_dice(1, 40)
    first_name = execute_query_one(sql, (roll,))["name"]
    # 40% chance of epithet (this was an arbitrary choice)
    if random.random() < 0.4:
        epithet = generate_epithet()
        name = f"{first_name} {epithet}"
    else:
        name = first_name
    return name


def generate_atlantean_name(gender: str) -> str:
    gender = process_gender(gender)
    table_lookup = {
        "Female": "t157_atlantean_female_names",
        "Male": "t158_atlantean_male_names",
        "Clan": "t159_atlantean_clan_names",
    }
    die_size = {
        "Female": 40,
        "Male": 60,
        "Clan": 12,
    }
    first_name_table = table_lookup[gender]
    first_name_roll = roll_dice(1, die_size[gender])
    first_name = execute_query_one(
        get_name_sql(first_name_table), (first_name_roll,)
    ).get("name")
    clan_name_table = table_lookup["Clan"]
    clan_name_roll = die_size["Clan"]
    clan_name = execute_query_one(get_name_sql(clan_name_table), (clan_name_roll,)).get(
        "name"
    )
    return f"{first_name} {clan_name}"


def generate_carolingian_frankish_name(gender: str) -> str:
    gender = process_gender(gender)
    table_lookup: Dict[str, Dict[str, Union[str, int]]] = {
        "Female": {
            "table": "t160_carolingian_frankish_female_names",
            "die_size": 25,
        },
        "Male": {
            "table": "t161_carolingian_frankish_male_names",
            "die_size": 50,
        },
    }
    sql = get_name_sql(table_lookup[gender]["table"])  # type: ignore
    roll = roll_dice(1, table_lookup[gender]["die_size"])  # type: ignore
    first_name = execute_query_one(sql, (roll,))["name"]
    # 50% chance of epithet (this was an arbitrary choice)
    if random.random() < 0.5:
        epithet = generate_epithet()
        name = f"{first_name} {epithet}"
    else:
        name = first_name
    return name


def generate_esquimaux_name(gender: str) -> str:
    sql = get_name_sql("t162_esquimaux_names")
    roll = roll_dice(1, 50)
    name: str = execute_query_one(sql, (roll,))["name"]
    return name


def generate_esquimaux_ixian_name(gender: str) -> str:
    # get an Esquimaux name, and sometimes shorten it to just the first syllable
    name = generate_esquimaux_name(gender)
    name_map = {
        # Aguta
        "Akiak": "Ak",
        "Arjalinerk": "Arj",
        # Arrluk
        # Assiminik
        "Aukaneck": "Auk",
        "Chulyin": "Chu",
        "Cikuq": "Cik",
        # Iluq
        # Issumatar
        "Kakortok": "Kak",
        "Karpok": "Kar",
        # Kesuk
        # Kinaktok
        # Kinapak
        "Krernertok": "Krer",
        "Kussuyok": "Kuss",
        "Maguyuk": "Mag",
        # Maniitok
        # Nauja
        "Ningakpok": "Ning",
        "Nukilik": "Nuk",
        # Olikpok
        "Piktaungitok": "Pik",
        "Pukulria": "Puk",
        "Qigiq": "Qig",
        "Saghani": "Sag",
        "Salaksartok": "Salak",
        "Sangilak": "Sang",
        "Saomik": "Sao",
        "Shila": "Shi",
        "Siku": "Sik",
        # Sirmiq
        "Sitiyok": "Sit",
        # Sos
        # Suka
        "Taliriktug": "Tal",
        "Taqukaq": "Taq",
        "Tartok": "Tar",
        "Tiglikte": "Tig",
        "Tikaani": "Tik",
        "Tonrar": "Ton",
        "Tornuaq": "Torn",
        # Tulugaq
        # Tulukaruk
        # Tuluwaq
        "Tungulria": "Tung",
        # Tuwawi
        # Ulva
        "Yakone": "Yak",
    }
    short_name = name_map.get(name)
    if short_name:
        # 70% chance to shorten
        if random.random() < 0.7:
            name = short_name
    return name


def generate_greek_name(gender: str) -> str:
    gender = process_gender(gender)
    male_sql = get_name_sql("t164_greek_male_names")
    roll = roll_dice(1, 50)
    patronymic = execute_query_one(male_sql, (roll,))["name"]
    roll = roll_dice(1, 50)
    if gender == "Female":
        female_sql = get_name_sql("t163_greek_female_names")
        first_name = execute_query_one(female_sql, (roll,))["name"]
    else:
        first_name = execute_query_one(male_sql, (roll,))["name"]
    return f"{first_name} {patronymic}"


def generate_hyperborean_name(gender: str) -> str:
    gender = process_gender(gender)
    element_sql = get_name_sql("t165_hyperborean_name_elements")
    roll = roll_dice(1, 60)
    element1 = execute_query_one(element_sql, (roll,))["name"]
    roll = roll_dice(1, 60)
    element2 = execute_query_one(element_sql, (roll,))["name"]
    connecting_vowel = random.choice(["a", "i", "o", "u"])
    if gender == "Female":
        first_name = f"Sha{element1}{connecting_vowel}{element2}".title()
    else:
        first_name = f"{element1}{connecting_vowel}{element2}".title()
    family_sql = get_name_sql("t167_hyperborean_family_names")
    roll = roll_dice(1, 16)
    family_name = execute_query_one(family_sql, (roll,))["name"]
    return f"{first_name} {family_name}"


def generate_ixian_name(gender: str) -> str:
    gender = process_gender(gender)
    male_sql = get_name_sql("t169_ixian_male_names")
    roll = roll_dice(1, 50)
    patronymic = execute_query_one(male_sql, (roll,))["name"]
    if gender == "Female":
        married = random.choice([True, False])
        patronymic_prefix = "gunê" if married else "thugatêr"
        female_sql = get_name_sql("t168_ixian_female_names")
        roll = roll_dice(1, 32)
        first_name = execute_query_one(female_sql, (roll,))["name"]
        full_name = f"{first_name} {patronymic_prefix} {patronymic}"
    else:
        roll = roll_dice(1, 50)
        first_name = execute_query_one(male_sql, (roll,))["name"]
        full_name = f"{first_name} {patronymic}"
    return full_name


def generate_keltic_name(gender: str) -> str:
    gender = process_gender(gender)
    male_sql = get_name_sql("t171_keltic_male_names")
    if gender == "Female":
        female_sql = get_name_sql("t170_keltic_female_names")
        roll = roll_dice(1, 50)
        first_name = execute_query_one(female_sql, (roll,))["name"]
        patronymic_joiner = "Inghean"
    else:
        roll = roll_dice(1, 50)
        first_name = execute_query_one(male_sql, (roll,))["name"]
        patronymic_joiner = "Macc"
    if random.random() < 0.8:
        roll = roll_dice(1, 50)
        patronymic = execute_query_one(male_sql, (roll,))["name"]
        full_name = f"{first_name} {patronymic_joiner} {patronymic}"
    else:
        full_name = first_name
    return full_name


def generate_kimmerian_name(gender: str) -> str:
    gender = process_gender(gender)
    subterranean_krimmean = random.choice([False, True])
    table_map = {
        "Female": {
            False: "t172_kimmerian_female_names",
            True: "t174_kimmerian_krimmean_female_names",
        },
        "Male": {
            False: "t173_kimmerian_male_names",
            True: "t175_kimmerian_krimmean_male_names",
        },
    }
    name_sql = get_name_sql(table_map[gender][subterranean_krimmean])
    die_size = 20 if subterranean_krimmean else 40
    roll = roll_dice(1, die_size)
    name = execute_query_one(name_sql, (roll,))["name"]
    epithet = generate_epithet()
    return f"{name} {epithet}"


def generate_kemmeri_kelt_name(gender: str) -> str:
    if random.random() < 0.8:
        name = generate_keltic_name(gender)
    else:
        name = generate_kimmerian_name(gender)
    return name


def generate_lapp_name(gender: str) -> str:
    gender = process_gender(gender)
    clan_name = random.choice(
        [
            "Bear",
            "Elk",
            "Fox",
            "Wolf",
        ]
    )
    if gender == "Female":
        sql = get_name_sql("t176_lapp_female_names")
    else:
        sql = get_name_sql("t177_lapp_male_names")
    roll = roll_dice(1, 20)
    first_name = execute_query_one(sql, (roll,))["name"]
    full_name = f"{first_name} of the {clan_name} Clan"
    return full_name


def generate_lemurian_name(gender: str) -> str:
    gender = process_gender(gender)
    if gender == "Female":
        sql = get_name_sql("t180_lemurian_female_names")
    else:
        sql = get_name_sql("t181_lemurian_male_names")
    roll = roll_dice(1, 80)
    personal_name = execute_query_one(sql, (roll,))["name"]
    # criminals/outcasts do not have a family name (5% chance)
    criminal = random.random() < 0.05
    if not criminal:
        family_sql = get_name_sql("t179_lemurian_family_names")
        roll = roll_dice(1, 60)
        family_name = execute_query_one(family_sql, (roll,))["name"]
        full_name = f"{family_name} {personal_name}"
    else:
        full_name = personal_name
    return full_name


def generate_moorish_name(gender: str) -> str:
    gender = process_gender(gender)
    male_sql = get_name_sql("t183_moorish_male_names")
    roll = roll_dice(1, 30)
    patronymic = execute_query_one(male_sql, (roll,))["name"]
    if gender == "Female":
        female_sql = get_name_sql("t182_moorish_female_names")
        roll = roll_dice(1, 25)
        first_name = execute_query_one(female_sql, (roll,))["name"]
        joiner = "ult"
    else:
        roll = roll_dice(1, 30)
        first_name = execute_query_one(male_sql, (roll,))["name"]
        joiner = "ag"
    full_name = f"{first_name} {joiner}-{patronymic}"
    return full_name


def generate_mu_name(gender: str) -> str:
    gender = process_gender(gender)
    sql = get_name_sql("t184_mu_names")
    roll = roll_dice(1, 60)
    name: str = execute_query_one(sql, (roll,))["name"]
    if gender == "Female":
        unmarried = True if random.random() < 0.65 else False
        if unmarried:
            if name.endswith("a"):
                name += "sha"
            else:
                name += "asha"
    return name


def generate_oon_name(gender: str) -> str:
    number = random.randint(1, 999_999_999)
    name = str(number).zfill(9)
    return name


def generate_pictish_name(gender: str) -> str:
    gender = process_gender(gender)
    if gender == "Female":
        sql = get_name_sql("t185_pictish_female_names")
        roll = roll_dice(1, 20)
        name: str = execute_query_one(sql, (roll,))["name"]
    else:
        sql = get_name_sql("t186_pictish_male_names")
        roll = roll_dice(1, 40)
        first_name = execute_query_one(sql, (roll,))["name"]
        if random.random() < 0.6:
            roll = roll_dice(1, 40)
            patronymic_base = execute_query_one(sql, (roll,))["name"]
            if patronymic_base.endswith("ex"):
                patronymic = re.sub(r"ex$", "egis", patronymic_base)
            elif patronymic_base.endswith("is"):
                patronymic = patronymic_base
            elif patronymic_base.endswith("ix"):
                patronymic = re.sub(r"ix$", "igis", patronymic_base)
            elif patronymic_base.endswith("os"):
                patronymic = re.sub(r"os$", "i", patronymic_base)
            elif patronymic_base == "Segovax":
                patronymic = "Segovegis"
            else:
                raise ValueError(
                    f"No patronymic modification rules for '{patronymic_base}'."
                )
            name = f"{first_name} nepos {patronymic}"
        else:
            name = first_name
    return name


def generate_half_blood_pict_name(gender: str) -> str:
    if random.random() < 0.95:
        name = generate_tlingit_name(gender)
    else:
        name = generate_pictish_name(gender)
    return name


def generate_roman_name(gender: str) -> str:
    gender = process_gender(gender)
    # TODO: Consider variants with only one of the name parts.
    # See Player's Manual pages 302-303
    praenomen_sql = f"""
        SELECT {gender.lower()}_name
        FROM t188_roman_personal_names
        WHERE id = ?
    """
    praenomen_roll = roll_dice(1, 25)
    praenomen = execute_query_one(praenomen_sql, (praenomen_roll,))[
        f"{gender.lower()}_name"
    ]
    nomen_sql = f"""
        SELECT {gender.lower()}_name
        FROM t189_roman_family_names
        WHERE id = ?
    """
    nomen_roll = roll_dice(1, 25)
    nomen = execute_query_one(nomen_sql, (nomen_roll,))[f"{gender.lower()}_name"]
    cognomen_sql = f"""
        SELECT {gender.lower()}_name
        FROM t190_roman_cognomen
        WHERE id = ?
    """
    cognomen_roll = roll_dice(1, 50)
    cognomen = execute_query_one(cognomen_sql, (cognomen_roll,))[
        f"{gender.lower()}_name"
    ]
    name = f"{praenomen} {nomen} {cognomen}"
    return name


def generate_tlingit_name(gender: str) -> str:
    gender = process_gender(gender)
    moiety = random.choice(["G̱ooch", "Yéil"])
    sql = get_name_sql("t191_tlingit_names")
    roll = roll_dice(1, 40)
    personal_name = execute_query_one(sql, (roll,))["name"]
    return f"{personal_name} {moiety}"


def generate_viking_name(gender: str) -> str:
    gender = process_gender(gender)
    female_sql = get_name_sql("t192_viking_female_names")
    male_sql = get_name_sql("t193_viking_male_names")
    roll = roll_dice(1, 100)
    if gender == "Female":
        first_name = execute_query_one(female_sql, (roll,))["name"]
    else:
        first_name = execute_query_one(male_sql, (roll,))["name"]
    # outcast Viking from the Isles of Thur
    outcast = random.random() < 0.1
    if outcast:
        first_name = re.sub(r"^Ull", "Thor", first_name)
    use_epithet = random.random() < 0.25
    if use_epithet:
        epithet = generate_epithet()
        full_name = f"{first_name} {epithet}"
    else:
        roll = roll_dice(1, 100)
        patronymic_base = execute_query_one(male_sql, (roll,))["name"]
        if patronymic_base.endswith("björn"):
            patronymic_mod = re.sub(r"björn$", "biarnar", patronymic_base)
        elif patronymic_base.endswith("dr"):
            patronymic_mod = re.sub(r"dr$", "ar", patronymic_base)
        elif patronymic_base.endswith("i"):
            patronymic_mod = re.sub(r"i$", "a", patronymic_base)
        elif patronymic_base.endswith("ir"):
            patronymic_mod = re.sub(r"ir$", "is", patronymic_base)
        elif patronymic_base.endswith("ll"):
            patronymic_mod = re.sub(r"ll$", "ls", patronymic_base)
        elif patronymic_base.endswith("nn"):
            patronymic_mod = re.sub(r"nn$", "ns", patronymic_base)
        elif patronymic_base.endswith("rr"):
            patronymic_mod = re.sub(r"rr$", "rs", patronymic_base)
        elif patronymic_base.endswith("r"):
            patronymic_mod = re.sub(r"r$", "s", patronymic_base)
        # Viking patronymic names: "Björn", "Gedda", "Hákon", "Magnus"
        elif patronymic_base == "Björn":
            if gender == "Female":
                patronymic_mod = "Bjarnar"
            else:
                patronymic_mod = "Björns"
        elif patronymic_base == "Gedda":
            patronymic_mod = patronymic_base
        elif patronymic_base == "Hákon":
            patronymic_mod = "Hákonar"
        elif patronymic_base == "Magnus":
            if gender == "Female":
                patronymic_mod = "Magnús"
            else:
                patronymic_mod = patronymic_base
        else:
            raise ValueError(
                f"Can't map patronymic modification for '{patronymic_base}'"
            )
        patronymic_suffix = "dóttir" if gender == "Female" else "son"
        patronymic = f"{patronymic_mod}{patronymic_suffix}"
        full_name = f"{first_name} {patronymic}"
    return full_name


def generate_yakut_name(gender: str) -> str:
    gender = process_gender(gender)
    if gender == "Female":
        sql = get_name_sql("t195_yakut_female_names")
    else:
        sql = get_name_sql("t196_yakut_male_names")
    roll = roll_dice(1, 12)
    name: str = execute_query_one(sql, (roll,))["name"]
    return name


def generate_name(race_id: int, gender: str) -> str:
    logger.debug(f"input {race_id = }")
    if race_id == 0:
        # select a random race_id
        race_id = random.choice(list(VALID_RACES_BY_ID.keys()))
        logger.debug(f"random {race_id = }")
    function_map: Dict[int, Callable[[str], str]] = {
        1: generate_common_name,
        2: generate_amazon_name,
        3: generate_atlantean_name,
        4: generate_esquimaux_name,
        5: generate_hyperborean_name,
        6: generate_ixian_name,
        7: generate_keltic_name,
        8: generate_kimmerian_name,
        9: generate_kemmeri_kelt_name,
        10: generate_pictish_name,
        11: generate_half_blood_pict_name,
        12: generate_viking_name,
        13: generate_anglosaxon_name,
        14: generate_carolingian_frankish_name,
        15: generate_esquimaux_ixian_name,
        16: generate_greek_name,
        17: generate_lapp_name,
        18: generate_lemurian_name,
        19: generate_moorish_name,
        20: generate_mu_name,
        21: generate_oon_name,
        22: generate_roman_name,
        23: generate_tlingit_name,
        24: generate_yakut_name,
    }
    name = function_map[race_id](gender)
    return name


if __name__ == "__main__":
    for race_id, race_name in VALID_RACES_BY_ID.items():
        if race_id in range(25):
            print(f"""{race_name} name: {generate_name(race_id, "random")}""")
