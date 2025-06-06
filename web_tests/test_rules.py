"""
Testy reguł gry Hex (bez UI).
"""
import board, engine

def test_illegal_double_move(new_board):
    b = new_board
    engine.play_move(b, 5, 5, board.BLACK)
    # Drugi ruch w to samo miejsce musi zostać odrzucony
    assert not engine.play_move(b, 5, 5, board.WHITE)

def test_black_wins_top_bottom():
    b = board.Board(size=3)
    # Czarny łączy górę z dołem
    engine.play_move(b, 0, 0, board.BLACK)
    engine.play_move(b, 0, 1, board.WHITE)
    engine.play_move(b, 1, 0, board.BLACK)
    engine.play_move(b, 1, 1, board.WHITE)
    engine.play_move(b, 2, 0, board.BLACK)
    assert b.winner == board.BLACK
