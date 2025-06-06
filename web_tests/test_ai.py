"""
Sprawdza, czy moduł AI zwraca legalny ruch.
"""
import board, ai

def test_ai_responds():
    b = board.Board(size=11)
    x, y = ai.make_move(b, board.WHITE)
    assert b.is_empty(x, y)               # pole wolne
    assert b.in_bounds(x, y)              # współrzędne w granicach
