# Liar's Dice Game

A command-line implementation of **Liar's Dice**, a classic bluffing and bidding game, featuring both human and AI players powered by OpenAI's language models.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [AI Strategy](#ai-strategy)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is a Python-based implementation of Liar's Dice, allowing you to play against other human players or AI opponents. The AI players use OpenAI's language models to make decisions based on the game state, probabilities, and strategic guidelines.

## Features

- **Human and AI Players**: Play against friends or intelligent AI opponents.
- **Probability Calculations**: Provides statistical insights to help make informed decisions.
- **Customizable AI Strategy**: AI behavior can be adjusted via prompts for different play styles.
- **Command-Line Interface**: Simple and interactive text-based interface.
- **Extensible Codebase**: Modular design allows for easy additions and modifications.

## Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI Python library
- An OpenAI API key

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/liars-dice.git
   cd liars-dice
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**

   - Sign up for an OpenAI account if you don't have one.
   - Obtain your API key from the OpenAI dashboard.
   - Set the API key as an environment variable:

     ```bash
     export OPENAI_API_KEY='your-api-key-here'
     ```

     Alternatively, configure the API key in your code (not recommended for security reasons):

     ```python
     import os
     import openai

     openai.api_key = os.getenv('OPENAI_API_KEY')
     ```

## Usage

Run the game using:

```bash
python main.py
```

### Gameplay Instructions

- **Starting the Game**: Enter the number of players (2-6). For each player, provide a name and indicate if they are an AI.
- **During the Game**:
  - **Human Players**: When it's your turn, your dice will be displayed privately. You can make a bid or call "liar" on the previous bid.
  - **AI Players**: The AI will make decisions based on the game state and probabilities.
- **Bidding**: Enter your bid in the format `quantity face` (e.g., `5 4` for "five fours").
- **Calling "Liar"**: Type `call` to challenge the previous bid.

## Game Rules

- Players start with five six-sided dice.
- On your turn, you may either make a higher bid or call "liar" on the previous bid.
- **Bids**: Claim a quantity of dice showing a specific face value among all players (e.g., "five fours").
- **Ones are Wild**: Ones count as any face value during the reveal.
- **Challenging a Bid**:
  - If the actual count meets or exceeds the bid, the challenger loses a die.
  - If the actual count is less, the bidder loses a die.
- Players with no dice are eliminated.
- The last remaining player wins the game.

## AI Strategy

The AI players use OpenAI's language models to make decisions. Their strategy is guided by prompts that consider:

- Statistical probabilities of bids being true.
- Expected values based on the number of unknown dice.
- Rational decision-making thresholds

### Customizing AI Behavior

You can adjust the AI's strategy by modifying the system prompt in `api.py`. This allows you to experiment with different play styles and behaviors.

## Project Structure

- `main.py`: The main game logic and interface.
- `api.py`: Contains functions to interact with the OpenAI API and AI player logic.
- `requirements.txt`: Python dependencies.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for enhancements, bug fixes, or other improvements.

## License

This project is licensed under the [MIT License](LICENSE).