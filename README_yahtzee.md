Yahtzee! README

Overview

This Python script simulates a game of Yahtzee using ASCII art to display the dice. It supports multiple players, allows you to save and load games, and keeps track of the top 10 scores of all time.

See yahtzee_rules.pdf for a guide on how to play.

How to Run the Script

To run the game, input “python3 yahtzee.py”. Then input the number of players e.g. 1. The result is 5 dice that are automatically rolled. Input the numbers corresponding to the dice *that you want to re-roll*. The other dice will be kept for the next round. Alternatively, if the User wants to keep all dice, simply press Enter. After 3 rounds are completed, or all 5 dice are kept, the User will choose which category to save their score under. Categories 1-6 are considered the “Upper Section” of a traditional Yahtzee! game and standard rules apply. That is, a score of 65 or more in the Upper Section yields a bonus of 35 points. At the end of the game, you'll be prompted to save the game state. Say 'y' to save.

Features
* Multiplayer Support: Allows for multiple players.
* Save and Load: Saves the game state with Pickle, and loads it if available.
* Top Scores: Keeps track of the top 10 scores using JSON.
  
Constants
* DICE_VALUES: Lists the possible dice values (1-6).
* NUM_DICE: Number of dice in the game (5).
* NUM_ROLLS: Number of rolls per turn (3).
* NUM_TURNS: Number of turns per player (13).
* DICE_VISUALS: ASCII art for displaying dice values.
* SCORING_CATEGORIES: Lists the possible scoring categories in the game.
  
Functions
* display_dice(dice): Displays the ASCII art of the dice rolled.
* roll_dice(): Returns a random dice roll.
* score_roll(dice, category): Calculates the score based on the category and dice values.
* save_game(player_scores): Saves the current game state.
* load_game(): Loads a saved game.
* save_scores(player_total_scores): Manages and displays the top scores.
Future Improvements
* Add a graphical user interface (GUI).
* Implement a ‘help’ option to provide basic strategy advice.
  
Author
Brock Pluimer

