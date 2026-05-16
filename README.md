# Tuple Out Final Project

## Overview

This project is a Python version of the dice game Tuple Out.

Players take turns rolling three dice. If all three dice show the same value, the player tuples out and earns 0 points for that turn. If two dice show the same value, those dice are fixed and cannot be rerolled for the rest of the turn. The player can keep rerolling any dice that are not fixed, or they can stop and add the dice total to their score.

The winner is the player with the highest total score after the selected number of turns.

## How to Run the Program

Open a terminal in this project folder and run:

```bash
python tuple_out.py
```

Then follow the prompts in the terminal.

## Required Libraries

This project uses these libraries:

```bash
pip install numpy pandas seaborn matplotlib
```

## Files Included

| File | Purpose |
| --- | --- |
| `tuple_out.py` | Main game file |
| `game_utils.py` | Helper functions for dice rolling, scoring, file saving, and input checking |
| `scores.txt` | Stores readable game summaries after games are played |
| `game_results.csv` | Stores the turn history from the most recent game |
| `score_graph.png` | Graph created after a game is played |
| `requirements.txt` | List of required Python packages |

## Game Rules

1. Each player starts their turn by rolling three dice.
2. If all three dice match, the player tuples out and scores 0 points for that turn.
3. If two dice match, those dice become fixed.
4. Fixed dice cannot be rerolled.
5. The player may reroll available dice or stop.
6. If the player stops, the values of all three dice are added to their total score.
7. After all turns are complete, the player with the highest score wins.

## Features

This version includes:

* Multiple players
* User selected number of turns
* User selected number of sides on the dice
* Dice rolling with `numpy`
* Score tracking with a dictionary
* Turn history stored in a list of dictionaries
* Tuple use when saving dice results
* File reading from `scores.txt`
* File writing to `scores.txt`
* CSV writing to `game_results.csv`
* A graph of scores over time using `seaborn`
* Input checking with `try` and `except`

## Known Limits

This version decides the winner by highest score. If two players tie, the program keeps the first player who reached that score as the winner.

## Pattern Checklist Notes

This project includes examples of variables, functions, function arguments, named arguments, object methods, a standard library import, a local module import, input, file reading, file writing, conditionals, boolean operators, boolean functions, error handling, while loops, for loops, lists, indexing, dictionaries, tuples, comments, docstrings, and a README file.

The project also includes advanced coding topics by using `numpy` for dice rolling and `seaborn` with `pandas` for graphing score data.
