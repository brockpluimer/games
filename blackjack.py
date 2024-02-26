#!/usr/bin/env python

import random
import pickle
import os

class Card:
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f'{self.value}{Card.symbols[self.suit]}'

    def get_value(self):
        if self.value in ('J', 'Q', 'K'):
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:  # Check if the deck is empty
            self.cards = [Card(suit, value) for suit in Card.suits for value in Card.values]  # Create a new deck
            random.shuffle(self.cards)  # Shuffle the new deck
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(card.get_value() for card in self.cards)
        aces = sum(card.value == 'A' for card in self.cards)

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def __repr__(self):
        lines = [[] for _ in range(8)]
        
        for card in self.cards:
            lines[1].append('┌─────────┐')
            lines[2].append(f'│ {card.value:<2}      │')
            lines[3].append('│         │')
            lines[4].append(f'│    {card.symbols[card.suit]}    │')
            lines[5].append('│         │')
            lines[6].append(f'│      {card.value:>2} │')
            lines[7].append('└─────────┘')
        return '\n'.join(' '.join(line) for line in lines)

    def to_ascii(self):
        ascii_cards = []
        for card in self.cards:
            card_lines = [
                '┌─────────┐',
                f'│ {card.value:<2}      │',
                '│         │',
                f'│    {card.symbols[card.suit]}    │',
                '│         │',
                f'│      {card.value:>2} │',
                '└─────────┘',
            ]
            ascii_cards.append(card_lines)
        return '\n'.join(' '.join(cards[i] for cards in ascii_cards) for i in range(len(card_lines)))


class Player:
    funny_names = ['Dr. Chuckles', 'Sir Laughsalot', 'Miss Giggles', 'Captain Chucklehead', 'Madame Hilarity']
    villian_names = ['The Joker', 'Darth Vader', 'Lord Voldemort', 'Sauron', 'The Wicked Witch of the West']
    diplomat_names = ['Charlemagne Bautista','His Excellent Holiness Charles Hammington III', 'Her Exalted Grace Lady Eleanora von Wittenstein', 'His Serene Majesty Archduke Bartholomew von Gutenberg']
    
    basic_names = ['Tom', 'Linda', 'Earl', 'Emily', 'Jack', 'Molly', 'Tim', 'Sophia', 'Max', 'Grace']
    us_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin']

    def __init__(self, buy_in_amount, player_type='funny'):
        self.player_type = player_type
        self.name = self.generate_name(player_type)
        self.buy_in_amount = buy_in_amount
        self.hands = [Hand()]
        self.consecutive_wins = 0

    def generate_name(self, player_type):
        if player_type == 'funny':
            return random.choice(self.funny_names)
        elif player_type == 'villian':
            return random.choice(self.villian_names)
        elif player_type == 'diplomat':
            return random.choice(self.diplomat_names)
        elif player_type == 'tourist':
            name = random.choice(self.basic_names)
            city = random.choice(self.us_cities)
            return f'{name} from {city}'
        else:
            raise ValueError(f"Invalid player type: {player_type}")

    def __repr__(self):
        return f'{self.name} ({self.buy_in_amount}$)'

    def split_hand(self, hand_index, deck):
        hand = self.hands[hand_index]
        if len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
            new_hand = Hand()
            new_hand.add_card(hand.cards.pop())
            self.hands.append(new_hand)
            hand.add_card(deck.draw())
            new_hand.add_card(deck.draw())
            return True
        return False


def save_game(game_state, filename):
    with open(filename, 'wb') as file:
        pickle.dump(game_state, file)

def load_game(filename):
    if not os.path.exists(filename):
        return None

    with open(filename, 'rb') as file:
        game_state = pickle.load(file)
    return game_state

def check_consecutive_wins(player):
    min_wins_for_breakfast = 3
    breakfast_probability = .2

    if player.consecutive_wins >= min_wins_for_breakfast:
        if random.random() < breakfast_probability:
            offer_breakfast(player)

def basic_strategy(player_hand, dealer_up_card):
    player_value = player_hand.get_value()
    dealer_value = dealer_up_card.get_value()
    soft = any(card.value == 'A' for card in player_hand.cards) and player_value <= 21
    
    if len(player_hand.cards) == 2 and player_hand.cards[0].get_value() == player_hand.cards[1].get_value():
        pair = player_hand.cards[0].get_value()

        if pair == 11:
            return "....omg you idiot! Always split aces! It's like doubling down on 11"
        if pair == 8:
            return 'split, duh'
        elif pair == 2 or pair == 3:
            if dealer_value in (2, 3, 4, 7, 8):
                return 'split'
            else:
                return 'hit'
        elif pair == 6:
            if dealer_value in (2, 3, 4, 5, 6):
                return 'split'
            else:
                return 'hit'
        elif pair == 7:
            if dealer_value in (2, 3, 4, 5, 6, 7):
                return 'split'
            else:
                return 'hit'
        elif pair == 9:
            if dealer_value in (2, 3, 4, 5, 6, 8, 9):
                return 'split'
            else:
                return 'hit'
        else:
            return 'stand'

    if player_value == 11 and len(player_hand.cards) == 2:
        return "...omg you idiot! Always double down on 11! It's like splitting aces"

    if soft:
        if player_value <= 17:
            return 'hit'
        elif player_value == 18:
            if dealer_value in (2, 7, 8):
                return 'stand'
            else:
                return 'hit'
        else:
            return 'stand'
    else:
        if player_value <= 11:
            if player_value == 11:
                return 'double down'
            else:
                return 'hit'
        elif player_value == 12:
            if dealer_value in (4, 5, 6):
                return 'stand'
            else:
                return 'hit'
        elif player_value <= 16:
            if dealer_value >= 7:
                return 'hit'
            else:
                return 'stand'
        else:
            return 'stand'

def offer_breakfast(player):
    print(f"Wow! Look at the big winner in the casino! {player.name}, would you like to have some complimentary breakfast? (yes/no)")
    while True:
        response = input().lower()
        if response == 'yes':
            print("Enjoy your complimentary breakfast!")
            break
        elif response == 'no':
            print("Alright, have fun at the tables!")
            break
        else:
            print("Please type 'yes' or 'no'.")

def check_blackjack(player, cost_per_round):
    for hand in player.hands:
        if len(hand.cards) == 2 and hand.get_value() == 21:
            payout = cost_per_round * 1.5
            player.buy_in_amount += payout
            player.consecutive_wins += 1
            check_consecutive_wins(player)
            print(f'{player.name} got a blackjack! (Payout: {payout}$) 🎉')
            return True
    return False

def play_blackjack(num_players, buy_in_amount, load_saved_game=False):
    cost_per_round = 5 #############################################CHANGE BET SIZE HERE###############################
    round_number = 1
    if load_saved_game:
        save_name = input("Please enter the save name: ")
        game_state = load_game(f"blackjack_save_{save_name}.pickle")
        if game_state is None:
            print("Save not found.")
            return
        players, dealer, deck = game_state
    else:
        player_types = ['funny', 'villian', 'diplomat', 'tourist']
        print("Please choose your player type: ")
        for i, player_type in enumerate(player_types):
            print(f"{i + 1}. {player_type.capitalize()}")
        while True:
            try:
                choice = int(input("Enter the number corresponding to your choice: ")) - 1
                if 0 <= choice < len(player_types):
                    chosen_player_type = player_types[choice]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        players = [Player(buy_in_amount, player_type=chosen_player_type) for _ in range(num_players)]
        dealer = Player(0)
        dealer.name = 'Dealer'
        deck = Deck()

    while True:
        print(f"Round {round_number}:")
        print('-' * 30)

        for player in players + [dealer]:
            player.hands = [Hand()]
            for hand in player.hands:
                hand.add_card(deck.draw())
                hand.add_card(deck.draw())

        for player in players:
            if player.buy_in_amount <= 0:
                print(f"{player.name}, GAME OVER YOU DEGENERATE")
                players.remove(player)  # Remove the player with no money from the game

        if not players:  # If there are no more players left in the game
            print("All players are out. Game over.")
            break

        print(f"Dealer's hand: [X, {dealer.hands[0].cards[1]}]")


        for player in players:
            for hand_index, hand in enumerate(player.hands):
                if check_blackjack(player, cost_per_round):
                    print(f"{player.name} got a Blackjack! Hooray! 🎉")
                    player.consecutive_wins += 1
                    check_consecutive_wins(player)
                    continue
                print(f'{player}: {hand}')
                
                bust = False
                while True:
                    action = input(f"{player.name}, do you want to 'hit', 'stand', 'split', 'double down', or type 'help' for advice? ").lower()
                    if action in ('hit','h'):
                        hand.add_card(deck.draw())
                        print(hand)
                        if hand.get_value() > 21:
                            print(f'{player.name} busts!')
                            bust = True
                            break
                    elif action in ('s','stand'):
                        break
                    elif action in ('p','split'):
                        if player.split_hand(hand_index, deck):
                            for i, hand in enumerate(player.hands):
                                print(f"{player} hand {i+1}: {hand}")
                        else:
                            print("Cannot split this hand.")
                    elif action in ('dd','double down'):
                        if len(hand.cards) == 2:
                            hand.add_card(deck.draw())
                            print(hand)
                            player.buy_in_amount -= cost_per_round
                            payout = cost_per_round * 2
                            player.buy_in_amount += payout
                            break
                    elif action == 'help':
                        advice = basic_strategy(hand, dealer.hands[0].cards[1])
                        print(f"Based on basic strategy, you should {advice}.")
                    else:
                        print("Invalid input. Please type 'hit', 'stand', 'split', 'double down', or 'help'.")

                    if hand.get_value() > 21:
                        break
                
        dealer_hand = dealer.hands[0]
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.draw())

        print(f"Dealer's hand: {dealer_hand}")

        for player in players:
            for hand in player.hands:
                player_value = hand.get_value()
                dealer_value = dealer_hand.get_value()
                if player_value > 21:
                    print(f'{player.name} loses!')
                    player.buy_in_amount -= cost_per_round
                else:
                    if dealer_value > 21 or player_value > dealer_value:
                        payout = cost_per_round * 1.5 if player_value == 21 and len(hand.cards) == 2 else cost_per_round
                        print(f'{player.name} wins! (Payout: {payout}$)')
                        player.buy_in_amount += payout
                        player.consecutive_wins += 1
                        check_consecutive_wins(player)
                        print("Winning hand:")
                        print(hand.to_ascii())
                    elif player_value == dealer_value:
                        print()
                        print(f'{player.name} ties with the dealer!')
                        print()
                        player.consecutive_wins = 0
                    else:
                        print()
                        print(f'{player.name} loses!')
                        print()
                        player.consecutive_wins = 0
                        player.buy_in_amount -= cost_per_round

        round_number += 1

        action = input("Type 'cash out' to end the game, 'save' to save and exit, or press Enter to play again: ").lower()
        if action == 'cash out':
            break
        elif action == 'save':
            save_name = input("Please enter a save name: ")
            save_game((players, dealer, deck), f"blackjack_save_{save_name}.pickle")
            break

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print()
        print("Usage: python blackjack.py <number_of_players> <buy_in_amount>")
        print()
        sys.exit(1)

    try:
        num_players = int(sys.argv[1])
        buy_in_amount = int(sys.argv[2])
    except ValueError:
        print()
        print("Invalid arguments. Both number_of_players and buy_in_amount should be integers.")
        print()
        sys.exit(1)

    while True:
        print()
        game_action = input("Welcome to Vegas Baby! Type 'new game' to start a new game or 'load game' to load a saved game: ").lower()
        print()
        if game_action == 'new game':
            play_blackjack(num_players, buy_in_amount)
            break
        elif game_action == 'load game':
            play_blackjack(num_players, buy_in_amount, load_saved_game=True)
            break
        else:
            print()
            print("Invalid input. Please type 'new game' or 'load game'.")
            print()
