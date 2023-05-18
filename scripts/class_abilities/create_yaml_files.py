from hyperborea3.db import execute_query_all

class_abilities = execute_query_all("SELECT * FROM class_abilities")

for ca in class_abilities:
    id = ca["class_ability_id"]
    title = ca["ability_title"]
    with open(
        f"yaml/{id}_{title.replace('/', '-').replace(' ', '_')}.yml", "w"
    ) as yml_file:
        yml_file.write(f"id: {id}\n")
        yml_file.write(f"title: {title}\n")
        yml_file.write("desc: \n")
