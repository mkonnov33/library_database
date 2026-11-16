# Seeds library.db with sample data. Safe to run multiple times:
# run "python seed_data.py --reset" first to wipe and recreate the database.
import sqlite3
import sys

def reset():
    with open("library.sql", encoding="utf-8") as f:
        con = sqlite3.connect("library.db")
        con.executescript(f.read())
        con.commit()
        con.close()

def connect():
    con = sqlite3.connect("library.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con, con.cursor()

def main():
    con, cur = connect()
    cur.execute("SELECT COUNT(*) FROM authors")
    if cur.fetchone()[0] > 0:
        print("Database already has data, skipping seed. Use --reset to wipe it first.")
        con.close()
        return

    libraries = [
        ("Central Library", "12 Main Street"),
        ("East Branch", "5 Oak Avenue"),
        ("West Branch", "88 Birch Road"),
    ]
    cur.executemany("INSERT INTO libraries (name, address) VALUES (?, ?)", libraries)

    authors = [
        ("Jane", "Austen", "1775-12-16"),
        ("George", "Orwell", "1903-06-25"),
        ("Agatha", "Christie", "1890-09-15"),
        ("Ursula", "Le Guin", "1929-10-21"),
        ("Ray", "Bradbury", "1920-08-22"),
    ]
    cur.executemany("INSERT INTO authors (first_name, last_name, date_of_birth) VALUES (?, ?, ?)", authors)

    genres = [
        ("Fantasy", "Magic, mythical worlds and creatures"),
        ("Science Fiction", "Futuristic technology and space"),
        ("Mystery", "Crime and detective stories"),
        ("Romance", "Love stories"),
        ("Dystopian", "Oppressive future societies"),
    ]
    cur.executemany("INSERT INTO genres (name, description) VALUES (?, ?)", genres)

    positions = [
        ("Librarian", True, 3200.0),
        ("Assistant", True, 2100.0),
        ("Manager", False, 4800.0),
        ("Cleaner", True, 1500.0),
    ]
    cur.executemany("INSERT INTO positions (name, available, salary) VALUES (?, ?, ?)", positions)

    accounts = [
        ("admin", "admin123", True),
        ("jdoe", "hunter2", True),
        ("msmith", "qwerty", False),
    ]
    cur.executemany("INSERT INTO accounts (username, password, employee) VALUES (?, ?, ?)", accounts)

    events = [
        ("Summer Reading Week", 1, "2026-07-01", "2026-07-08", True),
        ("Mystery Month", 2, "2026-09-01", "2026-09-30", True),
        ("Sci-Fi Festival", 3, "2026-05-10", "2026-05-12", False),
    ]
    cur.executemany("INSERT INTO events (name, library_id, starting_date, ending_date, active) VALUES (?, ?, ?, ?, ?)", events)

    books = [
        ("Pride and Prejudice", "1813-01-28", 1, 4, True, 1),
        ("Emma", "1815-12-23", 1, 4, False, None),
        ("1984", "1949-06-08", 2, 5, True, 3),
        ("Animal Farm", "1945-08-17", 2, 5, False, None),
        ("Murder on the Orient Express", "1934-01-01", 3, 3, True, 2),
        ("And Then There Were None", "1939-11-06", 3, 3, False, None),
        ("A Wizard of Earthsea", "1968-11-01", 4, 1, False, None),
        ("The Left Hand of Darkness", "1969-03-01", 4, 2, True, 3),
        ("Fahrenheit 451", "1953-10-19", 5, 2, False, None),
        ("The Martian Chronicles", "1950-05-04", 5, 2, False, None),
    ]
    cur.executemany(
        "INSERT INTO books (name, release_date, author_id, genre_id, featured_in_event, event_id) VALUES (?, ?, ?, ?, ?, ?)",
        books,
    )

    employees = [
        ("John", "Doe", 34, 1, 2, 1),
        ("Mary", "Smith", 29, 1, 2, 3),
        ("Peter", "Jones", 41, 2, 1, 2),
        ("Anna", "Brown", 25, 3, 3, 2),
    ]
    cur.executemany(
        "INSERT INTO employees (first_name, last_name, age, library_id, account_id, position_id) VALUES (?, ?, ?, ?, ?, ?)",
        employees,
    )

    leaves = [
        (1, True, "Annual vacation", "2026-08-01", "2026-08-14"),
        (2, False, "Medical leave", "2026-06-10", "2026-06-24"),
        (3, True, "Family event", "2026-09-05", "2026-09-07"),
    ]
    cur.executemany(
        "INSERT INTO leaves (employee_id, paid, cause, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
        leaves,
    )

    reservations = [
        (1, 3, 1),
        (3, 2, 1),
        (5, 3, 2),
        (7, 2, 3),
        (9, 3, 1),
    ]
    cur.executemany(
        "INSERT INTO reservations (book_id, account_id, library_id) VALUES (?, ?, ?)",
        reservations,
    )

    con.commit()
    con.close()
    print("Database seeded with sample data.")

if __name__ == "__main__":
    if "--reset" in sys.argv:
        reset()
        print("Database schema recreated.")
    main()
