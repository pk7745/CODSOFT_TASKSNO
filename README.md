# CodSoft Python Programming Internship

Welcome to the **CodSoft Python Programming Internship** repository. This repository contains clean, robust, and well-tested solutions for the assigned Python programming tasks.

---

## 📁 Repository Structure

```text
CODSOFT_PYTHON/
│
├── Task4_RockPaperScissors/
│   ├── game.py          # Rock-Paper-Scissors Game CLI implementation (V2)
│   └── README.md        # Detailed Task 4 documentation
│
├── test_game.py         # Automated test suite for Task 4 verification
└── README.md            # Root repository overview
```

---

## 📋 Completed Tasks

### Task 4 — Rock-Paper-Scissors Game
- **Directory**: `Task4_RockPaperScissors/`
- **Features**:
  - Interactive terminal CLI with Rock, Paper, Scissors choices
  - Input normalization supporting numbers (`1-4`), aliases (`r`, `p`, `s`, `q`), case-insensitivity, and whitespace handling
  - Randomized computer choice using `random` module
  - Complete 9-combination winner engine with outcome explanations
  - Running score counter (User, Computer, Draws, Total Rounds) across multiple replay rounds
  - Robust input validation preventing crashes on invalid input
  - Final game summary with overall session outcome
- **Execution**:
  ```bash
  python Task4_RockPaperScissors/game.py
  ```
- **Testing**:
  ```bash
  python test_game.py
  ```

---

## ⚙️ Requirements

- **Python**: 3.6+
- **Dependencies**: None (Uses Python Standard Library only)
