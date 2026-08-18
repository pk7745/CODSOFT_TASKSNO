#!/usr/bin/env python3
"""
Unit test suite for CodSoft Task 4 - Rock-Paper-Scissors Game (V2 Upgrade).
Located at repository root for verification.
"""

import sys
import os
import unittest
from unittest.mock import patch
import io

# Add Task4_RockPaperScissors to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Task4_RockPaperScissors')))

import game


class TestRockPaperScissors(unittest.TestCase):

    def test_determine_winner_all_nine_combinations(self):
        """Verify all 9 combinations of Rock, Paper, Scissors."""
        # Rock combinations
        self.assertEqual(game.determine_winner("rock", "rock"), "draw")
        self.assertEqual(game.determine_winner("rock", "paper"), "computer")
        self.assertEqual(game.determine_winner("rock", "scissors"), "user")

        # Paper combinations
        self.assertEqual(game.determine_winner("paper", "rock"), "user")
        self.assertEqual(game.determine_winner("paper", "paper"), "draw")
        self.assertEqual(game.determine_winner("paper", "scissors"), "computer")

        # Scissors combinations
        self.assertEqual(game.determine_winner("scissors", "rock"), "computer")
        self.assertEqual(game.determine_winner("scissors", "paper"), "user")
        self.assertEqual(game.determine_winner("scissors", "scissors"), "draw")

    def test_normalize_choice_valid(self):
        """Test normalization of valid user inputs, aliases, uppercase, and padded whitespace."""
        self.assertEqual(game.normalize_choice("1"), "rock")
        self.assertEqual(game.normalize_choice("r"), "rock")
        self.assertEqual(game.normalize_choice("ROCK"), "rock")
        self.assertEqual(game.normalize_choice("  rock  "), "rock")

        self.assertEqual(game.normalize_choice("2"), "paper")
        self.assertEqual(game.normalize_choice("p"), "paper")
        self.assertEqual(game.normalize_choice("PAPER"), "paper")

        self.assertEqual(game.normalize_choice("3"), "scissors")
        self.assertEqual(game.normalize_choice("s"), "scissors")
        self.assertEqual(game.normalize_choice("SCISSORS"), "scissors")

        self.assertEqual(game.normalize_choice("4"), "quit")
        self.assertEqual(game.normalize_choice("q"), "quit")
        self.assertEqual(game.normalize_choice("QUIT"), "quit")

    def test_normalize_choice_invalid(self):
        """Test normalization of invalid values returns None."""
        self.assertIsNone(game.normalize_choice("abc"))
        self.assertIsNone(game.normalize_choice("99"))
        self.assertIsNone(game.normalize_choice(""))
        self.assertIsNone(game.normalize_choice("   "))
        self.assertIsNone(game.normalize_choice(1.5))
        self.assertIsNone(game.normalize_choice(None))

    def test_result_explanations(self):
        """Test concise winner/draw explanation strings."""
        self.assertEqual(game.get_result_explanation("rock", "scissors", "user"), "Rock beats Scissors.")
        self.assertEqual(game.get_result_explanation("scissors", "paper", "user"), "Scissors beats Paper.")
        self.assertEqual(game.get_result_explanation("paper", "rock", "user"), "Paper beats Rock.")
        self.assertEqual(game.get_result_explanation("rock", "paper", "computer"), "Paper beats Rock.")
        self.assertEqual(game.get_result_explanation("rock", "rock", "draw"), "Both players chose Rock.")

    @patch("random.choice")
    def test_get_computer_choice_deterministic(self, mock_random_choice):
        """Deterministic test for get_computer_choice() using unittest.mock."""
        mock_random_choice.side_effect = ["rock", "paper", "scissors"]
        
        self.assertEqual(game.get_computer_choice(), "rock")
        self.assertEqual(game.get_computer_choice(), "paper")
        self.assertEqual(game.get_computer_choice(), "scissors")
        self.assertEqual(mock_random_choice.call_count, 3)

    def test_choice_mapping_alias(self):
        """Test backwards compatibility of CHOICE_MAP alias."""
        self.assertEqual(game.CHOICE_MAP["1"], "rock")
        self.assertEqual(game.CHOICE_MAP["r"], "rock")
        self.assertEqual(game.CHOICE_MAP["rock"], "rock")
        self.assertEqual(game.CHOICE_MAP["4"], "quit")

    @patch("builtins.input", side_effect=["abc", "99", "-1", "", "1"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_get_user_choice_validation(self, mock_stdout, mock_input):
        """Test get_user_choice recovers gracefully from invalid inputs."""
        choice = game.get_user_choice()
        self.assertEqual(choice, "rock")
        self.assertEqual(mock_input.call_count, 5)
        self.assertIn("Invalid choice", mock_stdout.getvalue())

    @patch("builtins.input", side_effect=["invalid", "123", "Y"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_ask_play_again_yes(self, mock_stdout, mock_input):
        """Test ask_play_again recovers from invalid inputs and accepts 'Y'."""
        res = game.ask_play_again()
        self.assertTrue(res)
        self.assertEqual(mock_input.call_count, 3)

    @patch("builtins.input", side_effect=["NO"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_ask_play_again_no(self, mock_stdout, mock_input):
        """Test ask_play_again returns False for 'NO'."""
        res = game.ask_play_again()
        self.assertFalse(res)
        self.assertEqual(mock_input.call_count, 1)

    @patch("builtins.input", side_effect=["4"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_immediate_quit_zero_rounds(self, mock_stdout, mock_input):
        """Test selecting Quit immediately displays zero-round final summary."""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("No rounds were played.", output)
        self.assertIn("Exiting game...", output)

    @patch("random.choice", side_effect=["scissors", "rock", "paper", "scissors", "rock"])
    @patch("builtins.input", side_effect=["1", "y", "1", "y", "1", "y", "2", "y", "3", "n"])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_full_game_flow_multiple_rounds(self, mock_stdout, mock_input, mock_choice):
        """Test running a full game session with 5 rounds and verifying score tracking."""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertEqual(mock_choice.call_count, 5)
        self.assertIn("TOTAL ROUNDS : 5", output)
        self.assertIn("FINAL SCORE", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_final_summary_outcomes(self, mock_stdout):
        """Test final summary text output for user win, computer win, draw, zero rounds."""
        # Case 1: User win
        score_user_win = {"user": 3, "computer": 1, "draws": 1, "rounds": 5}
        game.display_final_summary(score_user_win)
        self.assertIn("YOU ARE THE WINNER!", mock_stdout.getvalue())

        # Case 2: Computer win
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        score_comp_win = {"user": 1, "computer": 3, "draws": 1, "rounds": 5}
        game.display_final_summary(score_comp_win)
        self.assertIn("COMPUTER IS THE WINNER!", mock_stdout.getvalue())

        # Case 3: Overall Draw
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        score_draw = {"user": 2, "computer": 2, "draws": 1, "rounds": 5}
        game.display_final_summary(score_draw)
        self.assertIn("OVERALL RESULT: DRAW!", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
