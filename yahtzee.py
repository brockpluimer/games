import random
import pickle
import json

# Possible dice values
DICE_VALUES = [1, 2, 3, 4, 5, 6]

# Number of dice in the game
NUM_DICE = 5

# Number of rolls per turn
NUM_ROLLS = 3

# Number of turns per player
NUM_TURNS = 13

# ASCII visuals for dice
DICE_VISUALS = {
    1: '''
  
 |       |
 |   *   |
 |       |
  ''',

    2: '''
  
 | *     |
 |       |
 |     * |
  ''',

    3: '''
  
 | *     |
 |   *   |
 |     * |
  ''',

    4: '''
  
 | *   * |
 |       |
 | *   * |
  ''',

    5: '''
  
 | *   * |
 |   *   |
 | *   * |
  ''',

    6: '''
  
 | *   * |
 | *   * |
 | *   * |
  '''
}


SCORING_CATEGORIES = [
    "ones", "twos", "threes", "fours", "fives", "sixes",
    "three_of_a_kind", "four_of_a_kind", "full_house",
    "small_straight", "large_straight", "yahtzee", "chance"
]

def display_dice(dice):
    dice_lines = [DICE_VISUALS[d].split("\n")[1:-1] for d in dice]
    print("")  # Add a blank line before the dice
    for i in range(len(dice_lines[0])):
        print(" ".join(line[i] for line in dice_lines))
    print("")  # Add a blank line after the dice


def roll_dice():
    return random.choice(DICE_VALUES)

def display_dice(dice):
    dice_lines = [DICE_VISUALS[d].split("\n")[1:-1] for d in dice]
    for i in range(len(dice_lines[0])):
        print(" ".join(line[i] for line in dice_lines))

def score_roll(dice, category):
    counts = [dice.count(i) for i in range(1, 7)]
    category_idx = SCORING_CATEGORIES.index(category)

    if 0 <= category_idx < 6:
        return counts[category_idx] * (category_idx + 1)
    elif category == "three_of_a_kind":
        return sum(dice) if max(counts) >= 3 else 0
    elif category == "four_of_a_kind":
        return sum(dice) if max(counts) >= 4 else 0
    elif category == "full_house":
        return 25 if 3 in counts and 2 in counts else 0
    elif category == "small_straight":
        sorted_dice = sorted(dice)
        return 30 if any(sorted_dice[i:i+4] == list(range(n, n+4)) for i in range(2) for n in range(1, 4)) else 0
    elif category == "large_straight":
        sorted_dice = sorted(dice)
        return 40 if any(sorted_dice == list(range(n, n+5)) for n in range(1, 3)) else 0
    elif category == "yahtzee":
        return 50 if max(counts) == 5 else 0
    elif category == "chance":
        return sum(dice)


def save_game(player_scores, filename='yahtzee_save.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(player_scores, f)

def load_game(filename='yahtzee_save.pkl'):
    try:
        with open(filename, 'rb') as f:
            player_scores = pickle.load(f)
        return player_scores
    except FileNotFoundError:
        return None

def save_scores(player_total_scores):
    top_scores_file = "top_scores.json"

    try:
        with open(top_scores_file, "r") as f:
            top_scores = json.load(f)
    except FileNotFoundError:
        top_scores = []

    # Update the top scores list with the new scores
    top_scores.extend(player_total_scores)
    top_scores.sort(reverse=True)
    top_scores = top_scores[:10]

    # Save the updated top scores list
    with open(top_scores_file, "w") as f:
        json.dump(top_scores, f)

    print("\nTop 10 scores of all time:")
    for i, score in enumerate(top_scores, start=1):
        print(f"{i}. {score}")

def main():
    num_players = int(input("Enter the number of players: "))

    # Load saved game data, if any
    player_scores = load_game()
    if player_scores is None:
        player_scores = [
            {category: None for category in SCORING_CATEGORIES}
            for _ in range(num_players)
        ]

    print("\nWelcome to ASCII Yahtzee!\n")

    for turn in range(NUM_TURNS):
        for player_idx in range(num_players):
            print(f"Player {player_idx + 1}'s turn:\n")

            dice = [roll_dice() for _ in range(NUM_DICE)]
            display_dice(dice)

            for roll_num in range(1, NUM_ROLLS):
                reroll_indices = input(f"\nRoll {roll_num}/3. Enter dice to reroll (1-5), or press Enter to keep: ")
                if reroll_indices:
                    for idx in reroll_indices:
                        if idx.isdigit() and 1 <= int(idx) <= NUM_DICE:
                            dice[int(idx) - 1] = roll_dice()
                    display_dice(dice)
                else:
                    break

            # Choose a scoring category
            while True:
                print("\nScoring categories:")
                for idx, category in enumerate(SCORING_CATEGORIES, start=1):
                    if player_scores[player_idx][category] is None:
                        print(f"{idx}. {category.capitalize()}")
                chosen_category = int(input("Choose a scoring category (1-13): ")) - 1
                category = SCORING_CATEGORIES[chosen_category]
                if player_scores[player_idx][category] is None:
                    break

            # Score the roll
            score = score_roll(dice, category)
            player_scores[player_idx][category] = score
            print(f"\nYou scored {score} points in the {category.capitalize()} category.\n")

    # Calculate and display final scores
    player_total_scores = []
    print("\nFinal scores:")
    for player_idx in range(num_players):
        upper_section = sum(
            player_scores[player_idx][category] for category in SCORING_CATEGORIES[:6]
        )
        upper_bonus = 35 if upper_section >= 63 else 0
        lower_section = sum(
            player_scores[player_idx][category] for category in SCORING_CATEGORIES[6:]
        )
        total_score = upper_section + upper_bonus + lower_section

        print(f"\nPlayer {player_idx + 1}:")
        print("Upper Section:")
        for category in SCORING_CATEGORIES[:6]:
            print(f"{category.capitalize()}: {player_scores[player_idx][category]}")
        print(f"Upper Section Total: {upper_section}")
        print(f"Upper Section Bonus: {upper_bonus}")

        print("\nLower Section:")
        for category in SCORING_CATEGORIES[6:]:
            print(f"{category.capitalize()}: {player_scores[player_idx][category]}")
        print(f"Lower Section Total: {lower_section}")

        print(f"\nTotal Score: {total_score}")

        player_total_scores.append(total_score)

    # Ask to save the game at the end
    save_game = input("\nDo you want to save the game? (y/n): ").lower().strip()
    if save_game == "y":
        save_scores(player_total_scores)

if __name__ == "__main__":
    main()
