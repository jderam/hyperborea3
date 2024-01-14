# hyperborea3

![Tests](https://github.com/jderam/hyperborea3/actions/workflows/tests.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An app for creating randomly-generated characters for the [Hyperborea](https://www.hyperborea.tv/) 3rd edition tabletop roleplaying game.

## Table of Contents
- [hyperborea3](#hyperborea3)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Parameters](#parameters)
  - [Sample Output](#sample-output)
  - [`class_id_map`](#class_id_map)
  - [Use Cases](#use-cases)
  - [Links](#links)
  - [Future Development](#future-development)
  - [Contributions](#contributions)

## Installation

``` bash
$ python -m pip install hyperborea3
```

## Usage

The main entry point to this application is the `PlayerCharacter` class. By default, a random character will be generated with the following options:

* Abilities are rolled using dice method III (4d6 drop lowest)
* Class is randomly selected from amongst those where ability score requirements are met
* 0 experience points
* All character class options are enabled
* The by-the-book descending Armour Class system is used

``` python
from pprint import pprint
from hyperborea3.player_character import PlayerCharacter

pc = PlayerCharacter()
pprint(pc.to_dict())
```
See [Sample Output](#sample-output) for some examples of what the generated characters look like.

## Parameters

Parameter | Description
----------|------------
`method` | _int, default 3_<br>Dice method used to roll ability scores. <br>**Allowed Values**: If no `class_id` is passed, `1`, `2`, `3`, `4`, `5` may be used. If a specific `class_id` other than `0` is passed, any value passed is ignored and `method=6` is automatically used.<br>**Example**: `pc = PlayerCharacter(method=5)` to create a random-classed PC using dice method V for rolling ability scores.
`class_id` | _int, default 0_<br>If `0`, a random class will be selected and dice methods 1 through 5 can be used. Otherwise, a value of 1 to 33 can be entered, and the dice method will automatically be set to 6, regardless of what is passed.<br>**Allowed Values**: `0` through `33`. See [`class_id_map`](#classidmap) below.<br>**Example**: `pc = PlayerCharacter(class_id=10)` to create a Ranger.
`subclasses` | _int, default 2_<br>Determines which classes are selected from when generating a character of a random class.<br>**Allowed Values**: `0`=Principal classes only (Fighter, Magician, Cleric, Thief); `1`=Principal classes plus subclasses; `2`=Principal classes, subclasses, and variant subclasses like the Ice Thief and Fell Paladin.<br>**Example**: `pc = PlayerCharacter(subclasses=0)` to create a random character from one of the 4 principal classes.
`xp` | _int, default 0_<br>The number of experience points the character has. This will determine the character's level, which is capped at 12.<br>**Allowed Values**: Any positive integer<br>**Example**: `pc = PlayerCharacter(class_id=1, xp=4000)` to create a 3rd-level Fighter.
`ac_type` | _str, default "descending"_<br>Choose whether to use ascending or descending AC system.<br>**Allowed Values**: `"descending"`, `"ascending"`<br>**Example**: `pc = PlayerCharacter(ac_type="ascending")`

## Sample Output

Check out the [directory of sample characters](https://github.com/jderam/hyperborea3/tree/main/hyperborea3/sample_data/PlayerCharacter) to examine and explore the data structures.

## `class_id_map`
Use this as a reference if you need to pass `class_id` to generate a character of a specific class.

``` python
1: "Fighter"
2: "Magician"
3: "Cleric"
4: "Thief"
# --------------> subclasses=0 will return a choice from above this line
5: "Barbarian"
6: "Berserker"
7: "Cataphract"
8: "Huntsman"
9: "Paladin"
10: "Ranger"
11: "Warlock"
12: "Cryomancer"
13: "Illusionist"
14: "Necromancer"
15: "Pyromancer"
16: "Witch"
17: "Druid"
18: "Monk"
19: "Priest"
20: "Runegraver"
21: "Shaman"
22: "Assassin"
23: "Bard"
24: "Legerdemainist"
25: "Purloiner"
26: "Scout"
# --------------> subclasses=1 will return a choice from above this line
27: "Fell Paladin"
28: "Ice Lord"
29: "Fire Lord"
30: "Death Soldier"
31: "Mountebank"
32: "Fire Thief"
33: "Ice Thief"
# --------------> subclasses=2 will return a choice from above this line
```

## Use Cases

I developed this package to generate characters for my personal gaming group. I use the package along with FastAPI and host the app on [render](https://render.com/). I use it in conjunction with Google's app script (javascript) to get the character data from the REST endpoint, and populate it into a Google Sheets character sheet. It's a bit janky, but it gets the job done for us. I put a lot of work into implementing the rules to generate characters of any class and any level up to the game's maximum of level 12.

## Links

[**App on render**](https://rpg-tools.onrender.com/docs):  All the endpoints prefixed with `/hyperborea3/` use this package. If you are curious about the container that gets deployed, see [this repo](https://github.com/jderam/rpg-tools-containers).

[**Google Sheet**](https://docs.google.com/spreadsheets/d/1Ll5aQwxn-bHl_GIYN9iQWbO3TitqnWJLHMm6BHP3EoM/edit?usp=sharing): with character generator integrated via Google's _Apps Script_. If you are intersted in simply making a copy of the Google Sheet character generator for your gaming group to use, see [this blog post](https://peoplethemwithmonsters.blogspot.com/2022/02/google-sheets-character-generator-for.html) for instructions on how to do that.

[**Web-based Print-and-Play Character Generator**](https://kilroy86.neocities.org/hyperborea3/hyperborea3-chargen): Generate a character using the dropdowns to set options. Note that if you generate a specific class, the dice method automatically changes to `VI`. You should be able to fit the resulting character sheet on a single printed page. In my own experimentation, I've needed to set the scale to 70% to get everything to fit. Enjoy!

## Contributions

Pull requests for small updates and bug fixes are always welcome. If you have a larger update you're interested in contributing, please create an Issue and we can have a conversation about it. If you are a talented front end developer and are interested in creating pretty web tools for this, I'd love to do whatever I can to help you!
