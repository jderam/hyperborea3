from typing import Dict, Optional

from fastapi import FastAPI, Query
from hyperborea3.player_character import PlayerCharacter

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hyperborea-tools"}


@app.get("/random")
async def random_char(
    method: Optional[int] = Query(3),
    subclasses: Optional[int] = Query(2),
    xp: Optional[int] = Query(0),
    ac_type: Optional[str] = Query("ascending"),
) -> Dict:
    pc = PlayerCharacter(
        method=method,
        subclasses=subclasses,
        xp=xp,
        ac_type=ac_type,
    )
    return pc.to_dict()


@app.get("/class_id/{class_id}")
async def specific_class(
    class_id: int,
    xp: Optional[int] = Query(0),
    ac_type: Optional[str] = Query("ascending"),
) -> Dict:
    pc = PlayerCharacter(
        class_id=class_id,
        xp=xp,
        ac_type=ac_type,
    )
    return pc.to_dict()
