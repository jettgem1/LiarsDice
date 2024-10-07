import random
import sys
import os
import time
import math
from typing import List, Tuple, Union
from api import get_liars_dice_completion, initialize_agent, Bet


import math
from typing import List, Tuple


def calculate_liars_dice_probabilities(
    total_dice: int,
    current_bid: Tuple[int, int],
    your_dice: List[int]
):
    """
    Calculates:
    1. Probability that the current bid is true (after considering your own dice)
    2. Expected total number of the bid's face value (including ones) on the table (including your own dice)
    3. Probability of your own best possible valid bet

    Parameters:
    - total_dice (int): Total number of dice on the table
    - current_bid (Tuple[int, int]): The current bid as (quantity, face_value)
    - your_dice (List[int]): Your own dice

    Returns:
    - current_bid_probability (float): Probability that the current bid is true
    - expected_total (float): Expected total number of the bid's face value (including ones)
    - best_bid_probability (float): Probability of your own best valid bet
    - best_bid (Tuple[int, int]): The best possible valid bet
    """
    quantity, face_value = current_bid
    num_unknown_dice = total_dice - len(your_dice)

    # Count matching dice in your own hand (do not double-count ones)
    your_matching_dice = sum(
        1 for die in your_dice if die == face_value or die == 1)

    # Adjust the required quantity from unknown dice
    required_from_unknown = quantity - your_matching_dice
    if required_from_unknown < 0:
        required_from_unknown = 0  # The bid is already met with your own dice

    # Probability that a single unknown die matches (ones are wild)
    # Probability of die being face_value or 1 (do not double-count ones)
    p = 2 / 6

    # Expected number of matching dice from unknown dice
    expected_from_unknown = num_unknown_dice * p

    # Expected total number including your own matching dice
    expected_total = expected_from_unknown + your_matching_dice

    # Calculate probability that at least 'required_from_unknown' matches in unknown dice
    current_bid_probability = 0.0
    for k in range(required_from_unknown, num_unknown_dice + 1):
        combinations = math.comb(num_unknown_dice, k)
        probability = combinations * \
            (p ** k) * ((1 - p) ** (num_unknown_dice - k))
        current_bid_probability += probability

    # Now, determine your best possible valid bet
    # Find the valid bet with the highest probability of being true
    # Start from the minimum valid bet and iterate upwards
    # The new bid must be higher in quantity or face value or both
    best_bid = None
    best_bid_probability = 0.0

    # Generate all possible valid bets
    valid_bets = []
    for q in range(quantity, total_dice + 1):
        for f in range(face_value + 1 if q == quantity else 1, 7):
            if q == quantity and f <= face_value:
                continue  # Must increase quantity or face value or both
            valid_bets.append((q, f))

    # Evaluate each valid bet
    for bid_q, bid_face in valid_bets:
        # Count your matching dice for the new bid
        your_bid_matching = sum(
            1 for die in your_dice if die == bid_face or die == 1)
        required_from_unknown_bid = bid_q - your_bid_matching
        if required_from_unknown_bid < 0:
            required_from_unknown_bid = 0

        # Probability that a single unknown die matches the new bid
        p_bid = 2 / 6  # Same probability since ones are wild

        # Calculate probability for the new bid
        bid_probability = 0.0
        for k in range(required_from_unknown_bid, num_unknown_dice + 1):
            combinations = math.comb(num_unknown_dice, k)
            probability = combinations * \
                (p_bid ** k) * ((1 - p_bid) ** (num_unknown_dice - k))
            bid_probability += probability

        # Keep track of the best bid (highest probability or highest quantity if probabilities are equal)
        if (bid_probability > best_bid_probability) or \
           (bid_probability == best_bid_probability and bid_q > (best_bid[0] if best_bid else 0)) or \
           (bid_probability == best_bid_probability and bid_face > (best_bid[1] if best_bid else 0)):
            best_bid_probability = bid_probability
            best_bid = (bid_q, bid_face)

    return current_bid_probability, expected_total, best_bid_probability, best_bid


class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.dice = [random.randint(1, 6) for _ in range(5)]
        self.is_ai = is_ai
        self.messages = initialize_agent() if is_ai else ""  # For AI players

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(len(self.dice))]

    def lose_die(self):
        if self.dice:
            self.dice.pop()

    def has_dice(self):
        return len(self.dice) > 0

    def __str__(self):
        return f"{self.name} ({len(self.dice)} dice)"

    def display_dice(self):
        dice_str = ' '.join(str(die) for die in self.dice)
        print(f"{self.name}, your dice: {dice_str}")


class GameState:
    def __init__(self, players):
        self.players = players  # List of Player objects
        self.move_history = []  # List of all moves (for overall game history)
        self.current_round_bids = []  # List of bids in the current round
        self.current_bid = None  # Tuple of (quantity, face)
        self.current_player_index = 0

    def add_move(self, move):
        self.move_history.append(move)

    def add_round_bid(self, bid):
        self.current_round_bids.append(bid)

    def get_active_players(self):
        return [player for player in self.players if player.has_dice()]

    def next_player(self):
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)

    def reset_bid(self):
        self.current_bid = None
        self.current_round_bids = []  # Reset bids for the new round

    def is_valid_bid(self, bid):
        quantity, face = bid
        if not self.current_bid:
            return True  # Any bid is valid if there's no current bid
        current_quantity, current_face = self.current_bid
        if quantity > current_quantity:
            return True
        if quantity == current_quantity and face > current_face:
            return True
        return False

    def count_dice(self, face):
        total = 0
        ones_count = 0
        for player in self.players:
            total += player.dice.count(face)
            if face != 1:
                ones_count += player.dice.count(1)  # Ones are wild
        return total + ones_count

    def total_dice(self):
        return sum(len(player.dice) for player in self.players)

    def display_previous_bids(self):
        if not self.current_round_bids:
            print("No previous bids in this round.")
            return
        print("Previous Bids:")
        for bid in self.current_round_bids:
            player = bid['player']
            quantity, face = bid['bid']
            print(f" - {player} bid {quantity} x {face}'s")
        print()


def clear_screen():
    # Clear the terminal screen for Windows and Unix/Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize_players():
    print("Welcome to Liar's Dice!")
    while True:
        try:
            num_players = int(input("Enter number of players (2-6): "))
            if 2 <= num_players <= 6:
                break
            else:
                print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ").strip()
        if not name:
            name = f"Player {i+1}"
        is_ai_input = input(f"Is {name} an AI? (y/n): ").strip().lower()
        is_ai = is_ai_input == 'y'
        players.append(Player(name, is_ai))
    return players


def get_bid_input(player, game_state):
    if player.is_ai:
        # AI Player Turn
        messages = player.messages
        # Prepare game state summary
        game_state_summary = f"""It's your turn.

Current bid: {game_state.current_bid if game_state.current_bid else 'None'}.

Your dice: {player.dice}.

Previous bids in this round:
"""
        # Number of dice remaining for each player
        game_state_summary += "Dice remaining for each player:\n"
        for p in game_state.players:
            game_state_summary += f" - {p.name}: {len(p.dice)} dice\n"

        if game_state.current_round_bids:
            for bid in game_state.current_round_bids:
                bid_player = bid['player']
                quantity, face = bid['bid']
                game_state_summary += f" - {bid_player} bid {quantity} x {face}'s\n"
        else:
            game_state_summary += "No previous bids in this round.\n"

        if game_state.current_round_bids:
            total_dice = game_state.total_dice()
            current_bid = game_state.current_bid
            your_dice = player.dice

            current_bid_prob, expected_total, best_bid_prob, best_bid = calculate_liars_dice_probabilities(
                total_dice,
                current_bid,
                your_dice
            )
            # Output the results
            game_state_summary += f"Probability that the current bid is true: {current_bid_prob * 100:.2f}%\n"
            game_state_summary += f"Expected total number of {current_bid[1]}'s (including ones): {expected_total:.2f}\n"
            game_state_summary += f"Probability of your best possible valid bet being true: {best_bid_prob * 100:.2f}% Best bid: {best_bid}\n"

        # Add game state to AI messages
        messages = game_state_summary
        print(messages)

        wait = input("Press Enter to continue...")

        # Get AI's response
        response = get_liars_dice_completion(messages)
        if response is None:
            print(f"{player.name} did not provide a valid response.")
            return None, None

        # Update AI messages with the assistant's response
        messages = response

        if response.quantity != 0:
            bid = (response.quantity, response.face)
            if game_state.is_valid_bid(bid):
                return 'bid', bid
            else:
                print(f"{player.name} made an invalid bid.")
                return None, None
        elif response.quantity == 0:
            return 'call', None
        else:
            print(f"{player.name} provided an invalid action.")
            print(response)
            wait = input("Press Enter to continue...")
            return None, None
    else:
        # Human Player Turn
        while True:
            bid_input = input(
                f"{player.name}, enter your bid (e.g., '5 4' for five fours) or 'call': ").strip().lower()
            if bid_input == 'call':
                return 'call', None
            parts = bid_input.split()
            if len(parts) != 2:
                print(
                    "Invalid input format. Please enter in 'quantity face' format or 'call'.")
                continue
            try:
                quantity = int(parts[0])
                face = int(parts[1])
                if face < 1 or face > 6:
                    print("Face value must be between 1 and 6.")
                    continue
                if game_state.is_valid_bid((quantity, face)):
                    return 'bid', (quantity, face)
                else:
                    print(
                        "Invalid bid. You must increase the quantity, the face, or both.")
            except ValueError:
                print("Invalid numbers. Please enter integers for quantity and face.")


def reveal_dice(players):
    print("\nRevealing all dice:")
    for player in players:
        print(f"{player.name}: {player.dice}")
    print()


def display_players(game_state):
    print("\nCurrent Players:")
    for player in game_state.get_active_players():
        print(f" - {player}")
    print()


def main():
    players = initialize_players()
    game_state = GameState(players)

    # Initial roll
    for player in players:
        player.roll_dice()

    while len(game_state.get_active_players()) > 1:
        clear_screen()
        display_players(game_state)
        current_player = game_state.players[game_state.current_player_index]

        if not current_player.has_dice():
            game_state.next_player()
            continue

        # Display current bid
        print(
            f"Current bid: {game_state.current_bid if game_state.current_bid else 'None'}\n")

        # Display previous bids in this round
        game_state.display_previous_bids()

        # Display current player's dice
        if not current_player.is_ai:
            current_player.display_dice()
            # Pause for the player to see their dice

        # Get player's action
        action, data = get_bid_input(current_player, game_state)

        if action == 'bid':
            bid = data
            game_state.current_bid = bid
            game_state.add_move(
                {'player': current_player.name, 'action': 'bid', 'bid': bid})
            game_state.add_round_bid(
                {'player': current_player.name, 'bid': bid})
            print(f"{current_player.name} bids {bid[0]} x {bid[1]}'s")
            game_state.next_player()

        elif action == 'call':
            if not game_state.current_bid:
                print("No bids to call. You must bid first.")
                time.sleep(2)  # Pause to let the player read the message
                continue

            previous_player_index = (
                game_state.current_player_index - 1) % len(game_state.players)
            previous_player = game_state.players[previous_player_index]
            print(f"{current_player.name} calls 'liar' on {previous_player.name}!")
            reveal_dice(game_state.players)
            total = game_state.count_dice(game_state.current_bid[1])
            print(
                f"Total {game_state.current_bid[1]}'s (including ones): {total}")

            if total >= game_state.current_bid[0]:
                print(
                    f"{previous_player.name}'s bid was valid. {current_player.name} loses a die.")
                current_player.lose_die()
                next_starting_player = current_player
            else:
                print(
                    f"{previous_player.name}'s bid was invalid. {previous_player.name} loses a die.")
                previous_player.lose_die()
                next_starting_player = previous_player

            game_state.add_move({'player': current_player.name,
                                'action': 'call', 'against': previous_player.name})

            # Determine the next player index before removing any players
            next_player_index = game_state.players.index(next_starting_player)

            # Remove players with no dice
            game_state.players = [
                player for player in game_state.players if len(player.dice) > 0]

            # Adjust next_player_index if necessary
            if next_player_index >= len(game_state.players):
                next_player_index = 0

            # Reset for next round
            wait = input("Press Enter to continue...")
            game_state.reset_bid()

            # Re-roll dice for active players
            for player in game_state.get_active_players():
                player.roll_dice()

            # Set the next starting player
            game_state.current_player_index = next_player_index
            game_state.next_player()

            if not current_player.is_ai:
                input("Press Enter to continue...")
            else:
                time.sleep(1)  # Small delay for AI turns

    # Determine the winner
    winner = game_state.get_active_players()[0]
    print(
        f"\nGame Over! The winner is {winner.name} with {len(winner.dice)} dice remaining.")


if __name__ == "__main__":
    main()
