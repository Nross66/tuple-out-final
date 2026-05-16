"""
Helper functions for the Tuple Out dice game.
"""

from pathlib import Path

import numpy as np


def roll_dice(amount: int = 3, sides: int = 6) -> list[int]:
    """
    Roll dice using numpy random number generation.
    """
    rolls = np.random.randint(1, sides + 1, size=amount)
    return rolls.tolist()


def check_tuple_out(dice: list[int]) -> bool:
    """
    Return True when all three dice have the same value.
    """
    return dice[0] == dice[1] and dice[1] == dice[2]


def find_fixed_dice(dice: list[int]) -> list[int]:
    """
    Find dice positions that are fixed because two dice have the same value.
    """
    fixed_indexes = []

    for index in range(len(dice)):
        value = dice[index]
        if dice.count(value) == 2:
            fixed_indexes.append(index)

    return fixed_indexes


def ask_yes_no(prompt: str) -> bool:
    """
    Ask the user a yes or no question and return True for yes or False for no.
    """
    while True:
        answer = input(prompt).strip().lower()

        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            print("Please enter yes or no.")


def ask_for_integer(prompt: str, minimum: int, maximum: int) -> int:
    """
    Ask the user for an integer in a specific range.
    """
    while True:
        answer = input(prompt).strip()

        try:
            number = int(answer)

            if number >= minimum and number <= maximum:
                return number
            else:
                print(f"Please enter a number from {minimum} to {maximum}.")
        except ValueError:
            print("Please enter a valid whole number.")


def record_turn(
    turn: int,
    player: str,
    dice: list[int],
    turn_score: int,
    total_score: int,
    tupled_out: bool,
) -> dict:
    """
    Create a dictionary that records one turn.
    """
    dice_tuple = tuple(dice)

    return {
        "turn": turn,
        "player": player,
        "dice": str(dice_tuple),
        "turn_score": turn_score,
        "total_score": total_score,
        "tupled_out": tupled_out,
    }


def get_winner(scores: dict[str, int]) -> tuple[str, int]:
    """
    Return the winning player and score.
    """
    winner = ""
    winning_score = -1

    for player, score in scores.items():
        if score > winning_score:
            winner = player
            winning_score = score

    return winner, winning_score


def save_turn_history(filename: str, turn_history: list[dict]) -> None:
    """
    Save every turn to a CSV file using string writing.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("turn,player,dice,turn_score,total_score,tupled_out\n")

        for record in turn_history:
            row = (
                f"{record['turn']},"
                f"{record['player']},"
                f'"{record["dice"]}",'
                f"{record['turn_score']},"
                f"{record['total_score']},"
                f"{record['tupled_out']}\n"
            )
            file.write(row)


def save_game_summary(filename: str, scores: dict[str, int], winner: str) -> None:
    """
    Add a readable game summary to a text file.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write("New Tuple Out Game\n")

        for player, score in scores.items():
            file.write(f"{player}: {score}\n")

        file.write(f"Winner: {winner}\n")
        file.write("\n")


def load_previous_results(filename: str) -> list[str]:
    """
    Read previous game results from a text file when the file exists.
    """
    path = Path(filename)

    if not path.exists():
        return []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines[-10:]
