from board import Board
import numpy as np
import time
from agent import CB, NA, MT, BFS, a_star_search


def main():
    for m in [10,20,30,40,50]:
        for seed in range(0,10):
            print("Size of problem set:", m)
            function_set = [CB, NA, MT]

            for function in function_set: 
                board = Board(m, seed)   # reset board each run
                start = time.process_time()   
                result = a_star_search(board=board, heuristic=function)
                end = time.process_time()

                solution_cpu_time = end - start
                print(f"Length of the solution found for {function.__name__}: {len(result)}")
                print("Total CPU Time spent", solution_cpu_time)
                print("\n\n")

if __name__ == "__main__":
    main()

