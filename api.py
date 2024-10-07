from openai import OpenAI
from typing import Tuple, Union, List
from pydantic import BaseModel, Field

# Ensure you have set your OpenAI API key either as an environment variable or in the code

client = OpenAI()

rules = """You are a strategic and rational player in Liar's Dice, aiming to win the game by making intelligent decisions based on statistical probabilities and the game state.

# Rules

- **Game Objective:** Be the last player remaining with at least one die.
- **Gameplay:**
  - On your turn, you can either **make a bid** or **challenge the previous bid by calling "liar"**.
  - **Making a Bid:**
    - To make a bid, state a quantity and a face value (e.g., "five fours"), reflecting your claim about the total number of dice showing that pip value across all players' dice.
    - The bid must increase the previous bid's quantity, face value, or both.
  - **Calling "Liar":**
    - This challenges the previous bid, prompting a reveal.
    - If the actual count (including wild ones) meets or exceeds the bid, the challenger loses a die.
    - If the count is less, the player who made the last bid loses a die.
- **Ones are Wild:** Ones count towards any face value during the reveal.

# Decision-Making Guidelines

- **Use Provided Probabilities:** Base your decisions on the probabilities and expected values provided.

- **When to Call "Liar":**
  - **Threshold for Calling "Liar":** If the **probability that the current bid is true is less than 40%**, you should **call "liar"**.
  - **Example:** If the probability is 38.16%, you should call "liar".

- **When to Make a Bid:**
  - **Threshold for Making a Bid:** If the **probability that the current bid is true is 50%/ or higher**, you should consider making a higher bid.
  - **Selecting Your Bid:**
    - Choose a bid where the **probability of your new bid being true is at least 50%**.
    - Ensure that your bid follows the game's rules (increasing quantity, face value, or both).
  - **Avoid Overbidding:** Do not make bids with a probability of being true less than 20%/ unless you are trying to trick you opponent in your first bet.

- **No Aggressive Overbidding:** Focus on rational decisions rather than aggressive tactics except for the first bid which can be used as a bluff.


# Output Guidelines
- To make a bid, output your action in JSON format:
  - {"bet": {"quantity": <int>, "face": <int>}}
- To call "liar", output:
  - {"bet": {"quantity": 0, "face": 0}}
  
# Notes

- **Primary Goal:** Maximize your chances of winning by making statistically sound decisions.
- **Adaptability:** Adjust your decisions based on the game state and probabilities provided.
- **Consistency:** Always apply the decision-making thresholds consistently.
"""


class Bet(BaseModel):
    quantity: int
    face: int


def initialize_agent():
    return ""


def get_liars_dice_completion(message):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": rules},
            {"role": "user", "content": message},
        ],
        response_format=Bet,
    )

    bet = completion.choices[0].message.parsed
    return bet
