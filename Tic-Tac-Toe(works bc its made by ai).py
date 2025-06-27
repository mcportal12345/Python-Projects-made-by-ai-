import sys 
def print_board(board):
    # function for the grid
    print("   1   2   3") # shows the numbers beside colums and rows for accesibility
    for i, row in enumerate(board, 1):
        print(f"{i}  " + " | ".join(row))
        if i < 3:
            print("  ---+---+---") # prints the grid
def rematch():
        choice = input("rematch?? (yes or no):") # lets the player choose if they want to play again
        if choice == "yes": # what happens if the player wants to play again
            main()
        if choice == "no": # what happens if the players dont want to play again
            print("Thanks for playing") # goodbye message
            sys._ExitCode # make the code terminalte
def check_win(board, player):
    # Check rows, columns, and diagonals for "X" or "O"
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = [[" " for _ in range(3)] for _ in range(3)] # defines what the board is
    current_player = "X" # what the current player is
    while True:
        print_board(board) # prints out the board/grid 
        try:
            move = input(f"Player {current_player}, enter row and column (e.g., 1 3): ") # asks the player where they want to put the "X" or "O"
            row, col = map(int, move.strip().split())
            if not (1 <= row <= 3 and 1 <= col <= 3):
                print("Row and column must be between 1 and 3.") # if the player puts in an incorrect input e.g. 1 4
                continue
            if board[row-1][col-1] != " ": 
                print("Cell already taken. Try again.") # if the player tries to put a "X" or "O" in a cell that is already taken
                continue
            board[row-1][col-1] = current_player
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break
            if is_full(board): # checks if the board is full aka a draw
                print_board(board)
                print("It's a draw!")
                break
            current_player = "O" if current_player == "X" else "X" # determines what player goes next
        except ValueError:
            print("Invalid input. Please enter row and column numbers separated by a space.")

if __name__ == "__main__":
    main() # calls the main function 
    rematch() # calls the rematch function 
    rematch() # calls the rematch function again to make the game best of three
    choice = input ("Who won more games X or O(use capitals):")
    if choice == "X":
        print("Well done although since you startted first in all the games winning is whats expected")
    if choice == "O":
        print("Wow you managed to beat X even though you started second you either are really good or X is just bad")