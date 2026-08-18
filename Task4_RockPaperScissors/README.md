# Rock-Paper-Scissors Game (V2 Upgrade)

A clean, interactive, professional CLI implementation of the classic **Rock-Paper-Scissors** game in Python. Built as part of the **CodSoft Python Programming Internship — Task 4**.

---

## 📌 Project Overview

This project is a beginner-friendly yet robust Python command-line application that allows users to play Rock-Paper-Scissors against an automated computer opponent. It tracks scores across multiple rounds, explains why the winner won each round, handles invalid inputs gracefully, and displays detailed statistics summaries.

---

## ✨ Features

- **User Choice Selection**: Select choices via numerical options (`1`, `2`, `3`, `4`) or text equivalents (`rock`, `paper`, `scissors`, `quit`, `r`, `p`, `s`, `q`).
- **Input Normalization & Validation**: Case-insensitive matching (`ROCK`, `Paper`, `SCISSORS`, `Y`, `N`) and leading/trailing whitespace stripping (`   rock  `).
- **Random Computer Opponent**: Computer choice is randomly generated using Python's standard `random` module.
- **Fair Game Logic & Explanations**: Complete 9-combination winner determination engine that explains why a round was won (e.g. *"Rock beats Scissors."*).
- **Score Tracking**: Tracks User Wins, Computer Wins, Draws, and Total Rounds across a session without resetting score between rounds.
- **Robust Error Handling**: Prevents crashes on invalid or empty inputs by giving clear error guidance and re-prompting.
- **Replay Option**: Option to immediately start another round (`[Y/N]`) while maintaining score state.
- **Final Session Summary**: Displays overall session statistics and announces the overall winner upon quitting.
- **Zero External Dependencies**: Standard Python 3 library only.

---

## 🎮 Game Rules & Supported Inputs

### Rules
```text
  ROCK       beats SCISSORS
  SCISSORS   beats PAPER
  PAPER      beats ROCK
```

### Supported Input Aliases
| Option | Canonical Choice | Accepted Input Aliases |
| :---: | :---: | :--- |
| **1** | `rock` | `1`, `r`, `rock`, `ROCK` |
| **2** | `paper` | `2`, `p`, `paper`, `PAPER` |
| **3** | `scissors` | `3`, `s`, `scissors`, `SCISSORS` |
| **4** | `quit` | `4`, `q`, `quit`, `QUIT`, `exit` |

---

## 🛠️ Technologies & Requirements

- **Python 3.6+**
- **Python Standard Library**
  - `random`: For computer choice selection
  - `typing`: Type annotations (`str`, `Optional`, `Dict`, `Tuple`)
  - `unittest`: For verification and unit test suite
- **External Dependencies**: None

---

## 🚀 How to Run & Test

### Run Application
1. Open your terminal or command prompt.
2. Navigate to the project directory:

   ```bash
   cd Task4_RockPaperScissors
   ```

3. Run the application:

   ```bash
   python game.py
   ```

### Run Test Suite
To execute the automated unit test suite from the repository root:

```bash
python test_game.py
```

Or using Python's test runner module:

```bash
python -m unittest test_game.py
```

*Status*: **12 automated tests passed cleanly.**

---

## 📂 Project Structure

```text
CODSOFT_PYTHON/
│
├── Task4_RockPaperScissors/
│   ├── game.py          # Main V2 application code
│   └── README.md        # Task-specific documentation
│
├── test_game.py         # Automated test suite (at repository root)
└── README.md            # Root repository overview
```

---

## 🏆 Internship Information

- **Organization**: CodSoft
- **Track**: Python Programming Internship
- **Task Number**: 4
- **Task Title**: Rock-Paper-Scissors Game
