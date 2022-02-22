subdir = "lvl1"

with open(f"{subdir}/spell_names.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    data = line.split()
    spell_id = data[0]
    file_name = f"{subdir}/{('_').join(data[1:])}.yml"
    print(file_name)
    with open(file_name, "w") as sf:
        sf.write(f"id: {spell_id}\n")
