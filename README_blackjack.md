**Blackjack.py README**

**Overview**

blackjack.py simulates a standard game of Las Vegas Blackjack

The game supports:
* Basic hit, stand, split, double down actions
* Blackjack check
* Deck reshuffle when empty
* Multiple types of player options with distinct personalities
* Basic AI strategy suggestions
* Save and Load game state
* Consecutive wins check with potential for complimentary breakfast offer
  
**Dependencies**
* Python Standard Library
* random for random shuffling and choices
* pickle for saving and loading game states
* os for checking file existence
  
**How to Run**

To run the script, you’ll need to input the number of players and buy in amount as arguments e.g. “python3 blackjack.py 1 100” for a one player game with $100 buy in. The default bet size is $5. This can be edited in line 241. The User will then input either “new game” or “load game”. Next, choose a number 1-4 to select your character type. 
The Dealer’s cards are displayed as follows [X, 9?] where X represents the facedown card (note: basic strategy concludes that the User should assume the X is the equivalent of a 10). The User’s cards are both shown faceup. The User then has the option to hit, stand, split, double down, or ask for help. The ‘help’ option provides strategic guidance that has been hardcoded into the script (lines 149-214).

After each hand, the User has the option to play another hand, ‘cash out’, or ‘save’ the game.

**Classes**
* Card: Represents a single card with a suit and value.
* Deck: Contains a standard 52-card deck of Card objects, supports shuffling and drawing.
* Hand: Represents a player's hand of Card objects. Calculates the total value and displays the hand in ASCII art.

**Player**
Allows User to select from 4 different player types (Funny, Villain, Diplomat, and Tourist) as well as the buy-in amount. This snippet also keeps track of hands played and consecutive wins which is used to determine if the User has won a complimentary breakfast. 

**Functions**
* save_game / load_game
Save or load the game state to/from a .pickle file.
* check_consecutive_wins
Checks a player's consecutive wins to potentially offer a complimentary breakfast.
* basic_strategy
Provides basic strategy advice based on the current player's hand and the dealer's face-up card.
* offer_breakfast
Offers complimentary breakfast based on consecutive wins.
* check_blackjack
Checks if a player has a blackjack.
* play_blackjack
The main function that initializes and runs the Blackjack game.

**Future Extensions**
1. Allow for custom bet size between rounds.
2. Debug display of the second hand generated after “split” is called.
3. Multi-threading for faster performance.
   
**Author**
Brock Pluimer
