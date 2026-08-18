#!/usr/bin/env python3
"""
CodSoft Python Programming Internship — Task 4: Rock-Paper-Scissors Game (V2 Upgrade)

Author: CodSoft Intern
Description: A clean, polished, modular CLI implementation of Rock-Paper-Scissors
             in standard Python with zero external dependencies. Features complete
             score tracking, robust input validation, and clear visual presentation.
"""

import random
from typing import Optional, Dict, Tuple

# Canonical game choices
CHOICES: Tuple[str, ...] = ("rock", "paper", "scissors")

# Mapping input aliases (numbers, shortcuts, full names) to canonical choice values
CHOICE_ALIASES: Dict[str, str] = {
    "1": "rock",
    "r": "rock",
    "rock": "rock",
    "2": "paper",
    "p": "paper",
    "paper": "paper",
    "3": "scissors",
    "s": "scissors",
    "scissors": "scissors",
    "4": "quit",
    "q": "quit",
    "quit": "quit",
    "exit": "quit"
}

# Backwards compatibility alias
CHOICE_MAP = CHOICE_ALIASES


def display_banner() -> None:
    """Display the opening welcome banner."""
    print("=" * 60)
    print("              ROCK | PAPER | SCISSORS")
    print("============================================================")
    print("                  CODSOFT TASK 4")
    print("=" * 60)


def display_rules() -> None:
    """Display the basic game rules."""
    print("\nGAME RULES")
    print("-" * 60)
    print("  ROCK       beats SCISSORS")
    print("  SCISSORS   beats PAPER")
    print("  PAPER      beats ROCK")
    print("-" * 60)


def normalize_choice(value: str) -> Optional[str]:
    """
    Normalize raw string input to canonical choice ('rock', 'paper', 'scissors', 'quit')
    or return None if input is invalid.
    """
    if not isinstance(value, str):
        return None
    cleaned = value.strip().lower()
    return CHOICE_ALIASES.get(cleaned, None)


def get_user_choice() -> str:
    """
    Prompt the user for their choice with robust input validation.
    Returns canonical choice string: 'rock', 'paper', 'scissors', or 'quit'.
    """
    while True:
        print("\n+----------------------------------------------------------+")
        print("|                      MAIN MENU                           |")
        print("+----------------------------------------------------------+")
        print("|  1. Rock                                                 |")
        print("|  2. Paper                                                |")
        print("|  3. Scissors                                             |")
        print("|  4. Quit                                                 |")
        print("+----------------------------------------------------------+")
        
        raw_input = input("Enter your choice: ")
        choice = normalize_choice(raw_input)
        
        if choice is not None:
            return choice
        
        print(f"\n[!] Invalid choice: '{raw_input}'.")
        print("\nPlease enter:")
        print("  1 - Rock")
        print("  2 - Paper")
        print("  3 - Scissors")
        print("  4 - Quit")


def get_computer_choice() -> str:
    """
    Generate the computer's choice randomly.
    Returns: 'rock', 'paper', or 'scissors'
    """
    return random.choice(CHOICES)


def determine_winner(user_choice: str, computer_choice: str) -> str:
    """
    Determine the winner of a single round.
    Args:
        user_choice: User choice ('rock', 'paper', or 'scissors')
        computer_choice: Computer choice ('rock', 'paper', or 'scissors')
    Returns: 'draw', 'user', or 'computer'
    """
    if user_choice == computer_choice:
        return "draw"

    winning_combos = {
        ("rock", "scissors"),
        ("scissors", "paper"),
        ("paper", "rock")
    }

    if (user_choice, computer_choice) in winning_combos:
        return "user"
    
    return "computer"


def get_result_explanation(user_choice: str, computer_choice: str, result: str) -> str:
    """
    Return a concise explanation of the round outcome.
    """
    if result == "draw":
        return f"Both players chose {user_choice.capitalize()}."
    
    winning_explanations = {
        ("rock", "scissors"): "Rock beats Scissors.",
        ("scissors", "paper"): "Scissors beats Paper.",
        ("paper", "rock"): "Paper beats Rock.",
    }
    
    if result == "user":
        return winning_explanations.get((user_choice, computer_choice), "")
    else:
        return winning_explanations.get((computer_choice, user_choice), "")


def display_round_result(user_choice: str, computer_choice: str, result: str, score: dict, round_num: int) -> None:
    """
    Display current round result, result explanation, and updated score table.
    """
    result_messages = {
        "user": "YOU WIN!",
        "computer": "COMPUTER WINS!",
        "draw": "IT'S A DRAW!"
    }
    
    explanation = get_result_explanation(user_choice, computer_choice, result)
    
    print("\n============================================================")
    print(f"                         ROUND {round_num:02d}")
    print("============================================================")
    print(f"\nYOU          : {user_choice.capitalize()}")
    print(f"COMPUTER     : {computer_choice.capitalize()}")
    print(f"\nRESULT       : {result_messages.get(result, result)}")
    print(f"EXPLANATION  : {explanation}")
    print("\n------------------------------------------------------------")
    print("CURRENT SCORE")
    print("------------------------------------------------------------")
    print(f"YOU          : {score['user']}")
    print(f"COMPUTER     : {score['computer']}")
    print(f"DRAWS        : {score['draws']}")
    print(f"TOTAL ROUNDS : {score['rounds']}")
    print("------------------------------------------------------------")


def ask_play_again() -> bool:
    """
    Prompt user whether to play another round. Handles case-insensitivity and whitespace.
    Returns: True if playing again, False otherwise.
    """
    valid_yes = {"y", "yes"}
    valid_no = {"n", "no"}
    
    while True:
        answer = input("\nPlay another round? [Y/N]: ").strip().lower()
        if answer in valid_yes:
            return True
        if answer in valid_no:
            return False
        print("[!] Please enter Y for yes or N for no.")


def display_final_summary(score: dict) -> None:
    """
    Display overall game session summary when exiting.
    """
    print("\n============================================================")
    print("                      FINAL SCORE")
    print("============================================================")
    print(f"YOU          : {score['user']}")
    print(f"COMPUTER     : {score['computer']}")
    print(f"DRAWS        : {score['draws']}")
    print(f"TOTAL ROUNDS : {score['rounds']}")
    print("------------------------------------------------------------\n")
    
    if score["rounds"] == 0:
        overall_result = "OVERALL RESULT: No rounds were played."
    elif score["user"] > score["computer"]:
        overall_result = "OVERALL RESULT\n>>> YOU ARE THE WINNER! <<<"
    elif score["computer"] > score["user"]:
        overall_result = "OVERALL RESULT\n>>> COMPUTER IS THE WINNER! <<<"
    else:
        overall_result = "OVERALL RESULT: DRAW!"
        
    print(f"{overall_result}")
    print("============================================================")
    print("          Thanks for playing Rock-Paper-Scissors!")
    print("============================================================\n")


def play_game() -> None:
    """Manage the game execution loop and score state persistence."""
    display_banner()
    display_rules()

    score = {
        "user": 0,
        "computer": 0,
        "draws": 0,
        "rounds": 0
    }

    while True:
        user_choice = get_user_choice()
        
        if user_choice == "quit":
            print("\nExiting game...")
            break

        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)

        score["rounds"] += 1
        if result == "user":
            score["user"] += 1
        elif result == "computer":
            score["computer"] += 1
        else:
            score["draws"] += 1

        display_round_result(user_choice, computer_choice, result, score, score["rounds"])

        if not ask_play_again():
            break

    display_final_summary(score)


def main() -> None:
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
