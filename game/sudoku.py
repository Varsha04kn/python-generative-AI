import random
from copy import deepcopy

BOARD_SIZE = 9
SUBGRID = 3


def valid(board, row, col, num):
    """Check whether it's valid to place num at (row, col)."""
    if any(board[row][c] == num for c in range(BOARD_SIZE)):
        return False
    if any(board[r][col] == num for r in range(BOARD_SIZE)):
        return False

    start_row = (row // SUBGRID) * SUBGRID
    start_col = (col // SUBGRID) * SUBGRID
    for r in range(start_row, start_row + SUBGRID):
        for c in range(start_col, start_col + SUBGRID):
            if board[r][c] == num:
                return False
    return True


def generate_full_board():
    """Generate a full valid 9x9 Sudoku board."""
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    numbers = list(range(1, BOARD_SIZE + 1))

    def backtrack(cell=0):
        if cell == BOARD_SIZE * BOARD_SIZE:
            return True
        row, col = divmod(cell, BOARD_SIZE)
        random.shuffle(numbers)
        for num in numbers:
            if valid(board, row, col, num):
                board[row][col] = num
                if backtrack(cell + 1):
                    return True
                board[row][col] = 0
        return False

    backtrack()
    return board


def remove_cells(board, removals=40):
    """Remove a number of cells from a full board to make a puzzle."""
    puzzle = deepcopy(board)
    removed = 0
    attempts = removals * 3
    while removed < removals and attempts > 0:
        row = random.randrange(BOARD_SIZE)
        col = random.randrange(BOARD_SIZE)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            removed += 1
        attempts -= 1
    return puzzle


def print_board(board):
    """Print the board in a readable format."""
    line = "+-------+-------+-------+"
    print(line)
    for i, row in enumerate(board):
        row_str = "| "
        for j, value in enumerate(row):
            row_str += str(value) if value != 0 else "."
            row_str += " "
            if (j + 1) % SUBGRID == 0:
                row_str += "| "
        print(row_str)
        if (i + 1) % SUBGRID == 0:
            print(line)


def is_solved(board):
    """Check whether the board is completely filled."""
    return all(all(cell != 0 for cell in row) for row in board)


def play_sudoku(mistakes_allowed=5, removals=40):
    """Create and play a Sudoku game in the console."""
    solution = generate_full_board()
    puzzle = remove_cells(solution, removals=removals)
    mistakes = 0

    print("Welcome to Sudoku! Enter moves as row,col,value (1-9).")
    print(f"You may make up to {mistakes_allowed} mistakes.")

    while mistakes < mistakes_allowed and not is_solved(puzzle):
        print_board(puzzle)
        entry = input("Enter row,col,value or 'q' to quit: ").strip()
        if entry.lower() == "q":
            print("Game ended by user.")
            return

        try:
            row_str, col_str, value_str = [part.strip() for part in entry.split(",")]
            row = int(row_str) - 1
            col = int(col_str) - 1
            value = int(value_str)
        except (ValueError, TypeError):
            print("Invalid input format. Use row,col,value with numbers 1-9.")
            continue

        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and 1 <= value <= BOARD_SIZE):
            print("Row, column, and value must be between 1 and 9.")
            continue
        if puzzle[row][col] != 0:
            print("Cell already filled. Choose an empty cell.")
            continue
        if solution[row][col] == value:
            puzzle[row][col] = value
            print("Good move!")
        else:
            mistakes += 1
            remaining = mistakes_allowed - mistakes
            print(f"Wrong number. Mistakes left: {remaining}")

    print_board(puzzle)
    if is_solved(puzzle):
        print("Congratulations! You solved the puzzle.")
    else:
        print("Game over. You reached the mistake limit.")
        print("The correct solution was:")
        print_board(solution)


if __name__ == "__main__":
    play_sudoku()
