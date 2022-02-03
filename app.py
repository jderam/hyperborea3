from flask import Flask, request
from hyperborea3.player_character import PlayerCharacter


app = Flask(__name__)


@app.route("/")
def root_test():
    return "welcome to Hyperborea"


@app.route("/hyperborea/json")
def hyperborea_character():
    method = 3
    class_id = 0
    subclasses = 2
    xp = 0
    ac_type = "ascending"

    if request.args:
        args = request.args
        if "method" in args:
            method = args.get("method")
        if "class_id" in args:
            class_id = args.get("class_id")
        if "subclasses" in args:
            subclasses = args.get("subclasses")
        if "xp" in args:
            xp = args.get("xp")
        if "ac_type" in args:
            ac_type = args.get("ac_type")

    return PlayerCharacter(
        method=int(method),
        class_id=int(class_id),
        subclasses=int(subclasses),
        xp=int(xp),
        ac_type=ac_type,
    ).to_dict()
