#!/usr/bin/env python3
"""
Classic Arcade Tic-Tac-Toe Game
A simple text-based tic-tac-toe game with arcade-style presentation.
"""

import os
import sys

def clear_screen():
    """Clear the terminal screen for a fresh display."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print("=" * 50)
    print("         TIC-TAC-TOE ARCADE")
    print("=" * 50)
    print()

def display_board(board):
    """Display the tic-tac-toe board."""
    print("     1   2   3")
    print("   +---+---+---+")
    for i, row in enumerate(board):
        print(f"{i+1}  | {' | '.join(cell if cell != ' ' else ' ' for cell in row)} |")
        if i < 2:
            print("   +---+---+---+")
    print()

def get_player_move(board, player):
    """Get a valid move from the player."""
    while True:
        try:
            move = input(f"Player {player}, enter your move (row col): ").strip()
            row, col = map(int, move.split())
            if 1 <= row <= 3 and 1 <= col <= 3:
                if board[row-1][col-1] == ' ':
                    return row-1, col-1
                else:
                    print("That spot is already taken!")
            else:
                print("Invalid coordinates! Use 1-3 for both row and column.")
        except ValueError:
            print("Invalid input! Please enter two numbers separated by space.")

def check_winner(board):
    """Check if there's a winner or if it's a draw."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    # Check for draw
    if all(cell != ' ' for row in board for cell in row):
        return 'Draw'

    return None

def play_game():
    """Main game loop."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = 0

    clear_screen()
    print_header()

    while True:
        display_board(board)
        row, col = get_player_move(board, players[current_player])
        board[row][col] = players[current_player]

        winner = check_winner(board)
        if winner:
            clear_screen()
            print_header()
            display_board(board)
            if winner == 'Draw':
                print("It's a draw! Good game!")
            else:
                print(f"Player {winner} wins! Congratulations!")
            break

        current_player = 1 - current_player  # Switch player

def main():
    """Main function to run the game."""
    while True:
        play_game()
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()