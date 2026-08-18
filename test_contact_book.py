#!/usr/bin/env python3
"""
Unit Test Suite for CodSoft Python Programming Internship - Task 5: Contact Book
=============================================================================
Tests business logic, field validations, monotonic ID generation, CRUD operations,
JSON persistence, corrupted JSON non-destructive recovery, duplicate phone detection,
favorites, and statistics.
"""

import json
import os
import shutil
import tempfile
import unittest
from typing import Dict, Any

from Task5_ContactBook.contact_book import (
    ContactBook,
    validate_name,
    validate_phone,
    validate_email,
    validate_address,
    normalize_phone,
)


class TestValidationFunctions(unittest.TestCase):
    """Test standalone field validation helper functions."""

    def test_validate_name(self) -> None:
        """Test name validation rules."""
        self.assertTrue(validate_name("Pavan Kumar")[0])
        self.assertTrue(validate_name("A")[0])
        self.assertFalse(validate_name("")[0])
        self.assertFalse(validate_name("   ")[0])
        self.assertFalse(validate_name("A" * 101)[0])

    def test_validate_phone(self) -> None:
        """Test phone validation rules."""
        self.assertTrue(validate_phone("9876543210")[0])
        self.assertTrue(validate_phone("+91 9876543210")[0])
        self.assertTrue(validate_phone("98765-43210")[0])
        self.assertTrue(validate_phone("(080) 2345678")[0])

        self.assertFalse(validate_phone("")[0])
        self.assertFalse(validate_phone("   ")[0])
        self.assertFalse(validate_phone("abc")[0])
        self.assertFalse(validate_phone("12345")[0])  # too short (<7 digits)

    def test_validate_email(self) -> None:
        """Test email validation rules."""
        self.assertTrue(validate_email("pavan@example.com")[0])
        self.assertTrue(validate_email("pavan.kumar@sub.domain.in")[0])

        self.assertFalse(validate_email("")[0])
        self.assertFalse(validate_email("   ")[0])
        self.assertFalse(validate_email("plainaddress")[0])
        self.assertFalse(validate_email("@example.com")[0])
        self.assertFalse(validate_email("pavan@")[0])

    def test_validate_address(self) -> None:
        """Test address validation rules."""
        self.assertTrue(validate_address("Bengaluru, Karnataka")[0])
        self.assertFalse(validate_address("")[0])
        self.assertFalse(validate_address("   ")[0])

    def test_normalize_phone(self) -> None:
        """Test phone normalization to raw digits."""
        self.assertEqual(normalize_phone("+91 98765-43210"), "919876543210")
        self.assertEqual(normalize_phone("(080) 123-4567"), "0801234567")


class TestContactBookCore(unittest.TestCase):
    """Test ContactBook core operations using isolated temporary directory."""

    def setUp(self) -> None:
        """Set up a fresh temporary directory and data file for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_contacts.json")
        self.book = ContactBook(data_file=self.test_data_file)

    def tearDown(self) -> None:
        """Clean up temporary directory after each test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initial_empty_state(self) -> None:
        """Test that a new ContactBook starts with no contacts."""
        self.assertEqual(len(self.book.get_all_contacts()), 0)
        self.assertEqual(self.book.get_stats()["total"], 0)

    def test_add_contact_success(self) -> None:
        """Test successfully adding a contact."""
        success, msg, contact = self.book.add_contact(
            name="Pavan Kumar",
            phone="9876543210",
            email="pavan@example.com",
            address="Bengaluru",
            favorite=True,
        )
        self.assertTrue(success)
        self.assertIsNotNone(contact)
        self.assertEqual(contact["id"], "C001")
        self.assertEqual(contact["name"], "Pavan Kumar")
        self.assertEqual(contact["phone"], "9876543210")
        self.assertEqual(contact["email"], "pavan@example.com")
        self.assertEqual(contact["address"], "Bengaluru")
        self.assertTrue(contact["favorite"])
        self.assertEqual(len(self.book.get_all_contacts()), 1)

    def test_add_contact_validation_failures(self) -> None:
        """Test that invalid inputs fail during contact addition."""
        # Invalid name
        success, msg, _ = self.book.add_contact("", "9876543210", "pavan@example.com", "Bengaluru")
        self.assertFalse(success)

        # Invalid phone
        success, msg, _ = self.book.add_contact("Pavan", "invalid-phone", "pavan@example.com", "Bengaluru")
        self.assertFalse(success)

        # Invalid email
        success, msg, _ = self.book.add_contact("Pavan", "9876543210", "bad-email", "Bengaluru")
        self.assertFalse(success)

        # Invalid address
        success, msg, _ = self.book.add_contact("Pavan", "9876543210", "pavan@example.com", "")
        self.assertFalse(success)

    def test_monotonic_id_generation(self) -> None:
        """Test that IDs increase monotonically and remain stable after deletion."""
        self.book.add_contact("Alice", "9111111111", "alice@example.com", "City A")  # C001
        self.book.add_contact("Bob", "9222222222", "bob@example.com", "City B")      # C002
        self.book.add_contact("Charlie", "9333333333", "charlie@example.com", "City C")# C003

        # Delete C002
        self.book.delete_contact("C002")

        # C003 must remain C003
        charlie = self.book.get_contact_by_id("C003")
        self.assertIsNotNone(charlie)
        self.assertEqual(charlie["name"], "Charlie")

        # Next added contact must be C004 (monotonic increment)
        _, _, david = self.book.add_contact("David", "9444444444", "david@example.com", "City D")
        self.assertEqual(david["id"], "C004")

    def test_duplicate_phone_detection(self) -> None:
        """Test detecting existing phone numbers."""
        self.book.add_contact("Pavan Kumar", "+91 98765 43210", "pavan@example.com", "Bengaluru")

        # Exact match check
        dup = self.book.check_duplicate_phone("9876543210")
        self.assertIsNotNone(dup)
        self.assertEqual(dup["id"], "C001")

        # Non-matching check
        nodup = self.book.check_duplicate_phone("9123456789")
        self.assertIsNone(nodup)

    def test_search_contacts(self) -> None:
        """Test searching contacts by name, phone, and partial/case-insensitive queries."""
        self.book.add_contact("Pavan Kumar", "9876543210", "pavan@example.com", "Bengaluru")
        self.book.add_contact("Rahul Sharma", "9988776655", "rahul@example.com", "Mumbai")

        # Search by partial name (case-insensitive)
        results = self.book.search_contacts("pavan", search_type="name")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "C001")

        # Search by phone substring
        results = self.book.search_contacts("9988", search_type="phone")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "C002")

        # Search by non-existent query
        results = self.book.search_contacts("NonExistent", search_type="all")
        self.assertEqual(len(results), 0)

    def test_update_contact(self) -> None:
        """Test updating contact fields."""
        self.book.add_contact("Pavan Kumar", "9876543210", "pavan@example.com", "Bengaluru")

        # Update partial fields
        success, msg = self.book.update_contact(
            contact_id="C001",
            phone="9999988888",
            address="Mysuru, Karnataka",
        )
        self.assertTrue(success)

        updated = self.book.get_contact_by_id("C001")
        self.assertEqual(updated["name"], "Pavan Kumar")  # Retained original
        self.assertEqual(updated["phone"], "9999988888") # Updated
        self.assertEqual(updated["address"], "Mysuru, Karnataka") # Updated

        # Update non-existent ID
        success, msg = self.book.update_contact("C999", name="Nobody")
        self.assertFalse(success)

    def test_delete_contact(self) -> None:
        """Test deleting a contact."""
        self.book.add_contact("Pavan Kumar", "9876543210", "pavan@example.com", "Bengaluru")
        self.assertEqual(len(self.book.get_all_contacts()), 1)

        # Delete existing contact
        success, msg = self.book.delete_contact("C001")
        self.assertTrue(success)
        self.assertEqual(len(self.book.get_all_contacts()), 0)

        # Delete non-existent contact
        success, msg = self.book.delete_contact("C001")
        self.assertFalse(success)

    def test_favorites_and_stats(self) -> None:
        """Test favorites list and statistics helper methods."""
        self.book.add_contact("Pavan", "9876543210", "p@ex.com", "Blr", favorite=True)
        self.book.add_contact("Rahul", "9988776655", "r@ex.com", "Mum", favorite=False)

        favs = self.book.get_favorites()
        self.assertEqual(len(favs), 1)
        self.assertEqual(favs[0]["name"], "Pavan")

        # Toggle favorite on Rahul
        self.book.toggle_favorite("C002")
        stats = self.book.get_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["favorites"], 2)

    def test_persistence_across_instances(self) -> None:
        """Test that contacts persist to disk and re-load accurately."""
        self.book.add_contact("Pavan Kumar", "9876543210", "pavan@example.com", "Bengaluru")
        self.book.add_contact("Rahul Sharma", "9988776655", "rahul@example.com", "Mumbai")

        # Re-instantiate ContactBook reading from same test file
        book2 = ContactBook(data_file=self.test_data_file)
        self.assertEqual(len(book2.get_all_contacts()), 2)
        self.assertIsNotNone(book2.get_contact_by_id("C001"))
        self.assertIsNotNone(book2.get_contact_by_id("C002"))

        # Verify next ID generated by new instance is C003
        _, _, c3 = book2.add_contact("Ananya", "9123456789", "a@ex.com", "Hyd")
        self.assertEqual(c3["id"], "C003")

    def test_corrupted_json_recovery(self) -> None:
        """
        Test that corrupted JSON is preserved, backed up as contacts.json.corrupt-*,
        and recovery proceeds with empty contact list without throwing an exception.
        """
        # Write corrupted JSON content
        with open(self.test_data_file, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON CORRUPTED FILE CONTENT ...")

        book_corrupt = ContactBook(data_file=self.test_data_file)

        # 1. Original file was NOT overwritten with empty JSON
        with open(self.test_data_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("INVALID JSON", content)

        # 2. Backup file contacts.json.corrupt-* exists in directory
        dir_files = os.listdir(self.temp_dir)
        corrupt_backups = [f for f in dir_files if f.startswith("test_contacts.json.corrupt-")]
        self.assertEqual(len(corrupt_backups), 1)

        # 3. Application initialized empty contact list safely
        self.assertEqual(len(book_corrupt.get_all_contacts()), 0)


if __name__ == "__main__":
    unittest.main()
