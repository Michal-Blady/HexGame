import json, requests, pathlib, time
from selenium.webdriver.common.by import By

BASE = "http://127.0.0.1:5000"

def new_game() -> str:
    r = requests.post(f"{BASE}/api/game", json={"ai": False})
    r.raise_for_status()
    return r.json()["id"]

class HexPage:
    def __init__(self, driver, gid: str, role: int):
        self.drv = driver
        self.url = f"{BASE}/?mode=online&gid={gid}&role={role}"
        self.drv.get(self.url)


    def _cell(self, r: int, c: int):
        return self.drv.find_element(By.CSS_SELECTOR,
              f".row:nth-child({r+1}) .cell:nth-child({c+1})")

    def click_cell(self, r: int, c: int):
        self._cell(r, c).click()

    def board_state(self):
        rows = self.drv.find_elements(By.CSS_SELECTOR, ".row")
        return [
            [ "E" if "black" not in cell.get_attribute("class")
                    and "white" not in cell.get_attribute("class")
              else ("B" if "black" in cell.get_attribute("class") else "W")
              for cell in row.find_elements(By.CSS_SELECTOR, ".cell") ]
            for row in rows
        ]
