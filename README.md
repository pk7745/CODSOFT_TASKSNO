# CodSoft Python Programming Internship

Welcome to the **CodSoft Python Programming Internship** repository. This repository contains clean, robust, and well-tested solutions for the assigned Python programming tasks.

---

## 📁 Repository Structure

```text
CODSOFT_PYTHON/
│
├── Task4_RockPaperScissors/
│   ├── game.py          # Rock-Paper-Scissors Game CLI implementation
│   └── README.md        # Detailed Task 4 documentation
│
├── Task5_ContactBook/
│   ├── contact_book.py  # Contact Book CLI implementation
│   ├── contacts.example.json # Sample template data
│   └── README.md        # Detailed Task 5 documentation
│
├── test_game.py         # Automated test suite for Task 4 verification
├── test_contact_book.py # Automated test suite for Task 5 verification
└── README.md            # Root repository overview
```

---

## 📋 Completed Tasks

### Task 4 — Rock-Paper-Scissors Game
- **Status**: Completed
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

### Task 5 — Contact Book
- **Status**: Completed
- **Directory**: `Task5_ContactBook/`
- **Features**:
  - Contact storage with `Name`, `Phone`, `Email`, `Address`, and `Favorite` status
  - Add Contact with input validation & duplicate phone detection
  - View Contact List in clean ASCII tabular format with full details view
  - Search Contact by Name (case-insensitive, partial) and Phone Number (digit matching)
  - Update Contact with default prompt `[Current Value]` (Press Enter to keep existing)
  - Delete Contact with explicit `[Y/N]` confirmation
  - Monotonic & stable Contact IDs (`C001`, `C002`, ...)
  - Persistent JSON storage with non-destructive corrupted JSON safety (`contacts.json.corrupt-YYYYMMDD-HHMMSS` backup creation)
  - User-facing Favorites management and Contact Statistics summary
- **Execution**:
  ```bash
  python Task5_ContactBook/contact_book.py
  ```
- **Testing**:
  ```bash
  python test_contact_book.py
  ```

---

## ⚙️ Requirements

- **Python**: 3.6+
- **Dependencies**: None (Uses Python Standard Library only)

