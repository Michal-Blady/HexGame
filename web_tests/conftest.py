"""
Wspólne fikstury dla testów Hex.
"""
import sys, pathlib, pytest

# Dodaj katalog 'web' do sys.path, aby importować moduły gry
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "web"))

@pytest.fixture(scope="session")
def new_board():
    import board
    return board.Board(size=11)
