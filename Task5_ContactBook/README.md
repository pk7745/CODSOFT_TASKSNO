# Task 5 — Contact Book

A persistent, modular, terminal-based Contact Book CLI application built for **CodSoft Python Programming Internship — Task 5**.

---

## 📌 CodSoft Internship

- **Program**: Python Programming Internship
- **Task 5**: Contact Book
- **Status**: Completed & Verified

---

## 🎯 Mandatory Features

The application satisfies every official CodSoft requirement:

1. **Contact Information Storage**:
   - `Name`
   - `Phone Number`
   - `Email Address`
   - `Address`
2. **Add Contact**:
   - Prompts for Name, Phone, Email, Address.
   - Validates input formats (non-empty name/address, phone format, email regex).
3. **View Contact List**:
   - Tabular CLI display listing Contact ID, Name, Phone Number, and Favorite status.
   - Detailed single-contact inspection.
4. **Search Contact**:
   - Search by **Name** (case-insensitive, partial matching).
   - Search by **Phone Number** (partial digit sequence matching).
5. **Update Contact**:
   - Update any field with default prompt `[Current Value]` (Press Enter to keep existing values).
6. **Delete Contact**:
   - Interactive deletion requiring explicit `[Y/N]` confirmation step.
7. **User-Friendly Interface**:
   - Clean ASCII menu, error recovery, input validation, and clear feedback messages.

---

## 🚀 Enhancements & Advanced Features

In addition to core mandatory requirements, Task 5 includes user-facing V2 features:

- **Monotonic Contact ID System**:
  - Stable IDs (`C001`, `C002`, `C003`, ...) generated automatically.
  - IDs remain stable when contacts are deleted (deleting `C002` retains `C003`; next added contact is assigned `C004`).
- **Persistent JSON Storage**:
  - Automatically loads and saves data to `contacts.json`.
- **Corrupted JSON Non-Destructive Safety**:
  - If `contacts.json` contains invalid JSON, the corrupted file is **never** silently overwritten.
  - Automatically preserves the corrupted file as `contacts.json.corrupt-YYYYMMDD-HHMMSS`.
  - Warns the user and safely starts with an empty in-memory list without throwing a Python traceback.
- **Duplicate Phone Number Detection**:
  - Normalizes phone numbers (handling country codes like `+91`) and warns if a duplicate phone number exists.
  - Asks for explicit `[Y/N]` user confirmation before saving duplicates.
- **User-Facing Favorites Management**:
  - Mark/unmark contacts as Favorites.
  - Filter and view favorite contacts (Option 6 in Main Menu).
- **Contact Statistics**:
  - View summary counts for Total Contacts and Favorite Contacts (Option 7 in Main Menu).

---

## 🛠️ Technologies Used

- **Python 3**
- **JSON** (Data persistence)
- **Python Standard Library** (`json`, `os`, `re`, `shutil`, `datetime`)
- **unittest** & **unittest.mock** (Automated test suite)

---

## ⚙️ How to Run

Run the Contact Book CLI application from the repository root:

```bash
python Task5_ContactBook/contact_book.py
```

### CLI Main Menu Preview

```text
============================================================
                    CONTACT BOOK
============================================================
                 CODSOFT TASK 5
============================================================

+----------------------------------------------------------+
|                     MAIN MENU                            |
+----------------------------------------------------------+
|  1. Add Contact                                          |
|  2. View Contacts                                        |
|  3. Search Contact                                       |
|  4. Update Contact                                       |
|  5. Delete Contact                                       |
|  6. View Favorites                                       |
|  7. Contact Statistics                                   |
|  8. Exit                                                 |
+----------------------------------------------------------+

Enter your choice (1-8):
```

---

## 🧪 How to Test

Run the automated unit test suite from the repository root:

```bash
python test_contact_book.py
```

Or via `unittest`:

```bash
python -m unittest test_contact_book.py
```

---

## 💾 Data Storage Strategy

- Runtime data is saved to `Task5_ContactBook/contacts.json`.
- `contacts.json` and corrupted backup files (`contacts.json.corrupt-*`) are excluded from Git version control in `.gitignore` to prevent committing local data.
- Sample reference template data with fictional contacts is provided in `Task5_ContactBook/contacts.example.json`.

---

## 📁 File Structure

```text
CODSOFT_PYTHON/
│
├── Task5_ContactBook/
│   ├── contact_book.py          # Main CLI application & business logic
│   ├── contacts.example.json    # Sample template contacts file
│   └── README.md                # Task 5 documentation
│
├── test_contact_book.py         # Automated unit test suite for Task 5
```
