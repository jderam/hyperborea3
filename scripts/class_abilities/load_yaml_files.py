# mypy: ignore-errors

import os
import yaml
from hyperborea3.db import get_cursor

cwd = os.getcwd()
assert cwd.split("/")[-1] == "class_abilities"

yaml_files = os.listdir("yaml")
# print(yaml_files)

CUR = get_cursor()

for yf in yaml_files:
    with open(f"yaml/{yf}", "r") as f:
        payload = yaml.safe_load(f)
    id = payload["id"]
    desc = payload["desc"]
    print(f"{id = }")
    print(f"{desc = }")

CUR.close()
