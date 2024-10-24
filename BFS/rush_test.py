#! /usr/bin/env python
"""
support code for the rush-hour game

ASSUMPTIONS
 1. game file is formatted correctly
 2. goal is always in the 3rd row
 3. empty positions are indicated by '0'
 4. Cars occupy 2 spaces and move 1 space in any direction if the move is possible and valid.
 5. Trucks occupy 3 spaces and move 1 space up or down only if the move is possible and valid.
 6. The goal piece occupies 2 spaces and moves 1 space right or left only if the move is possible and valid.
"""


from collections import deque
def load_game(filename):
    """Reads filename and returns a list representing the initial state of the game"""
    with open(filename) as fin:
        nextline = fin.readline()
        maxX, maxY = [int(token) for token in nextline.split()]
        gameArray = []
        for i in range(maxX):
            nextline = fin.readline()
            gameArray.append(nextline.split())
    return gameArray

def print_board(board):
    """pretty print the board"""
    for row in board:
        print(' '.join(cell.rjust(4) for cell in row))

def copy_game(alist):
    """alist should be a 2D matrix representing a game state. returns a copy of the game state"""
    return [list(row) for row in alist]

def equal_games(game1, game2):
    """games are board states, returns True if two game boards have the same values at all the positions"""
    return game1 == game2

def legal_position(board, x, y):
    """returns True if (x, y) is on the board"""
    return 0 <= x < len(board) and 0 <= y < len(board[0])

def empty(board, x, y):
    """returns True if the (x, y) position on the board is empty"""
    return legal_position(board, x, y) and board[x][y] == '0'

def at_goal(board):
    """returns True if goal is in the rightmost column"""
    return board[2][-1] == 'g'

def move_left(board, y, x):
    if x <= 0:
        return False
    piece = board[y][x]
    if piece == '0':
        return False
    if piece[0] in ['c', 'g']:  # car or goal piece (length 2)
        if x + 1 >= len(board[0]) or board[y][x+1] != piece:
            return False
        if empty(board, y, x-1):
            board[y][x-1], board[y][x], board[y][x+1] = piece, piece, '0'
            return True
    elif piece[0] == 't':  # truck (length 3)
        if x + 2 >= len(board[0]) or board[y][x+1] != piece or board[y][x+2] != piece:
            return False
        if empty(board, y, x-1):
            board[y][x-1], board[y][x], board[y][x+1], board[y][x+2] = piece, piece, piece, '0'
            return True
    return False

def move_right(board, y, x):
    piece = board[y][x]
    if piece == '0':
        return False
    if piece[0] in ['c', 'g']:  # car or goal piece (length 2)
        if x + 2 >= len(board[0]) or board[y][x+1] != piece:
            return False
        if empty(board, y, x+2):
            board[y][x], board[y][x+1], board[y][x+2] = '0', piece, piece
            return True
    elif piece[0] == 't':  # truck (length 3)
        if x + 3 >= len(board[0]) or board[y][x+1] != piece or board[y][x+2] != piece:
            return False
        if empty(board, y, x+3):
            board[y][x], board[y][x+1], board[y][x+2], board[y][x+3] = '0', piece, piece, piece
            return True
    return False

def move_up(board, y, x):
    if y <= 0:
        return False
    piece = board[y][x]
    if piece == '0':
        return False
    if piece[0] in ['c', 'g']:  # car or goal piece (length 2)
        if y + 1 >= len(board) or board[y+1][x] != piece:
            return False
        if empty(board, y-1, x):
            board[y-1][x], board[y][x], board[y+1][x] = piece, piece, '0'
            return True
    elif piece[0] == 't':  # truck (length 3)
        if y + 2 >= len(board) or board[y+1][x] != piece or board[y+2][x] != piece:
            return False
        if empty(board, y-1, x):
            board[y-1][x], board[y][x], board[y+1][x], board[y+2][x] = piece, piece, piece, '0'
            return True
    return False

def move_down(board, y, x):
    piece = board[y][x]
    if piece == '0':
        return False
    if piece[0] in ['c', 'g']:  # car or goal piece (length 2)
        if y + 2 >= len(board) or board[y+1][x] != piece:
            return False
        if empty(board, y+2, x):
            board[y][x], board[y+1][x], board[y+2][x] = '0', piece, piece
            return True
    elif piece[0] == 't':  # truck (length 3)
        if y + 3 >= len(board) or board[y+1][x] != piece or board[y+2][x] != piece:
            return False
        if empty(board, y+3, x):
            board[y][x], board[y+1][x], board[y+2][x], board[y+3][x] = '0', piece, piece, piece
            return True
    return False

def list_valid_move(board):
    moves = []
    for y, row in enumerate(board):
        for x, piece in enumerate(row):
            if piece != '0':
                if piece[0] == 'g':  # Goal piece
                    if move_left(copy_game(board), y, x):
                        moves.append([[y,x],'L'])
                    if move_right(copy_game(board), y, x):
                        moves.append([[y,x],'R'])
                elif piece[0] == 't':  # Truck
                    if move_up(copy_game(board), y, x):
                        moves.append([[y,x],'U'])
                    if move_down(copy_game(board), y, x):
                        moves.append([[y,x],'D'])
                elif piece[0] == 'c':  # Car
                    if move_left(copy_game(board), y, x):
                        moves.append([[y,x],'L'])
                    if move_right(copy_game(board), y, x):
                        moves.append([[y,x],'R'])
                    if move_up(copy_game(board), y, x):
                        moves.append([[y,x],'U'])
                    if move_down(copy_game(board), y, x):
                        moves.append([[y,x],'D'])
    return moves

def apply_move(board, move):
    y, x = move[0]
    direction = move[1]
    if direction == 'L':
        move_left(board, y, x)
    elif direction == 'R':
        move_right(board, y, x)
    elif direction == 'U':
        move_up(board, y, x)
    elif direction == 'D':
        move_down(board, y, x)
    return board

def RushHour(filein):
    print(f"Loading game from file: {filein}")
    initialBoard = load_game(filein)
    print("Initial board state:")
    print_board(initialBoard)
    moveListPrint(initialBoard)
    
def moveListPrint(initialBoard):
    if(at_goal(initialBoard)):
        print("The initial board or the given board has the goal piece at the goal state no move needed")
        return
    start_time=time.perf_counter()
    moveList=BFS(initialBoard)
    end_time=time.perf_counter()
    totTime=end_time-start_time
    print(f"Total time taken: {totTime:.4f} seconds")
    if moveList: 
        print("Yay you Won! \nSolution found. The Solutions are:")
        for move in moveList:
            print("\t",move)
    else:
        print("Game over!!! \n Solution not found.")
        
import time
def BFS(initialBoard):
    
    visited = [] # we can also use sets for visited to reduce the time complexity.
    visited.append(tuple(map(tuple, initialBoard)))
    """ Used tuple conversion to convert the gamearray list to tuple. 
    This way when we store the gamearray which is a list. 
    We have to convert the list to tuple so that the values don't change.
    Tuple is immutable"""

    q = deque([(initialBoard, [])]) # adding board and moves as a tuple inside a list so that it cant be changed.
                                    # using lists instead of sets for this requirement - First in first out concept. Sets have no order. 
    totStates=0
    while q:
        gameState = q.popleft() #First in First out.
        currentBoard = gameState[0] #0th index value will be the current board.
        moves = gameState[1] #1st index value will be the moves
        

        print("Current board state:")
        print_board(currentBoard)  # Print current board state(debugging)
        totStates+=1
        print("Total states till now: ", totStates)

        if at_goal(currentBoard):
            return moves  # Found the goal - return move set

        validMoves = list_valid_move(currentBoard)
        print("Valid moves: ", validMoves)  # Print valid moves

        for move in validMoves: #need to find the valid moves from the current board valid moves
            nextBoard = apply_move(copy_game(currentBoard), move) 
            newState = tuple(map(tuple, nextBoard))

            if newState not in visited: #if the new state(converted new board) obtained not in the visited list before append it. 
                visited.append(newState)
                print("The move Selected is: ", [move])#debug
                q.append((nextBoard, moves + [move]))
            else:
                print(f"This move {move} is already visited")
    print("No solutions found after this many states", totStates)
    return None

def manual_play():
    play_on = 'Y'
    while play_on.upper() == 'Y':
        print("\nGameBoard1 = test1.txt \nGameBoard2 = test2.txt \n")
        
        g_b_file = input("Enter GameBoard file: ")
        print(f"Loading file {g_b_file}\n")
        game_board = load_game(g_b_file)
        
        if at_goal(game_board):
            print("The initial state is already the goal state. No moves needed!")
            play_on = input("Do you want to play again? (Y/N): ")
            continue

        while not at_goal(game_board):
            print_board(game_board)
            valid_moves = list_valid_move(game_board)
            print("Valid moves are:", valid_moves)
            
            move_input = input("Enter a move (e.g., [2,3],R) or 'q' to quit: ")
            if move_input.lower() == 'q':
                break 
            try:
                move_input = move_input.replace(" ", "").strip("[]")
                move_parts = move_input.split("],")
                if len(move_parts) != 2:
                    raise ValueError("Invalid input format")

                position = list(map(int, move_parts[0].strip("[").split(",")))
                direction = move_parts[1].strip("'")
                
                move = [position, direction]
                
                if move not in valid_moves:
                    print("Not a valid move. Please try again.\n")
                else:
                    game_board = apply_move(game_board, move)
                    print("Move applied successfully!\n")
            except Exception as e:
                print(f"Invalid input. Please enter a move in the correct format. Error: {e}\n")
        
        if at_goal(game_board):
            print("Congratulations! You've reached the goal!")
        else:
            print("Game ended without reaching the goal.")
        
        play_on = input("Do you want to play again? (Y/N): ")

def main():
    print("Welcome to the Rush Hour Puzzle Solver!")
    
    while True:
        choice = input("Choose mode: (1) Auto Solve, (2) Manual Play, (3) Quit: ")
        if choice == '1':
            filein = input("Enter the name of the input file (e.g., 'test1.txt'): ")
            RushHour(filein)
            
        elif choice == '2':
            manual_play()
        elif choice == '3':
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
