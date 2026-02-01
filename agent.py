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

#this will return the smallest heuristic -  a little better than BFS
def NA_1(board: Board) -> int:
    score: int = 0
    minimum:int = 1000 
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctY = (tile-1) % 3
            correctX = floor((tile-1)/3)
            
            #print(x, y, correctX, correctY)
            
            score =  _manhattan(x, y, correctX, correctY)
            if score < minimum: 
                minimum=score
    
    return minimum


#return maximum heursitc from tiles 1-8. Half of BFS around set of 10, around a third of BFS in set of 20. Still not better than CB or MT
def NA_2(board: Board) -> int:
    score: int = 0
    maximum:int = -1 
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctY = (tile-1) % 3
            correctX = floor((tile-1)/3)
            
            #print(x, y, correctX, correctY)
            
            score =  _manhattan(x, y, correctX, correctY)
            if score >maximum: 
                maximum=score
    
    return maximum

#multiply min herustic by 8, didn't work that well 
def NA_3(board: Board) -> int:
    score: int = 0
    minimum:int = 1000 
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctY = (tile-1) % 3
            correctX = floor((tile-1)/3)
            
            #print(x, y, correctX, correctY)
            
            score =  _manhattan(x, y, correctX, correctY)
            if score < minimum: 
                minimum=score
    
    return minimum * 8 




def NA_4(board: Board) -> int:
    score: int = 0
    scores = []
    for x in range(3):
        for y in range(3): 
            if board.open_space[0] == x and board.open_space[1] == y:
                continue
            
            tile = board.state[x, y]
            correctY = (tile-1) % 3
            correctX = floor((tile-1)/3)
            
            #print(x, y, correctX, correctY)
            
            score = _manhattan(x, y, correctX, correctY)
            scores.append(score)
    
    
    scores.sort()
    
    mid_index = int(len(scores)/2)
    return scores[mid_index]



'''
What constraints does manhattan not explore properly?
    -It doesn't consider that tiles can get blocked. 
        -> what if we add a lower bound on that, and add an extra move to account for:
          "moving the tile in front out of the way?" 

'''

def NA_5(board: Board) -> int:
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
            score+=2 #added step to account for removing a piece...
    
    return score

'''
Assignment description says heuristic may not be admissible. Let's try to 
deliberately make a non admissible one and see if it reduces search time: 
for example: reducing
'''

def NA(board: Board) -> int:
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
    score = score * 2 
    return score








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

#check if this works for BFS since idk if the priority queue becomes a FIFO queue 
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    
    frontier = PriorityQueue()
    cost = {} #cost just stores g(n) 
    reached = {} #reached stores f(n) = g(n) + h(n)
    
    came_from = {}

    num_nodes:int = 0 
    
    cost[str(board)] = 0  
    reached[str(board)] = 0 + heuristic(board) 
    came_from[str(board)] = (None, None)
    frontier.push(reached[str(board)], board)
    
    actions = []
    
    while(not frontier.is_empty()):
        parent = frontier.pop() #pop queue 
        if(parent.goal_test()): #if parent is the goal state, return path
            path = []
            current_key = str(parent)
            while came_from[current_key][0] is not None:
                prev_key, action = came_from[current_key]
                path.append(action)
                current_key = prev_key
            path.reverse()
            print(path)
            print("Number of nodes searched", num_nodes)  #check if this is accurate 
            return path
        
        for child in parent.next_action_states():
            num_nodes+=1 #since we're considering a new child state - we're increasing num_nodes by 1. 
            state = child[0]
            action = child[1]
            actions.append(action)
            
            path_cost = cost[str(parent)] + 1 #can only make one move per turn/cost +1 
            a = path_cost + heuristic(state) #calculating estimation a= g(n) + h(n)
            
            if not (str(state) in reached) or a < reached[str(state)]:
                reached[str(state)] = a
                cost[str(state)] = path_cost
                
                came_from[str(state)] = (str(parent), action)
                
                frontier.push(a, state)
        
    
    return -1

