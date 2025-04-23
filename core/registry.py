from __future__ import annotations
import json, uuid, time
from pathlib import Path
from core.engine import HexEngine
from core.board  import Cell

DATA = Path("games")
DATA.mkdir(exist_ok=True)

class GameInfo(dict):
    pass

def _fn(gid: str) -> Path:
    return DATA / f"{gid}.json"

def new_game(size: int, with_ai: bool) -> GameInfo:
    gid  = uuid.uuid4().hex[:6]
    info = GameInfo(id=gid, ts=time.time(), size=size, ai=with_ai, finished=False)
    save(gid, HexEngine(size), info)
    return info

def load(gid: str) -> tuple[HexEngine, GameInfo]:
    data = json.loads(_fn(gid).read_text())
    info = GameInfo(data["info"])
    eng  = HexEngine(info["size"])
    eng.board.grid = [[Cell(v) for v in row] for row in data["grid"]]
    eng.turn = Cell(data["turn"])
    return eng, info

def save(gid: str, eng: HexEngine, info: GameInfo) -> None:
    _fn(gid).write_text(json.dumps({
        "grid": [[cell.value for cell in row] for row in eng.board.grid],
        "turn": eng.turn.value,
        "info": info,
    }))
