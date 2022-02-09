# hyperborea-tools

An app for creating randomly-generated characters for the [Hyperborea](https://www.hyperborea.tv/) 3rd edition tabletop roleplaying game. 

## Installation

``` bash
python -m pip install hyperborea3
```

## Usage

By default, a random character will be generated with the following options:

* Abilities are rolled using dice method III
* Class is randomly selected, ensuring minimum ability requirements are met
* 0 experience points
* All subclasses are enabled
* The by-the-book descending Armour Class system is used

``` python
from pprint import pprint
from hyperborea3.player_character import PlayerCharacter

pc = PlayerCharacter()
pprint(pc.to_dict())
```

## Sample Output
``` python
{'ac': 3,
 'alignment': {'align_id': 4, 'long_name': 'Lawful Good', 'short_name': 'LG'},
 'armour': {'ac': 6,
            'armour_id': 5,
            'armour_type': 'Scale Mail',
            'cost': 50,
            'description': None,
            'dr': 1,
            'mv': 30,
            'weight': 25,
            'weight_class': 'Medium'},
 'attr': {'ch': {'max_henchmen': 8, 'react_adj': 1, 'score': 15, 'turn_adj': 1},
          'cn': {'feat': 8,
                 'hp_adj': 1,
                 'poison_adj': 0,
                 'score': 13,
                 'test': 3,
                 'trauma_surv': 80},
          'dx': {'atk_mod': 0, 'def_adj': 1, 'feat': 8, 'score': 13, 'test': 3},
          'in': {'bonus_spells': 0, 'lang': 0, 'learn_spell': 50, 'score': 11},
          'st': {'atk_mod': 0, 'dmg_adj': 0, 'feat': 12, 'score': 9, 'test': 2},
          'ws': {'bonus_spells': 0,
                 'learn_spell': 50,
                 'score': 10,
                 'will_adj': 0}},
 'ca': 0,
 'class_abilities': [{'ability_desc': None,
                      'ability_title': 'Divine Protection',
                      'brief_desc': 'disease immunity, +2 to all saves, +1 AC '
                                    'vs. evil creatures',
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Extraordinary',
                      'brief_desc': '+8% feat of ST',
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Healing Hands',
                      'brief_desc': 'restore 2 hp/day/level; cure disease '
                                    '1/week',
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Honour',
                      'brief_desc': None,
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Horsemanship',
                      'brief_desc': None,
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Sense Evil',
                      'brief_desc': '60-foot range, requires concentration',
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Valiant Resolve',
                      'brief_desc': 'immune to magical fear',
                      'class_id': 9,
                      'level': 1},
                     {'ability_desc': None,
                      'ability_title': 'Weapon Mastery',
                      'brief_desc': '+1 atk/dmg, increased attack rate with '
                                    'one weapon',
                      'class_id': 9,
                      'level': 1}],
 'class_id': 9,
 'class_name': 'Paladin',
 'combat_matrix': {-9: 28,
                   -8: 27,
                   -7: 26,
                   -6: 25,
                   -5: 24,
                   -4: 23,
                   -3: 22,
                   -2: 21,
                   -1: 20,
                   0: 19,
                   1: 18,
                   2: 17,
                   3: 16,
                   4: 15,
                   5: 14,
                   6: 13,
                   7: 12,
                   8: 11,
                   9: 10},
 'deity': {'deity_id': 2,
           'deity_name': 'Artemis',
           'primary_alignment': 'Lawful'},
 'equipment': ['backpack',
               'wooden holy symbol',
               'soft leather pouch',
               'iron rations (1 week)',
               'tinderbox',
               'torches ×2',
               'wineskin (full)'],
 'fa': 1,
 'gender': 'Female',
 'hd': '1d10',
 'hp': 3,
 'level': 1,
 'method': 3,
 'money': {'cp': 0, 'ep': 0, 'gp': 4, 'pp': 0, 'sp': 0},
 'mv': 30,
 'name': '',
 'race': 'Pict (Half-Blood)',
 'race_id': 11,
 'shield': {'cost': 10,
            'def_mod': 2,
            'shield_id': 2,
            'shield_type': 'Large Shield',
            'weight': 10},
 'spells': None,
 'sv': 16,
 'sv_bonus': {'avoidance': 2,
              'death': 2,
              'device': 2,
              'sorcery': 2,
              'transformation': 2},
 'ta': 0,
 'thief_skills': None,
 'turn_undead_matrix': None,
 'weapons_melee': [{'atk_rate': '1/1',
                    'cost': 4,
                    'damage': '1d4',
                    'damage_2h': None,
                    'dmg_adj': 0,
                    'hurlable': True,
                    'hurled_atk': 0,
                    'hurled_rof': '3/2',
                    'mastery': False,
                    'melee_atk': 0,
                    'qty': 1,
                    'range_sml': '10/20/30',
                    'wc': 1,
                    'weapon_id': 108,
                    'weapon_type': 'Dagger',
                    'weight': 1},
                   {'atk_rate': '1/1',
                    'cost': 10,
                    'damage': '1d8',
                    'damage_2h': '1d10',
                    'dmg_adj': 0,
                    'hurlable': False,
                    'hurled_atk': None,
                    'hurled_rof': None,
                    'mastery': False,
                    'melee_atk': 0,
                    'qty': 1,
                    'range_sml': None,
                    'wc': 2,
                    'weapon_id': 120,
                    'weapon_type': "Footman's Mace",
                    'weight': 5},
                   {'atk_rate': '3/2',
                    'cost': 20,
                    'damage': '1d8',
                    'damage_2h': '1d10',
                    'dmg_adj': 1,
                    'hurlable': False,
                    'hurled_atk': None,
                    'hurled_rof': None,
                    'mastery': True,
                    'melee_atk': 1,
                    'qty': 1,
                    'range_sml': None,
                    'wc': 2,
                    'weapon_id': 137,
                    'weapon_type': 'Long Sword',
                    'weight': 4}],
 'weapons_missile': [],
 'xp': 0,
 'xp_bonus': False,
 'xp_to_next': 2750}
```

## Additional Options

`method: int (default: 3)` 

​	The dice method used to roll ability scores. Valid values are 1 through 6. 

`class_id: int (default: 0)` 

​	If `0`, a random class will be selected and dice methods 1 through 6 can be used. Otherwise, a value of 1 to 33 can be entered (see `class_id_map` below), and the dice method will automatically be set to 6, regardless of what is passed 

`subclasses: int (default: 2)`

​	0: Principal classes only (Fighter, Magician, Cleric, Thief)

​	1: Principal classes and subclasses

​	2: Principal classes, subclasses, and sub-subclasses (Fell Paladin, Warlock variants, and Legerdemainist variants)

`xp: int (default: 0)`

​	Experience points, used to determine character level. Must be a positive integer.

`ac_type: str (default: "descending")`

​	Valid values are "descending" or "ascending", indicating which type of AC system to use. If "ascending" is chosen, no combat matrix is provided, FA (fighting ability) is used as a base attack bonus, and AC values are subtracted from 19, e.g. AC 6 in descending system becomes AC 13 in ascending system. Note that this results in everyone (including monsters) having a 5% better chance to hit when using ascending AC. This was a conscious design decision, as it was important to me to have AC 10 for unarmored characters, and keep the FA values as they are stated in the book. Besides, hitting is more fun than missing.

### `class_id_map`

``` python
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

```



## Use Cases

I developed this package to generate characters for my personal gaming group. I use the package along with FastAPI and host the app on Heroku. I use it in conjunction with Google's app script (javascript) to get the character data from the Heroku endpoint, and populate it into a Google Sheets character sheet. It's a bit janky, but it gets the job done for us. I put a lot of work into implementing the rules to generate characters of any class and any level up to the game's maximum of level 12.

If someone out there were to use this and create a proper front-end website for it, that would bring me much joy. If you use this, please share what you've built with it!

That being said, I also plan to hone my own web skills and try to build a web-based front end for it, but that will take time.

## Links

[**App on Heroku**](http://rpg-tools-app.herokuapp.com/docs):  All the endpoints prefixed with `/hyperborea3/` use this package. If you are curious about the container that gets deployed, see [this repo](https://github.com/jderam/rpg-tools-containers).

[**Google Sheet**](https://docs.google.com/spreadsheets/d/1Ll5aQwxn-bHl_GIYN9iQWbO3TitqnWJLHMm6BHP3EoM/edit?usp=sharing) with character generator integrated:

* Click **File > Make a Copy** to create your own personal copy that now belongs to you.
* Click **Extensions > Apps Script** to examine the code that retrieves the character data and populates the active sheet. Note that nothing untoward is going on.
* At the bottom on the Sheets doc, on the tab labeled **Template**, click the little arrow pointing down and choose **Duplicate**. The Template sheet is only there to create more sheets from, and you should never generate a character on the template. Now that you have a new sheet created, find the menu item across the top labeled as **Generate**. It should appear immediately to the right of **Help**. Sometimes you need to wait a few moments for it to appear. Click on that, then click **Random Class**. The first time you (or anyone else) accesses this menu item, an ominous warning will pop up, and you need to grant permissions for the script to run. Only do this if you have followed the previous step, and are comfortable with granting the permissions. Here's how to do it:
  * On the popup that appears saying **Authorization Required**, click **Continue**
  * Choose the google account you want to use with this sheet, and login if necessary
  * On the next window that says **Google hasn't verified this app**, click the small link on the lower left that says **Advanced**
  * Click on the link that appears below. It should say something like **Go to Hyperborea3 Character Generator (unsafe)**
  * It tells you all the nefarious things that could happen, but again, as you can see by examining the code, the only thing it does is update the active sheet with this Google Sheets doc. Click the **Allow** button.
  * You can now generate characters! Congratulations!
  * If you decide not to use this, you won't hurt my feelings. I would personally never use a tool like this from a stranger. 😃
* You can enter an XP amount in the blue-shaded **Experience** cell, and characters will be generated at the corresponding power level.
* You can select a class from the dropdown in the blue-shaded **Class** cell, then click **Generate > Selected Class** to generate a character of a specific class. Alternatively, **Generate > Random Class** will ignore any selection in the **Class** cell and generate a randomly classed character.
* Character generation can take anywhere from a few seconds to up to 30 seconds. This is due to a few factors. First, the Heroku endpoint goes to sleep if it hasn't had a request for 30 minutes, and in this scenario it takes some time to wake up. Additionally, some classes such as the Ranger, Shaman, and Bard cast spells from multiple schools and to arrange these items in an easy-to-use layout, the script needs to merge/unmerge certain cell ranges, add or remove checkboxes, and these actions aren't very performant.
* In order for your friends to be able to use your sheet and create their own tabs to generate their characters, you will need to click the **Share** button and add them as **Editors** by their Google accounts. They will also need to click through all the security warnings as outlined above. Also, make sure they know not to click Generate while they have someone else's sheet active, or a sheet of their own that they care about. Generating a new character will completely overwrite the active sheet!
* The only automation that exists in the sheet is the initial character generation. You can update anything you want after that, but it is up to you to ensure that any other values that would be affected by such a change are also updated. For example, if you increase your Strength score, you will also need to manually update your melee attack bonus, damage adjustment, test, and feat values.
* One final note: Once you have clicked **Make a Copy**, per the above instructions, the copy is owned by you. This is good because no one else can go in later and update what the Apps Scripts code is doing, but it also precludes you from bug fixes or performance updates. That's just how it is, so be aware of it. If I have any worthwhile updates to make on the Google Sheets side, I'll release a new version of it, but I'm pretty happy with where it's at.

## Future Development

I also have plans to implement the following features into this package, as time and motivation allows:

* Additional character data:
  * Favoured weapons
  * Random name generation based on the tables in the rulebook
  * Height and Weight based on the tables in the rulebook
* Add detailed html-formatted spell descriptions to the spells database table in order to enable spell lookups and possibly some sort of tool to create character spellbook documents. Detailed spell information could be added to the character output as well.
* A fully-detailed monster table that would enable the lookup of full monster stat blocks.
* A random treasure generator tool. Pass the treasure type and get a randomly generated result with monetary treasure and/or magic items.
* Given completed spells, monsters, or treasure data, I'd like to create compendiums for use with [Foundry VTT](https://foundryvtt.com/).

## Contributions

Pull requests for small updates and bug fixes are always welcome. If you have a larger update you're interested in contributing, please create an Issue and we can have a conversation about it. If you are a talented front end developer and are interested in creating pretty web tools for this, I'd love to do whatever I can to help you!

