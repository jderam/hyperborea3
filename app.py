from flask import Flask, request
from hyperborea3.player_character import PlayerCharacter


app = Flask(__name__)


@app.route("/")
def root_test():
    return "welcome to Hyperborea"


@app.route("/hyperborea/json")
def hyperborea_character():
    method = 3
    selected_class = "random"
    subclasses = True
    xp = 0

    if request.args:
        args = request.args
        if "method" in args:
            method = args.get("method")
        if "selected_class" in args:
            selected_class = args.get("selected_class")
        if "subclasses" in args:
            subclasses = args.get("subclasses")
        if "xp" in args:
            xp = args.get("xp")

    return PlayerCharacter(
        method=method,
        selected_class=selected_class,
        subclasses=subclasses,
        xp=xp,
    ).to_dict()
