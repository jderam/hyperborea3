from typing import Dict

VALID_ABILITIES = ["st", "dx", "cn", "in", "ws", "ch"]
VALID_ABILITY_SCORES = list(range(3, 19))
VALID_AC_TYPES = ["ascending", "descending"]
VALID_ALIGMENTS_SHORT = ["CE", "CG", "LE", "LG", "N"]
VALID_CA = list(range(13))
VALID_CLASS_ID_MAP = {
    1: "Fighter",
    2: "Magician",
    3: "Cleric",
    4: "Thief",
    5: "Barbarian",
    6: "Berserker",
    7: "Cataphract",
    8: "Huntsman",
    9: "Paladin",
    10: "Ranger",
    11: "Warlock",
    12: "Cryomancer",
    13: "Illusionist",
    14: "Necromancer",
    15: "Pyromancer",
    16: "Witch",
    17: "Druid",
    18: "Monk",
    19: "Priest",
    20: "Runegraver",
    21: "Shaman",
    22: "Assassin",
    23: "Bard",
    24: "Legerdemainist",
    25: "Purloiner",
    26: "Scout",
    27: "Fell Paladin",
    28: "Ice Lord",
    29: "Fire Lord",
    30: "Death Soldier",
    31: "Mountebank",
    32: "Fire Thief",
    33: "Ice Thief",
}
VALID_CLASS_IDS = list(range(1, 34))
VALID_CLASS_THIEF_ABILITIES = {
    4: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
        "read_scrolls",
    ],
    5: [
        "climb",
        "move_silently",
    ],
    6: [
        "climb",
    ],
    8: [
        "climb",
        "hide",
        "manipulate_traps",
        "move_silently",
    ],
    10: [
        "climb",
        "discern_noise",
        "hide",
        "move_silently",
    ],
    18: [
        "climb",
        "discern_noise",
        "hide",
        "move_silently",
    ],
    22: [
        "climb",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
    ],
    23: [
        "decipher_script",
        "discern_noise",
        "hide",
        "move_silently",
    ],
    24: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
    ],
    25: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
    ],
    26: [
        "climb",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
    ],
    31: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
    ],
    32: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
    ],
    33: [
        "climb",
        "decipher_script",
        "discern_noise",
        "hide",
        "manipulate_traps",
        "move_silently",
        "open_locks",
        "pick_pockets",
    ],
}
VALID_COMPLEXIONS = [
    "Albino",
    "Bronzed",
    "Coppery",
    "Dark brown",
    "Dusky",
    "Ebony",
    "Fair",
    "Glaucous",
    "Jaundiced",
    "Light brown",
    "Medium brown",
    "Milky white",
    "Olive",
    "Ruddy",
    "Tan",
]
VALID_DEITIES = [
    "Apollo",
    "Artemis",
    "Aurorus",
    "Azathoth",
    "Boetzu",
    "Boreas",
    "Helios",
    "Kraken",
    "Kthulhu",
    "Krimmr",
    "Lunaqqua",
    "Mordezzan",
    "Raven",
    "Rel",
    "Thaumagorga",
    "Tlakk-Nakka",
    "Ullr",
    "Xathoqqua",
    "Yig",
    "Yikkorth",
    "Ymir",
    "Yoon'Deh",
    "Ythaqqa",
    "Yug",
]
VALID_DENOMINATIONS = ["pp", "gp", "ep", "sp", "cp"]
VALID_DICE_METHODS = [1, 2, 3, 4, 5, 6]
VALID_EYE_COLOURS = [
    "Amber, Dark",
    "Amber, Light",
    "Black",
    "Blue, Dark",
    "Blue, Light",
    "Brown, Dark",
    "Brown, Light",
    "Green, Dark",
    "Green, Emerald",
    "Green, Light",
    "Grey, Dark",
    "Grey, Light",
    "Hazel, Dark",
    "Hazel, Light",
    "Violet, Dark",
    "Violet, Light",
    "Yellow, Dark",
    "Yellow, Light",
]
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
VALID_FAVOURED_WEAPONS = {
    1: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    2: {
        "any": False,
        "melee_wpns": [108, 126],
        "missile_wpns": [203, 216],
        "unskilled_penalty": -4,
    },
    3: {
        "any": False,
        "melee_wpns": [
            106,
            107,
            108,
            111,
            112,
            114,
            115,
            119,
            120,
            122,
            126,
            131,
            132,
            134,
            135,
            136,
            137,
            138,
            140,
            143,
        ],
        "missile_wpns": [205],
        "unskilled_penalty": -2,
    },
    4: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    5: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    6: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    7: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    8: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    9: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    10: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    11: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    12: {
        "any": False,
        "melee_wpns": [101, 108, 123, 126, 131],
        "missile_wpns": [203],
        "unskilled_penalty": -4,
    },
    13: {
        "any": False,
        "melee_wpns": [108, 126],
        "missile_wpns": [203, 216],
        "unskilled_penalty": -4,
    },
    14: {
        "any": False,
        "melee_wpns": [108, 126, 130, 143],
        "missile_wpns": [203, 216],
        "unskilled_penalty": -4,
    },
    15: {
        "any": False,
        "melee_wpns": [108, 110, 122, 126, 127, 128],
        "missile_wpns": [203],
        "unskilled_penalty": -4,
    },
    16: {
        "any": False,
        "melee_wpns": [108, 126, 143],
        "missile_wpns": [203, 208, 216],
        "unskilled_penalty": -4,
    },
    17: {
        "any": False,
        "melee_wpns": [
            106,
            107,
            108,
            110,
            122,
            126,
            127,
            128,
            130,
            131,
            132,
            134,
            140,
            142,
            143,
        ],
        "missile_wpns": [203, 205, 209, 211, 216],
        "unskilled_penalty": -2,
    },
    18: {
        "any": False,
        "melee_wpns": [
            x + 100
            for x in range(1, 44)
            if x not in [103, 116, 121, 125, 129, 133, 139]
        ],
        "missile_wpns": [x + 200 for x in range(1, 16)],
        "unskilled_penalty": -2,
    },
    19: {
        "any": False,
        "melee_wpns": [108, 126, 143],
        "missile_wpns": [203, 216],
        "unskilled_penalty": -4,
    },
    20: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    21: {
        "any": False,
        "melee_wpns": [101, 105, 106, 107, 108, 126, 131, 132, 140, 141, 142],
        "missile_wpns": [201, 202, 204, 208, 211, 216],
        "unskilled_penalty": -4,
    },
    22: {
        "any": False,
        "melee_wpns": [
            101,
            105,
            106,
            108,
            110,
            111,
            114,
            119,
            123,
            127,
            135,
            136,
            137,
            140,
            141,
        ],
        "missile_wpns": [203, 204, 208, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    23: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    24: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    25: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 205, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    26: {
        "any": False,
        "melee_wpns": [
            101,
            106,
            108,
            110,
            111,
            114,
            119,
            122,
            123,
            127,
            135,
            136,
            137,
            141,
        ],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    27: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    28: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    29: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    30: {
        "any": True,
        "melee_wpns": [x + 100 for x in range(1, 44)],
        "missile_wpns": [x + 200 for x in range(1, 17)],
        "unskilled_penalty": 0,
    },
    31: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    32: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
    33: {
        "any": False,
        "melee_wpns": [101, 106, 108, 110, 111, 114, 119, 123, 127, 135, 136, 137, 141],
        "missile_wpns": [203, 211, 214, 216],
        "unskilled_penalty": -2,
    },
}
VALID_GENDERS = ["Male", "Female", "Non-Binary"]
VALID_GP = range(2, 6)
VALID_HAIR_COLOURS = [
    "Auburn, Dark",
    "Auburn, Light",
    "Auburn, Medium",
    "Black",
    "Blond, Dark",
    "Blond, Light",
    "Blond, Medium",
    "Blue-Black",
    "Brown, Dark",
    "Brown, Light",
    "Brown, Medium",
    "Golden, Pale",
    "Golden, Rich",
    "Red, Dark",
    "Red, Light",
    "Red, Medium",
    "Red-Orange, Dark",
    "Red-Orange, Light",
    "Red-Orange, Medium",
    "Silvery-White",
    "White",
]
VALID_HD_QTY = list(range(1, 10))
VALID_HD_SIZE = [4, 6, 8, 10, 12]
VALID_HD_PLUS = [1, 2, 3, 4, 6, 8, 9, 12]
VALID_LANGUAGES = [
    "Common",
    "Berber",
    "Esquimaux (Coastal dialect)",
    "Esquimaux (Tundra dialect)",
    "Esquimaux-Ixian (pidgin)",
    "Hellenic (Amazon dialect)",
    "Hellenic (Atlantean dialect)",
    "Hellenic (Greek dialect)",
    "Hellenic (Hyperborean dialect)",
    "Hellenic (Kimmerian dialect)",
    "Keltic (Goidelic dialect)",
    "Keltic (Pictish dialect)",
    "Latin",
    "Lemurian",
    "Muat",
    "Old Norse (Anglo-Saxon dialect)",
    "Old Norse (Viking dialect)",
    "Oonat",
    "Thracian (Ixian dialect)",
    "Thracian (Kimmerian dialect)",
    "Tlingit",
    "Uralic (Lapp dialect)",
    "Uralic (Yakut dialect)",
]
VALID_LEVELS = list(range(1, 13))
VALID_MONSTER_IDS = [1, 2, 3]
VALID_RACE_IDS = list(range(1, 25))
VALID_RACES_BY_ID: Dict[int, str] = {
    1: "Common",
    2: "Amazon",
    3: "Atlantean",
    4: "Esquimaux",
    5: "Hyperborean",
    6: "Ixian",
    7: "Kelt",
    8: "Kimmerian",
    9: "Kimmeri-Kelt",
    10: "Pict",
    11: "Pict (Half-Blood)",
    12: "Viking",
    13: "Anglo-Saxon",
    14: "Carolingian Frank",
    15: "Esquimaux-Ixian",
    16: "Greek",
    17: "Lapp",
    18: "Lemurian",
    19: "Moor",
    20: "Mu",
    21: "Oon",
    22: "Roman",
    23: "Tlingit",
    24: "Yakut",
}
VALID_SAVES = list(range(11, 17))
VALID_SCHOOLS = ["clr", "cry", "drd", "ill", "mag", "nec", "pyr", "run", "wch"]
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
VALID_SECONDARY_SKILLS = [
    "animal trainer",
    "armourer",
    "atilliator",
    "baker/cook",
    "barber/dentist",
    "bar-/innkeeper",
    "black-/coin-/metalsmith",
    "boat-/shipwright",
    "bookbinder",
    "bowyer/fletcher",
    "brewer/vintner",
    "butcher/salter",
    "carpenter",
    "cart-/wainwright",
    "chandler",
    "charcoaler/peatman",
    "clothier/dyer",
    "cobbler/shoemaker",
    "cooper",
    "engineer",
    "farmer",
    "fisherman/whaler",
    "fuller",
    "furrier/skinner",
    "gaffer/glazier",
    "gaoler/turnkey",
    "gardener",
    "gem cutter/jeweller",
    "grocer",
    "guard/watchman",
    "herdsman/pack handler",
    "hunter/trapper",
    "labourer/yardman",
    "leatherworker/saddler/tanner",
    "limner/painter/sculptor",
    "linkboy/messenger",
    "locksmith",
    "logger/woodcutter",
    "mason/slater",
    "merchant/monger",
    "miller",
    "miner",
    "minstrel/musician",
    "mortician",
    "navigator",
    "potter",
    "riverman/waterman",
    "roofer/thatcher",
    "roper",
    "sailor/seaman",
    "scribe/scrivener",
    "soldier/mercenary",
    "stabler",
    "stevedore",
    "sword-/weaponsmith",
    "tailor/weaver",
    "teamster",
    "tinker",
    "wheelwright",
    "wire drawer",
]
VALID_SPELL_IDS = list(range(1, 456))
VALID_SPELL_LEVELS = list(range(1, 7))
VALID_SQL_TABLES = [
    "alignment",
    "class_abilities",
    "class_alignment",
    "class_attr_req",
    "class_favoured_weapons_melee",
    "class_favoured_weapons_missile",
    "class_level",
    "class_prime_attr",
    "class_spells_by_level",
    "class_thief_abilities",
    "classes",
    "deities",
    "monsters",
    "runes",
    "spells",
    "starting_armour",
    "starting_gear",
    "starting_shield",
    "starting_weapons_melee",
    "starting_weapons_missile",
    "t001_strength",
    "t002_dexterity",
    "t003_constitution",
    "t004_intelligence",
    "t005_wisdom",
    "t006_charisma",
    "t010_familiars",
    "t013_turn_undead",
    "t016_thief_abilities",
    "t047_priest_abilities",
    "t066_primary_races",
    "t067_ancillary_races",
    "t069_height_and_weight",
    "t070a_eye_colour",
    "t070b_hair_colour",
    "t070c_complexion",
    "t071_languages",
    "t072_secondary_skills",
    "t074_armour",
    "t075_shields",
    "t076_melee_weapons",
    "t077_missile_weapons",
    "t093_mag_spell_list",
    "t094_cry_spell_list",
    "t095_ill_spell_list",
    "t096_nec_spell_list",
    "t097_pyr_spell_list",
    "t098_wch_spell_list",
    "t099_clr_spell_list",
    "t100_drd_spell_list",
    "t134_unskilled_weapon_attack_penalty",
    "t150_common_name_elements",
    "t152_amazon_female_names",
    "t153_amazon_male_names",
    "t155_anglosaxon_female_names",
    "t156_anglosaxon_male_names",
    "t157_atlantean_female_names",
    "t158_atlantean_male_names",
    "t159_atlantean_clan_names",
    "t160_carolingian_frankish_female_names",
    "t161_carolingian_frankish_male_names",
    "t162_esquimaux_names",
    "t163_greek_female_names",
    "t164_greek_male_names",
    "t165_hyperborean_name_elements",
    "t167_hyperborean_family_names",
    "t168_ixian_female_names",
    "t169_ixian_male_names",
    "t170_keltic_female_names",
    "t171_keltic_male_names",
    "t172_kimmerian_female_names",
    "t173_kimmerian_male_names",
    "t174_kimmerian_krimmean_female_names",
    "t175_kimmerian_krimmean_male_names",
    "t176_lapp_female_names",
    "t177_lapp_male_names",
    "t179_lemurian_family_names",
    "t180_lemurian_female_names",
    "t181_lemurian_male_names",
    "t182_moorish_female_names",
    "t183_moorish_male_names",
    "t184_mu_names",
    "t185_pictish_female_names",
    "t186_pictish_male_names",
    "t188_roman_personal_names",
    "t189_roman_family_names",
    "t190_roman_cognomen",
    "t191_tlingit_names",
    "t192_viking_female_names",
    "t193_viking_male_names",
    "t195_yakut_female_names",
    "t196_yakut_male_names",
    "t197_epithets",
    "thief_ability_bonuses",
    "weapon_annotation_lkp",
]
VALID_SQL_VIEWS = [
    "v_clr_spell_list",
    "v_complete_spell_list",
    "v_cry_spell_list",
    "v_drd_spell_list",
    "v_ill_spell_list",
    "v_mag_spell_list",
    "v_nec_spell_list",
    "v_pyr_spell_list",
    "v_race_lkp",
    "v_wch_spell_list",
]
VALID_SUBCLASS_PARAMS = [0, 1, 2]
VALID_TA = list(range(13))
VALID_UNSKILLED_PENALTIES = {
    1: 0,
    2: -4,
    3: -2,
    4: -2,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: -4,
    13: -4,
    14: -4,
    15: -4,
    16: -4,
    17: -2,
    18: -2,
    19: -4,
    20: 0,
    21: -4,
    22: -2,
    23: 0,
    24: -2,
    25: -2,
    26: -2,
    27: 0,
    28: 0,
    29: 0,
    30: 0,
    31: -2,
    32: -2,
    33: -2,
}
