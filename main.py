from typing import Any, Dict

from fastapi import FastAPI, Query
from hyperborea3.player_character import PlayerCharacter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hyperborea3"}


@app.get("/random")
async def random_char(
    method: int = Query(3),
    subclasses: int = Query(2),
    xp: int = Query(0),
    ac_type: str = Query("ascending"),
) -> Dict[str, Any]:
    pc: PlayerCharacter = PlayerCharacter(
        method=method,
        subclasses=subclasses,
        xp=xp,
        ac_type=ac_type,
    )
    pc_dict: Dict[str, Any] = pc.to_dict()
    return pc_dict


@app.get("/class_id/{class_id}")
async def specific_class(
    class_id: int,
    xp: int = Query(0),
    ac_type: str = Query("ascending"),
) -> Dict[str, Any]:
    pc = PlayerCharacter(
        class_id=class_id,
        xp=xp,
        ac_type=ac_type,
    )
    pc_dict: Dict[str, Any] = pc.to_dict()
    return pc_dict
