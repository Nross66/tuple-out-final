"""
Tuple Out final project main file.

Run this file with:
python tuple_out.py
"""

import sys
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from game_utils import (
    ask_for_integer,
    ask_yes_no,
    check_tuple_out,
    find_fixed_dice,
    get_winner,
    load_previous_results,
    record_turn,
    roll_dice,
    save_game_summary,
    save_turn_history,
)


RESULTS_FILE = "game_results.csv"
SUMMARY_FILE = "scores.txt"
GRAPH_FILE = "score_graph.png"


def play_turn(player_name, dice_sides):
    """
    Play one full turn for one player.

    A player starts by rolling three dice. If all three match, the player tuples out.
    If two dice match, those dice are fixed. The player may reroll dice that are not fixed.
    """
    print(f"\n{player_name}'s turn")
    dice = roll_dice(3, dice_sides)
    fixed_indexes = []

    while True:
        print(f"Current dice: {dice}")

        if check_tuple_out(dice):
            print(f"{player_name} tupled out and scored 0 points this turn.")
            return 0, dice, True

        fixed_indexes = find_fixed_dice(dice)

        if fixed_indexes:
            fixed_display = [index + 1 for index in fixed_indexes]
            print(f"Fixed dice positions: {fixed_display}")
        else:
            print("No dice are fixed right now.")

        available_indexes = []
        for index in range(len(dice)):
            if index not in fixed_indexes:
                available_indexes.append(index)

        if not available_indexes:
            turn_score = sum(dice)
            print(f"All dice are fixed. {player_name} scores {turn_score} points.")
            return turn_score, dice, False

        keep_rolling = ask_yes_no("Do you want to reroll the available dice? yes or no: ")

        if not keep_rolling:
            turn_score = sum(dice)
            print(f"{player_name} stopped and scored {turn_score} points.")
            return turn_score, dice, False

        print("Available dice positions:")
        for index in available_indexes:
            print(f"{index + 1}: current value {dice[index]}")

        choice = input("Enter dice positions to reroll, separated by spaces, or type all: ").strip().lower()

        if choice == "all":
            indexes_to_reroll = available_indexes
        else:
            indexes_to_reroll = []
            parts = choice.split()

            for part in parts:
                try:
                    position = int(part) - 1
                    if position in available_indexes:
                        indexes_to_reroll.append(position)
                    else:
                        print(f"Position {part} is not available, so it was ignored.")
                except ValueError:
                    print(f"{part} is not a number, so it was ignored.")

        if not indexes_to_reroll:
            print("No valid dice were selected. The available dice will be rerolled.")
            indexes_to_reroll = available_indexes

        new_values = roll_dice(len(indexes_to_reroll), dice_sides)

        for place, index in enumerate(indexes_to_reroll):
            dice[index] = new_values[place]


def make_score_graph(turn_history):
    """
    Create a seaborn line graph of player scores over time.
    """
    if not turn_history:
        print("No turn history was available, so no graph was created.")
        return

    frame = pd.DataFrame(turn_history)

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=frame, x="turn", y="total_score", hue="player", marker="o")
    plt.title("Tuple Out Scores Over Time")
    plt.xlabel("Turn")
    plt.ylabel("Total Score")
    plt.tight_layout()
    plt.savefig(GRAPH_FILE)
    plt.close()

    print(f"A score graph was saved as {GRAPH_FILE}.")


def play_game():
    """
    Run a complete Tuple Out game.
    """
    print("Welcome to Tuple Out")
    print("Try to score points without rolling three matching dice.")

    previous_results = load_previous_results(SUMMARY_FILE)
    if previous_results:
        print("\nPrevious game summaries:")
        for line in previous_results:
            print(line.strip())

    player_count = ask_for_integer("\nHow many players? Enter at least 2: ", 2, 6)
    max_turns = ask_for_integer("How many turns should each player get? Enter 1 to 20: ", 1, 20)
    dice_sides = ask_for_integer("How many sides should each die have? Enter 4 to 20: ", 4, 20)

    players = []
    for number in range(player_count):
        name = input(f"Enter player {number + 1} name: ").strip()
        if name == "":
            name = f"Player {number + 1}"
        players.append(name)

    scores = {}
    for player in players:
        scores[player] = 0

    turn_history = []

    for turn in range(1, max_turns + 1):
        print(f"\nTurn {turn} of {max_turns}")

        for player in players:
            turn_score, final_dice, tupled_out = play_turn(player, dice_sides)
            scores[player] += turn_score

            record = record_turn(
                turn,
                player,
                final_dice,
                turn_score,
                scores[player],
                tupled_out,
            )
            turn_history.append(record)

            print("\nCurrent scores:")
            for name, score in scores.items():
                print(f"{name}: {score}")

    winner, winning_score = get_winner(scores)

    print("\nGame over")
    print(f"Winner: {winner} with {winning_score} points")

    save_turn_history(RESULTS_FILE, turn_history)
    save_game_summary(SUMMARY_FILE, scores, winner)
    make_score_graph(turn_history)

    print(f"Turn history was saved in {RESULTS_FILE}.")
    print(f"Game summary was saved in {SUMMARY_FILE}.")


def main():
    """
    Start the game.

    The command line argument demo can be used to quickly run the normal program.
    Example:
    python tuple_out.py demo
    """
    if len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print("Run the game with: python tuple_out.py")
        print("Then follow the prompts in the terminal.")
    else:
        play_game()


if __name__ == "__main__":
    main()
