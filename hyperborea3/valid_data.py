VALID_ABILITIES = ["st", "dx", "cn", "in", "ws", "ch"]
VALID_ABILITY_SCORES = list(range(3, 19))
VALID_AC_TYPES = ["ascending", "descending"]
VALID_ALIGMENTS_SHORT = ["CE", "CG", "LE", "LG", "N"]
VALID_CA = list(range(13))
VALID_CLASS_IDS = list(range(1, 34))
VALID_DENOMINATIONS = ["pp", "gp", "ep", "sp", "cp"]
VALID_DICE_METHODS = [1, 2, 3, 4, 5, 6]
VALID_FA = list(range(13))
VALID_FAMILIARS = [
    "Archæopteryx",
    "Ice Toad",
    "Falcon/Hawk",
    "Squirrel",
    "Hare",
    "Gull",
    "Owl",
    "Cat",
    "Rat",
    "Bat",
    "Raven",
    "Weasel",
    "Fox",
    "Viper",
    "Pegomastax",
]
VALID_GENDERS = ["Male", "Female", "Non-Binary"]
VALID_GP = range(2, 6)
VALID_LEVELS = list(range(1, 13))
VALID_RACE_IDS = list(range(1, 25))
VALID_SAVES = list(range(11, 17))
VALID_HD_QTY = list(range(1, 10))
VALID_HD_SIZE = [4, 6, 8, 10, 12]
VALID_HD_PLUS = [1, 2, 3, 4, 6, 8, 9, 12]
VALID_SCHOOLS = ["clr", "cry", "drd", "ill", "mag", "nec", "pyr", "run", "wch"]
VALID_SPELL_LEVELS = list(range(1, 7))
VALID_SUBCLASS_PARAMS = [0, 1, 2]
VALID_TA = list(range(13))

VALID_SCHOOLS_BY_CLASS_ID = {
    1: [],
    2: ["mag"],
    3: ["clr"],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: ["clr"],
    10: ["drd", "mag"],
    11: ["mag"],
    12: ["cry"],
    13: ["ill"],
    14: ["nec"],
    15: ["pyr"],
    16: ["wch"],
    17: ["drd"],
    18: [],
    19: ["clr"],
    20: ["run"],
    # 21: Shaman intentinally omitted as they have special rules
    22: [],
    23: ["drd", "ill"],
    24: ["mag"],
    25: ["clr"],
    26: [],
    27: ["clr"],
    28: ["cry"],
    29: ["pyr"],
    30: ["nec"],
    31: ["ill"],
    32: ["pyr"],
    33: ["cry"],
}
