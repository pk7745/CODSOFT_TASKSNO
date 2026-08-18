#!/usr/bin/env python3
"""
CodSoft Python Programming Internship - Task 5: Contact Book
============================================================
A persistent, modular, terminal-based CLI Contact Book application.

Features:
- Contact information: Name, Phone, Email, Address, Favorite status.
- Mandatory operations: Add, View List, Search (Name/Phone), Update, Delete.
- Monotonic unique Contact IDs (C001, C002, ...).
- Robust JSON persistence with non-destructive corrupted file recovery.
- Duplicate phone number detection with user confirmation.
- User-facing Favorites management and Contact Statistics.
"""

import json
import os
import re
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Default path for JSON persistence
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")


def validate_name(name: str) -> Tuple[bool, str]:
    """Validate contact name."""
    cleaned = name.strip()
    if not cleaned:
        return False, "Name cannot be empty."
    if len(cleaned) > 100:
        return False, "Name must be 100 characters or fewer."
    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate contact phone number."""
    cleaned = phone.strip()
    if not cleaned:
        return False, "Phone number cannot be empty."
    # Allow numbers starting optional +, digits, spaces, hyphens, parentheses (7 to 20 chars)
    pattern = r"^\+?[\d\s\-()]{7,20}$"
    digits_only = re.sub(r"[^\d]", "", cleaned)
    if not re.match(pattern, cleaned) or len(digits_only) < 7:
        return False, "Invalid phone number format. Please enter a valid phone number (e.g., 9876543210, +91 9876543210)."
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate contact email address."""
    cleaned = email.strip()
    if not cleaned:
        return False, "Email address cannot be empty."
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, cleaned):
        return False, "Invalid email address format (e.g., user@example.com)."
    return True, ""


def validate_address(address: str) -> Tuple[bool, str]:
    """Validate contact address."""
    cleaned = address.strip()
    if not cleaned:
        return False, "Address cannot be empty."
    return True, ""


def normalize_phone(phone_str: str) -> str:
    """Normalize phone number to digits only for accurate duplicate comparison."""
    return re.sub(r"[^\d]", "", phone_str)


def phones_match(phone1: str, phone2: str) -> bool:
    """
    Check if two phone numbers match, handling optional country codes (+91)
    and formatting differences.
    """
    norm1 = normalize_phone(phone1)
    norm2 = normalize_phone(phone2)
    if not norm1 or not norm2:
        return False
    if norm1 == norm2:
        return True
    if len(norm1) >= 7 and len(norm2) >= 7:
        if norm1.endswith(norm2) or norm2.endswith(norm1):
            return True
    return False


class ContactBook:
    """Business logic and data storage manager for Contact Book."""


    def __init__(self, data_file: Optional[str] = None) -> None:
        self.data_file: str = data_file or DEFAULT_DATA_FILE
        self.contacts: List[Dict[str, Any]] = []
        self._next_id_num: int = 1
        self.load_contacts()

    def _extract_id_number(self, id_str: str) -> int:
        """Extract numeric portion from Contact ID string like 'C005' -> 5."""
        match = re.search(r"\d+", id_str)
        return int(match.group()) if match else 0

    def generate_contact_id(self) -> str:
        """Generate a stable, monotonic unique Contact ID."""
        new_id = f"C{self._next_id_num:03d}"
        self._next_id_num += 1
        return new_id

    def load_contacts(self) -> Tuple[bool, str]:
        """
        Load contacts from JSON persistence file.
        Non-destructively handles corrupted JSON by backing up original file.
        """
        self.contacts = []
        self._next_id_num = 1

        if not os.path.exists(self.data_file):
            return True, "No existing data file found. Started with empty contact list."

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return True, "Data file is empty. Started with empty contact list."
                data = json.loads(content)

            if isinstance(data, dict) and "contacts" in data:
                raw_contacts = data.get("contacts", [])
                max_id = data.get("max_id_num", 0)
            elif isinstance(data, list):
                raw_contacts = data
                max_id = 0
            else:
                raw_contacts = []
                max_id = 0

            self.contacts = []
            for item in raw_contacts:
                if isinstance(item, dict) and "id" in item and "name" in item and "phone" in item:
                    contact_entry = {
                        "id": str(item["id"]),
                        "name": str(item["name"]),
                        "phone": str(item["phone"]),
                        "email": str(item.get("email", "")),
                        "address": str(item.get("address", "")),
                        "favorite": bool(item.get("favorite", False)),
                    }
                    self.contacts.append(contact_entry)
                    item_id_num = self._extract_id_number(contact_entry["id"])
                    if item_id_num > max_id:
                        max_id = item_id_num

            self._next_id_num = max(1, max_id + 1)
            return True, f"Loaded {len(self.contacts)} contact(s) successfully."

        except (json.JSONDecodeError, ValueError) as e:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_filename = f"{self.data_file}.corrupt-{timestamp}"
            try:
                shutil.copy2(self.data_file, backup_filename)
                warning_msg = (
                    f"[!] WARNING: '{os.path.basename(self.data_file)}' contains invalid JSON.\n"
                    f"    A backup of the corrupted file was created at:\n"
                    f"    '{os.path.basename(backup_filename)}'\n"
                    f"    Starting with an empty in-memory contact list."
                )
            except Exception as copy_err:
                warning_msg = (
                    f"[!] WARNING: '{os.path.basename(self.data_file)}' contains invalid JSON.\n"
                    f"    (Could not create backup file: {copy_err})\n"
                    f"    Starting with an empty in-memory contact list."
                )

            self.contacts = []
            self._next_id_num = 1
            print(warning_msg)
            return False, warning_msg

    def save_contacts(self) -> Tuple[bool, str]:
        """Save contacts to JSON file."""
        data = {
            "max_id_num": self._next_id_num - 1,
            "contacts": self.contacts,
        }
        try:
            dir_name = os.path.dirname(self.data_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True, "Contacts saved successfully."
        except Exception as e:
            return False, f"Failed to save contacts: {e}"

    def check_duplicate_phone(self, phone: str, exclude_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Check if a contact with matching normalized phone number already exists.
        Optionally exclude a specific contact ID (for updates).
        """
        if not phone.strip():
            return None

        for contact in self.contacts:
            if exclude_id and contact["id"].upper() == exclude_id.upper():
                continue
            if phones_match(contact["phone"], phone):
                return contact
        return None

    def add_contact(
        self,
        name: str,
        phone: str,
        email: str,
        address: str,
        favorite: bool = False,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Add a new contact after validating fields."""
        is_valid, msg = validate_name(name)
        if not is_valid:
            return False, msg, None

        is_valid, msg = validate_phone(phone)
        if not is_valid:
            return False, msg, None

        is_valid, msg = validate_email(email)
        if not is_valid:
            return False, msg, None

        is_valid, msg = validate_address(address)
        if not is_valid:
            return False, msg, None

        contact_id = self.generate_contact_id()
        new_contact = {
            "id": contact_id,
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
            "address": address.strip(),
            "favorite": favorite,
        }

        self.contacts.append(new_contact)
        self.save_contacts()
        return True, f"Contact added successfully. Assigned ID: {contact_id}", new_contact

    def get_all_contacts(self) -> List[Dict[str, Any]]:
        """Return list of all stored contacts."""
        return self.contacts

    def search_contacts(self, query: str, search_type: str = "all") -> List[Dict[str, Any]]:
        """
        Search contacts by name, phone, or both (case-insensitive & partial match).
        search_type options: 'name', 'phone', 'all'
        """
        query_clean = query.strip().lower()
        if not query_clean:
            return []

        query_digits = normalize_phone(query)
        results = []

        for contact in self.contacts:
            name_match = query_clean in contact["name"].lower()
            phone_raw_match = query_clean in contact["phone"].lower()
            phone_digit_match = bool(query_digits and query_digits in normalize_phone(contact["phone"]))

            if search_type == "name" and name_match:
                results.append(contact)
            elif search_type == "phone" and (phone_raw_match or phone_digit_match):
                results.append(contact)
            elif search_type == "all" and (name_match or phone_raw_match or phone_digit_match):
                results.append(contact)

        return results

    def get_contact_by_id(self, contact_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve contact by ID (case-insensitive)."""
        clean_id = contact_id.strip().upper()
        for contact in self.contacts:
            if contact["id"].upper() == clean_id:
                return contact
        return None

    def update_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        favorite: Optional[bool] = None,
    ) -> Tuple[bool, str]:
        """Update existing contact fields."""
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return False, f"Contact with ID '{contact_id}' not found."

        if name is not None and name.strip():
            is_valid, msg = validate_name(name)
            if not is_valid:
                return False, msg
            contact["name"] = name.strip()

        if phone is not None and phone.strip():
            is_valid, msg = validate_phone(phone)
            if not is_valid:
                return False, msg
            contact["phone"] = phone.strip()

        if email is not None and email.strip():
            is_valid, msg = validate_email(email)
            if not is_valid:
                return False, msg
            contact["email"] = email.strip()

        if address is not None and address.strip():
            is_valid, msg = validate_address(address)
            if not is_valid:
                return False, msg
            contact["address"] = address.strip()

        if favorite is not None:
            contact["favorite"] = favorite

        self.save_contacts()
        return True, "Contact updated successfully."

    def delete_contact(self, contact_id: str) -> Tuple[bool, str]:
        """Delete contact by ID."""
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return False, f"Contact with ID '{contact_id}' not found."

        self.contacts = [c for c in self.contacts if c["id"].upper() != contact_id.strip().upper()]
        self.save_contacts()
        return True, f"Contact '{contact['name']}' ({contact['id']}) deleted successfully."

    def toggle_favorite(self, contact_id: str) -> Tuple[bool, str]:
        """Toggle favorite status of a contact."""
        contact = self.get_contact_by_id(contact_id)
        if not contact:
            return False, f"Contact with ID '{contact_id}' not found."

        contact["favorite"] = not contact.get("favorite", False)
        status_str = "marked as Favorite" if contact["favorite"] else "removed from Favorites"
        self.save_contacts()
        return True, f"Contact '{contact['name']}' ({contact['id']}) {status_str}."

    def get_favorites(self) -> List[Dict[str, Any]]:
        """Return list of contacts marked as favorite."""
        return [c for c in self.contacts if c.get("favorite", False)]

    def get_stats(self) -> Dict[str, int]:
        """Return general statistics of contacts."""
        total = len(self.contacts)
        favorites = len(self.get_favorites())
        return {
            "total": total,
            "favorites": favorites,
        }


# ==============================================================================
# CLI USER INTERFACE FUNCTIONS
# ==============================================================================

def display_banner() -> None:
    """Print top banner."""
    print("=" * 60)
    print("                    CONTACT BOOK")
    print("=" * 60)
    print("                 CODSOFT TASK 5")
    print("=" * 60)


def display_menu() -> None:
    """Print main menu options."""
    print("\n+----------------------------------------------------------+")
    print("|                     MAIN MENU                            |")
    print("+----------------------------------------------------------+")
    print("|  1. Add Contact                                          |")
    print("|  2. View Contacts                                        |")
    print("|  3. Search Contact                                       |")
    print("|  4. Update Contact                                       |")
    print("|  5. Delete Contact                                       |")
    print("|  6. View Favorites                                       |")
    print("|  7. Contact Statistics                                   |")
    print("|  8. Exit                                                 |")
    print("+----------------------------------------------------------+")


def display_contacts_table(contacts: List[Dict[str, Any]], title: str = "CONTACT LIST") -> None:
    """Display contacts formatted as a readable CLI table."""
    print(f"\n============================================================")
    print(f"                    {title}")
    print(f"============================================================")

    if not contacts:
        print("\n[!] No contacts found.")
        print("=" * 60)
        return

    print(f"{'ID':<7} {'NAME':<20} {'PHONE':<16} {'FAV':<5}")
    print("-" * 60)
    for c in contacts:
        fav_mark = "Yes" if c.get("favorite", False) else "No"
        disp_name = c['name'] if len(c['name']) <= 18 else c['name'][:15] + "..."
        print(f"{c['id']:<7} {disp_name:<20} {c['phone']:<16} {fav_mark:<5}")
    print("-" * 60)
    print(f"Total Count: {len(contacts)}")
    print("=" * 60)


def display_contact_details(contact: Dict[str, Any]) -> None:
    """Display full details of a single contact."""
    fav_str = "Yes (Favorite)" if contact.get("favorite", False) else "No"
    print("\n------------------------------------------------------------")
    print(f"Contact Details ({contact['id']})")
    print("------------------------------------------------------------")
    print(f"  ID       : {contact['id']}")
    print(f"  Name     : {contact['name']}")
    print(f"  Phone    : {contact['phone']}")
    print(f"  Email    : {contact['email']}")
    print(f"  Address  : {contact['address']}")
    print(f"  Favorite : {fav_str}")
    print("------------------------------------------------------------")


def cli_add_contact(book: ContactBook) -> None:
    """CLI flow for adding a new contact."""
    print("\n---------------- ADD CONTACT ----------------")

    # Name input loop
    while True:
        name = input("Name       : ").strip()
        is_valid, msg = validate_name(name)
        if is_valid:
            break
        print(f"[!] {msg} Please try again.")

    # Phone input loop with duplicate check
    while True:
        phone = input("Phone      : ").strip()
        is_valid, msg = validate_phone(phone)
        if not is_valid:
            print(f"[!] {msg} Please try again.")
            continue

        duplicate = book.check_duplicate_phone(phone)
        if duplicate:
            print("\n[!] A contact with this phone number already exists:")
            print(f"    {duplicate['id']} - {duplicate['name']} ({duplicate['phone']})")
            confirm = input("Do you still want to add this contact? [Y/N]: ").strip().lower()
            if confirm not in ("y", "yes"):
                print("[!] Contact creation cancelled due to duplicate phone.")
                return

        break

    # Email input loop
    while True:
        email = input("Email      : ").strip()
        is_valid, msg = validate_email(email)
        if is_valid:
            break
        print(f"[!] {msg} Please try again.")

    # Address input loop
    while True:
        address = input("Address    : ").strip()
        is_valid, msg = validate_address(address)
        if is_valid:
            break
        print(f"[!] {msg} Please try again.")

    # Favorite status
    fav_input = input("Mark as Favorite? [Y/N] (Default: N): ").strip().lower()
    is_favorite = fav_input in ("y", "yes")

    success, msg, contact = book.add_contact(name, phone, email, address, favorite=is_favorite)
    if success and contact:
        print(f"\n[OK] {msg}")
    else:
        print(f"\n[!] Failed to add contact: {msg}")


def cli_view_contacts(book: ContactBook) -> None:
    """CLI flow to view contact list."""
    contacts = book.get_all_contacts()
    display_contacts_table(contacts, "CONTACT LIST")
    if contacts:
        sub_choice = input("\nEnter Contact ID to view full details (or press Enter to return): ").strip()
        if sub_choice:
            contact = book.get_contact_by_id(sub_choice)
            if contact:
                display_contact_details(contact)
            else:
                print(f"[!] Contact with ID '{sub_choice}' not found.")


def cli_search_contact(book: ContactBook) -> None:
    """CLI flow for searching contacts."""
    while True:
        print("\n---------------- SEARCH CONTACT ----------------")
        print("Search by:")
        print("  1. Name")
        print("  2. Phone Number")
        print("  3. Back")
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            query = input("Enter Name to search: ").strip()
            results = book.search_contacts(query, search_type="name")
            display_contacts_table(results, f"SEARCH RESULTS FOR NAME '{query}'")
            break
        elif choice == "2":
            query = input("Enter Phone Number to search: ").strip()
            results = book.search_contacts(query, search_type="phone")
            display_contacts_table(results, f"SEARCH RESULTS FOR PHONE '{query}'")
            break
        elif choice == "3":
            break
        else:
            print("[!] Invalid option. Please enter 1, 2, or 3.")


def cli_update_contact(book: ContactBook) -> None:
    """CLI flow to update a contact."""
    print("\n---------------- UPDATE CONTACT ----------------")
    contact_id = input("Enter Contact ID to update: ").strip()
    contact = book.get_contact_by_id(contact_id)

    if not contact:
        print(f"[!] Contact with ID '{contact_id}' not found.")
        return

    display_contact_details(contact)
    print("\nPress Enter to keep the existing value.\n")

    # Name
    while True:
        name_in = input(f"Name [{contact['name']}]: ").strip()
        if not name_in:
            new_name = contact['name']
            break
        is_valid, msg = validate_name(name_in)
        if is_valid:
            new_name = name_in
            break
        print(f"[!] {msg}")

    # Phone
    while True:
        phone_in = input(f"Phone [{contact['phone']}]: ").strip()
        if not phone_in:
            new_phone = contact['phone']
            break
        is_valid, msg = validate_phone(phone_in)
        if not is_valid:
            print(f"[!] {msg}")
            continue

        if normalize_phone(phone_in) != normalize_phone(contact['phone']):
            duplicate = book.check_duplicate_phone(phone_in, exclude_id=contact['id'])
            if duplicate:
                print("\n[!] A contact with this updated phone number already exists:")
                print(f"    {duplicate['id']} - {duplicate['name']} ({duplicate['phone']})")
                confirm = input("Do you still want to update to this phone number? [Y/N]: ").strip().lower()
                if confirm not in ("y", "yes"):
                    print("[!] Phone number update skipped (retaining existing phone).")
                    new_phone = contact['phone']
                    break
        new_phone = phone_in
        break

    # Email
    while True:
        email_in = input(f"Email [{contact['email']}]: ").strip()
        if not email_in:
            new_email = contact['email']
            break
        is_valid, msg = validate_email(email_in)
        if is_valid:
            new_email = email_in
            break
        print(f"[!] {msg}")

    # Address
    while True:
        address_in = input(f"Address [{contact['address']}]: ").strip()
        if not address_in:
            new_address = contact['address']
            break
        is_valid, msg = validate_address(address_in)
        if is_valid:
            new_address = address_in
            break
        print(f"[!] {msg}")

    # Favorite
    curr_fav_str = "Y" if contact.get("favorite", False) else "N"
    fav_in = input(f"Favorite [Y/N] (Current: {curr_fav_str}): ").strip().lower()
    if not fav_in:
        new_fav = contact.get("favorite", False)
    else:
        new_fav = fav_in in ("y", "yes")

    success, msg = book.update_contact(
        contact_id=contact['id'],
        name=new_name,
        phone=new_phone,
        email=new_email,
        address=new_address,
        favorite=new_fav,
    )
    if success:
        print(f"\n[OK] {msg}")
    else:
        print(f"\n[!] Update failed: {msg}")


def cli_delete_contact(book: ContactBook) -> None:
    """CLI flow to delete a contact."""
    print("\n---------------- DELETE CONTACT ----------------")
    contact_id = input("Enter Contact ID to delete: ").strip()
    contact = book.get_contact_by_id(contact_id)

    if not contact:
        print(f"[!] Contact with ID '{contact_id}' not found.")
        return

    display_contact_details(contact)
    confirm = input("\nAre you sure you want to delete this contact? [Y/N]: ").strip().lower()

    if confirm in ("y", "yes"):
        success, msg = book.delete_contact(contact_id)
        if success:
            print(f"\n[OK] {msg}")
        else:
            print(f"\n[!] Deletion failed: {msg}")
    else:
        print("\n[!] Deletion cancelled.")


def cli_view_favorites(book: ContactBook) -> None:
    """CLI flow to view favorite contacts."""
    favs = book.get_favorites()
    display_contacts_table(favs, "FAVORITE CONTACTS")
    if favs:
        sub = input("\nEnter Contact ID to toggle favorite status (or press Enter to return): ").strip()
        if sub:
            success, msg = book.toggle_favorite(sub)
            if success:
                print(f"[OK] {msg}")
            else:
                print(f"[!] {msg}")


def cli_contact_statistics(book: ContactBook) -> None:
    """CLI flow to view contact statistics."""
    stats = book.get_stats()
    print("\n============================================================")
    print("                  CONTACT STATISTICS")
    print("============================================================")
    print(f"  Total Contacts    : {stats['total']}")
    print(f"  Favorite Contacts : {stats['favorites']}")
    print("============================================================")


def main() -> None:
    """Main CLI execution loop."""
    book = ContactBook()
    display_banner()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            cli_add_contact(book)
        elif choice == "2":
            cli_view_contacts(book)
        elif choice == "3":
            cli_search_contact(book)
        elif choice == "4":
            cli_update_contact(book)
        elif choice == "5":
            cli_delete_contact(book)
        elif choice == "6":
            cli_view_favorites(book)
        elif choice == "7":
            cli_contact_statistics(book)
        elif choice == "8":
            print("\nThank you for using Contact Book. Goodbye!\n")
            break
        else:
            print("\n[!] Invalid option. Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
