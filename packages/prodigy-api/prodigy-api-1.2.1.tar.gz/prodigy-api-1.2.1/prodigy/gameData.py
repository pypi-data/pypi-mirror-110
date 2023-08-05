import os
from typing import Dict, List, TypedDict
import requests_cache
from prodigy.gameStatus import gameStatus

s = requests_cache.CachedSession(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache"))

class GameDataObject(TypedDict):
    ID: int
    assetID: int
    type: str
    gender: int
    data: dict
    metadata: dict
    name: str

def gameData() -> Dict[str, List[GameDataObject]]:
    gameDataVersion = gameStatus()["prodigyGameFlags"]["gameDataVersion"]
    return s.get(f"https://cdn.prodigygame.com/game/data/production/{gameDataVersion}/data.json").json()
