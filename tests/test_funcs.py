import contextlib
import io
import os
import sqlite3
import tempfile
import unittest
from datetime import date, timedelta

import funcs


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DatabaseFunctionTests(unittest.TestCase):
    def setUp(self):
        self.original_directory = os.getcwd()
        self.temp_directory = tempfile.TemporaryDirectory()
        os.chdir(self.temp_directory.name)
        with open(os.path.join(ROOT, "library.sql"), encoding="utf-8") as schema:
            con = sqlite3.connect("library.db")
            con.executescript(schema.read())
            con.commit()
            con.close()

    def tearDown(self):
        os.chdir(self.original_directory)
        self.temp_directory.cleanup()

    def query(self, statement, parameters=()):
        con = sqlite3.connect("library.db")
        try:
            return con.execute(statement, parameters).fetchone()
        finally:
            con.close()

    def test_account_passwords_are_stored_and_hidden(self):
        password = "test password"
        account_id = funcs.add_account("reader", password, "no")

        stored_password, employee = self.query(
            "SELECT password, employee FROM accounts WHERE id = ?", (account_id,)
        )
        self.assertEqual(stored_password, password)
        self.assertEqual(employee, 0)
        self.assertEqual(funcs.get_accounts()[0][2], "[hidden]")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            funcs.account_list()
        self.assertNotIn(password, output.getvalue())

    def test_dates_migrate_after_older_date_migration(self):
        con = sqlite3.connect("library.db")
        con.execute(
            "INSERT INTO authors (first_name, last_name, date_of_birth) VALUES (?, ?, ?)",
            ("Legacy", "Author", "2000-02-01"),
        )
        con.execute("CREATE TABLE app_migrations (name TEXT PRIMARY KEY)")
        con.execute(
            "INSERT INTO app_migrations (name) VALUES (?)",
            ("dates_dd_mm_yyyy_v1",),
        )
        con.commit()
        con.close()

        funcs.connect()[0].close()

        author_date, = self.query(
            "SELECT date_of_birth FROM authors WHERE first_name = ?", ("Legacy",)
        )
        self.assertEqual(author_date, "01/02/2000")

    def test_book_input_normalizes_date_and_boolean(self):
        author_id = funcs.add_author("Jane", "Reader")
        book_id = funcs.add_book(
            "A Book", "2020-01-02", author_id, "no"
        )

        release_date, featured = self.query(
            "SELECT release_date, featured_in_event FROM books WHERE id = ?",
            (book_id,),
        )
        self.assertEqual(release_date, "02/01/2020")
        self.assertEqual(featured, 0)

    def test_event_input_normalizes_dates_and_computes_activity(self):
        library_id = funcs.add_library("Central", "1 Main Street")
        start = date.today()
        end = start + timedelta(days=1)
        event_id = funcs.add_event(
            "Reading", library_id, start.isoformat(), end.isoformat()
        )

        starting_date, ending_date, active = self.query(
            "SELECT starting_date, ending_date, active FROM events WHERE id = ?",
            (event_id,),
        )
        self.assertEqual(starting_date, start.strftime("%d/%m/%Y"))
        self.assertEqual(ending_date, end.strftime("%d/%m/%Y"))
        self.assertEqual(active, 1)
        row = funcs.get_row_by_id("events", event_id)
        self.assertEqual(row["starting_date"], starting_date)
        self.assertEqual(row["active"], active)

    def test_account_update_keeps_password_when_blank(self):
        account_id = funcs.add_account("reader", "first password", True)
        row = funcs.get_row_by_id("accounts", account_id)
        self.assertEqual(row["username"], "reader")
        original, = self.query(
            "SELECT password FROM accounts WHERE id = ?", (account_id,)
        )

        funcs.update_row(
            "accounts",
            account_id,
            {"username": "reader", "password": "", "employee": "no"},
        )

        current, employee = self.query(
            "SELECT password, employee FROM accounts WHERE id = ?", (account_id,)
        )
        self.assertEqual(current, original)
        self.assertEqual(employee, 0)

        funcs.update_row(
            "accounts",
            account_id,
            {"username": "reader", "password": "second password", "employee": "no"},
        )
        updated, = self.query(
            "SELECT password FROM accounts WHERE id = ?", (account_id,)
        )
        self.assertEqual(updated, "second password")
        self.assertNotEqual(updated, original)


if __name__ == "__main__":
    unittest.main()
