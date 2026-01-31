from __future__ import annotations
from board import Board
from collections.abc import Callable
from math import floor

'''
Heuristics
'''
def MT(board: Board) -> int:
    return (int(board.state[0, 0] != 1) + int(board.state[0, 1] != 2) + int(board.state[0, 2] != 3) +
            int(board.state[1, 0] != 4) + int(board.state[1, 1] != 5) + int(board.state[1, 2] != 6) +
            int(board.state[2, 0] != 7) + int(board.state[2, 1] != 8)                               )

def manhattan(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

def CB(board: Board) -> int:
    score: int = 0
    
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctX = (tile-1) % 3
            correctY = floor((tile-1)/3)
            
            score += manhattan(x, y, correctX, correctY)
    
    return score

def NA(board: Board) -> int:
    return 



'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    return
