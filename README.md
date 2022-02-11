# hyperborea-tools

![Tests](https://github.com/jderam/hyperborea-tools/actions/workflows/tests.yml/badge.svg)

An app for creating randomly-generated characters for the [Hyperborea](https://www.hyperborea.tv/) 3rd edition tabletop roleplaying game.



## Installation

``` bash
$ python -m pip install hyperborea3
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

Check out the [directory of sample characters](https://github.com/jderam/hyperborea-tools/tree/main/hyperborea3/sample_data/PlayerCharacter) to examine and explore the data structures.




## Additional Options

The PlayerCharacter object accepts the following options:

`method`

> **Description**: The dice method used to roll ability scores. Methods I through V are used with randomly chosen classes. Method VI is always used when a specific class is chosen.
>
> > *Method I*: 3d6 in order
> >
> > *Method II*: Best of three sets of 3d6 in order
> >
> > *Method III*: 4d6 drop lowest
> >
> > *Method IV*: Best of three 3d6 rolls for each attribute
> >
> > *Method V*: 2d6+6 in order.
> >
> > *Method VI*: 3d6 for each attribute that doesn't have a required minimum. 4d6 drop lowest for each attribute that does have a required minimum, rerolling as necessary until the requisite minumum score is achieved.
>
> **Type**: int
>
> **Default**: 3
>
> **Valid Values**: 1 through 5 when `class_id=0` (q.v.), 6 for any other `class_id` value.



`class_id`

> **Description**: If `0`, a random class will be selected and dice methods 1 through 5 can be used. Otherwise, a value of 1 to 33 can be entered, and the dice method will automatically be set to 6, regardless of what is passed.
>
> **Type**: int
>
> **Default**: 0
>
> **Valid Values**: 0 through 33. See `class_id_map` below.

​	 

`subclasses`

> **Description**: Determines which Only relevant when generating a character of a random class. 
>
> **Type**: int
>
> **Default**: 2 (all classes, subclasses, and sub-subclasses)
>
> **Valid Values**:
>
> > 0: Principal classes only. (`class_id` 1 through 4)
> >
> > 1: Principal classes plus subclasses. (`class_id` 1 through 26)
> >
> > 2: Pricipal classes, subclasses, and sub-subclasses, which include Fell Paladin, Warlock variants, and Legerdemainist variants. (`class_id` 1 through 33)



`xp`

> **Description**: The number of experience points the character has. This will determine the character's level, which is capped at 12.
>
> **Type**: int
>
> **Default**: 0
>
> **Valid Values**: Any positive integer.

​	

`ac_type`

> **Description**: Indicates which type of AC system to use. If "ascending" is chosen, no combat matrix is provided, FA (fighting ability) is used as a base attack bonus, and AC values are subtracted from 19, e.g. AC 6 in descending system becomes AC 13 in ascending system. Note that this results in everyone (including monsters) having a 5% better chance to hit when using ascending AC. This was a conscious design decision, as it was important to me to have AC 10 for unarmored characters, and keep the FA values as they are stated in the book. Besides, hitting is more fun than missing.
>
> **Type**: str
>
> **Default**: "descending"
>
> **Valid Values**: "descending" or "ascending"

​	

### `class_id_map`

``` python
1: "Fighter"
2: "Magician"
3: "Cleric"
4: "Thief"
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
27: "Fell Paladin"
28: "Ice Lord"
29: "Fire Lord"
30: "Death Soldier"
31: "Mountebank"
32: "Fire Thief"
33: "Ice Thief"
```



## Use Cases

I developed this package to generate characters for my personal gaming group. I use the package along with FastAPI and host the app on Heroku. I use it in conjunction with Google's app script (javascript) to get the character data from the Heroku endpoint, and populate it into a Google Sheets character sheet. It's a bit janky, but it gets the job done for us. I put a lot of work into implementing the rules to generate characters of any class and any level up to the game's maximum of level 12.

If someone out there were to use this and create a proper front-end website for it, that would bring me much joy. If you use this, please share what you've built with it!

That being said, I also plan to hone my own web skills and try to build a web-based front end for it, but that will take time.



## Links

Container

[**App on Heroku**](http://rpg-tools-app.herokuapp.com/docs):  All the endpoints prefixed with `/hyperborea3/` use this package. If you are curious about the container that gets deployed, see [this repo](https://github.com/jderam/rpg-tools-containers).

**Google Sheet**: with character generator integrated. If you are intersted in simply making a copy of the Google Sheet character generator for your gaming group to use, see [this blog post](https://peoplethemwithmonsters.blogspot.com/2022/02/google-sheets-character-generator-for.html) for instructions on how to do that.



## Future Development

I also have plans to implement the following features into this package, as time and motivation allows:

* Additional character data:
  * Favoured weapons
  * Secondary skills
  * Random name generation based on the tables in the rulebook
  * Height and Weight based on the tables in the rulebook
  
* Add detailed html-formatted spell descriptions to the spells database table in order to enable spell lookups and possibly some sort of tool to create character spellbook documents. Detailed spell information could be added to the character output as well.

* A fully-detailed monster database table that would enable the lookup of full monster stat blocks.

* A random treasure generator tool. Pass the treasure type and get a randomly generated result with monetary treasure and/or magic items.

* Given completed spells, monsters, or treasure data, I'd like to create compendiums for use with [Foundry VTT](https://foundryvtt.com/).

  

## Contributions

Pull requests for small updates and bug fixes are always welcome. If you have a larger update you're interested in contributing, please create an Issue and we can have a conversation about it. If you are a talented front end developer and are interested in creating pretty web tools for this, I'd love to do whatever I can to help you!

