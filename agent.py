from __future__ import annotations
from board import Board
from collections.abc import Callable
from math import floor
import heapq

'''
Heuristics
'''

def BFS(board: Board) -> int:
    return 0

def MT(board: Board) -> int:
    return (int(board.state[0, 0] != 1) + int(board.state[0, 1] != 2) + int(board.state[0, 2] != 3) +
            int(board.state[1, 0] != 4) + int(board.state[1, 1] != 5) + int(board.state[1, 2] != 6) +
            int(board.state[2, 0] != 7) + int(board.state[2, 1] != 8)                               )

def _manhattan(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)

def CB(board: Board) -> int:
    score: int = 0
    
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctY = (tile-1) % 3
            correctX = floor((tile-1)/3)
            
            #print(x, y, correctX, correctY)
            
            score += _manhattan(x, y, correctX, correctY)
    
    return score

def NA(board: Board) -> int:
    return 0


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self._count = 0 

    def push(self, priority, item):
        heapq.heappush(self._heap, (priority, self._count, item))
        self._count += 1

    def pop(self):
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self):
        return self._heap[0][2]

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return not self._heap
'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    
    frontier = PriorityQueue()
    cost = {}
    reached = {}
    
    came_from = {}
    
    cost[str(board)] = 0
    reached[str(board)] = 0 + heuristic(board)
    came_from[str(board)] = (None, None)
    frontier.push(reached[str(board)], board)
    
    actions = []
    
    while(not frontier.is_empty()):
        parent = frontier.pop()
        if(parent.goal_test()): 
            path = []
            current_key = str(parent)
            while came_from[current_key][0] is not None:
                prev_key, action = came_from[current_key]
                path.append(action)
                current_key = prev_key
            path.reverse()
            print(path)
            return path
        
        for child in parent.next_action_states():
            state = child[0]
            action = child[1]
            
            actions.append(action)
            
            path_cost = cost[str(parent)] + 1
            a = path_cost + heuristic(state)
            
            if not (str(state) in reached) or a < reached[str(state)]:
                reached[str(state)] = a
                cost[str(state)] = path_cost
                
                came_from[str(state)] = (str(parent), action)
                
                frontier.push(a, state)
    
    return -1

