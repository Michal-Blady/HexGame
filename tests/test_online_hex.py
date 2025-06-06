import csv, json, pathlib, time, pytest
from helpers import new_game, HexPage

MOVES = pathlib.Path(__file__).parent
BASELINE = pathlib.Path(__file__).parent.parent / "baseline/expected_state.json"

def read_moves(fname):
    with open(MOVES / fname, newline="") as f:
        for row, col in csv.reader(f):
            yield int(row), int(col)

def test_online_two_players(driver):
    gid = new_game()
    p1 = HexPage(driver, gid, role=1)
    # drugie okno Firefoxa dla Player-2
    driver2 = driver.__class__(service=driver.service, options=driver.options)
    p2 = HexPage(driver2, gid, role=2)

    for (r1, c1), (r2, c2) in zip(read_moves("moves_p1.csv"),
                                  read_moves("moves_p2.csv")):
        p1.click_cell(r1, c1)
        time.sleep(0.2)          # krótka przerwa – update stanu
        p2.click_cell(r2, c2)
        time.sleep(0.2)

    # poczekaj aż gra rozpozna zwycięzcę lub zabraknie ruchów
    time.sleep(1)

    final_state = p1.board_state()   # wystarczy z jednej przeglądarki
    if not BASELINE.exists():
        BASELINE.write_text(json.dumps(final_state, indent=2))
        pytest.skip("baseline created – uruchom test ponownie")
    else:
        expected = json.loads(BASELINE.read_text())
        assert final_state == expected, "❌ Stan planszy zmienił się!"
