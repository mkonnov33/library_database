import sqlite3
from datetime import date, datetime

yeses = ["true", "yes", "t", "y", "+", "sure", "yeah", "ye", "yup"]
noes = ["false", "no", "f", "n", "-", "nope"]

BOOLEAN_FIELDS = {
    "accounts": {"employee"},
    "books": {"featured_in_event"},
    "events": {"active"},
    "leaves": {"paid", "active"},
    "positions": {"available"},
}
DATE_FIELDS = {
    "authors": {"date_of_birth"},
    "books": {"release_date"},
    "events": {"starting_date", "ending_date"},
    "leaves": {"start_date", "end_date"},
}
ACTIVE_DATE_RANGES = {
    "events": ("starting_date", "ending_date"),
    "leaves": ("start_date", "end_date"),
}
def connect():
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    con.execute("PRAGMA foreign_keys = ON")
    try:
        _migrate_database(con, cur)
    except Exception:
        con.close()
        raise
    return con, cur

def normalize_boolean(value):
    """Convert supported yes/no values to bool, rejecting ambiguous input."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in yeses or normalized == "1":
            return True
        if normalized in noes or normalized == "0":
            return False
    raise ValueError(f"Enter a yes/no value, not {value!r}.")

def parse_date(value):
    """Parse supported date values to a date object."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    for date_format in (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
    ):
        try:
            return datetime.strptime(text, date_format).date()
        except ValueError:
            continue
    raise ValueError(
        f"Invalid date {text!r}. Use DD/MM/YYYY."
    )

def normalize_date(value):
    """Parse common date inputs and return DD/MM/YYYY."""
    parsed = parse_date(value)
    return parsed.strftime("%d/%m/%Y") if parsed else None

def _migrate_database(con, cur):
    tables = {row[0] for row in cur.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    )}
    if "leaves" in tables:
        columns = {row[1] for row in cur.execute("PRAGMA table_info(leaves)")}
        if "active" not in columns:
            cur.execute("ALTER TABLE leaves ADD COLUMN active BOOLEAN NOT NULL DEFAULT 0")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS app_migrations (name TEXT PRIMARY KEY)"
    )
    migration_name = "dates_dd_mm_yyyy_v2"
    if not cur.execute(
        "SELECT 1 FROM app_migrations WHERE name = ?", (migration_name,)
    ).fetchone():
        date_columns = {
            "authors": ("date_of_birth",),
            "books": ("release_date",),
            "events": ("starting_date", "ending_date"),
            "leaves": ("start_date", "end_date"),
        }
        for table, columns in date_columns.items():
            if table not in tables:
                continue
            existing_columns = {row[1] for row in cur.execute(f"PRAGMA table_info({table})")}
            for column in columns:
                if column not in existing_columns:
                    continue
                for row_id, value in cur.execute(
                    f"SELECT id, {column} FROM {table} WHERE {column} IS NOT NULL"
                ).fetchall():
                    try:
                        normalized = normalize_date(value)
                    except ValueError as error:
                        raise ValueError(
                            f"Cannot migrate {table}.{column} for record {row_id}: {error}"
                        ) from error
                    if normalized != value:
                        cur.execute(
                            f"UPDATE {table} SET {column} = ? WHERE id = ?",
                            (normalized, row_id),
                        )

        cur.execute("INSERT INTO app_migrations (name) VALUES (?)", (migration_name,))

    con.commit()

def _active_for_range(start_date, end_date):
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
    except (TypeError, ValueError):
        return 0
    if start is None or end is None:
        return 0
    today = date.today()
    return int(start <= today <= end)

#region Add things
def add_account(username, password, employee = False):
    if username == "" or password == "":
        return
    return insert_row("accounts", {
        "username": username,
        "password": password,
        "employee": employee,
    })

def add_author(first_name, last_name, date_of_birth = None):
    if first_name == "" or last_name == "":
        return
    return insert_row("authors", {
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
    })

def add_book(name, release_date, author_id, featured_in_event, event_id = None, genre_id = None):
    if name == "" or release_date == "" or author_id == "":
        return
    return insert_row("books", {
        "name": name,
        "release_date": release_date,
        "author_id": author_id,
        "genre_id": genre_id,
        "featured_in_event": featured_in_event,
        "event_id": event_id,
    })

def add_employee(first_name, last_name, library_id, account_id, position_id, age = None):
    if first_name == "" or last_name == "" or library_id == "" or account_id == "" or position_id == "":
        return
    return insert_row("employees", {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "library_id": library_id,
        "account_id": account_id,
        "position_id": position_id,
    })

def add_event(name, library_id, starting_date, ending_date):
    if name == "" or library_id == "" or starting_date == "" or ending_date == "":
        return
    return insert_row("events", {
        "name": name,
        "library_id": library_id,
        "starting_date": starting_date,
        "ending_date": ending_date,
    })

def add_genre(name, description = None):
    if name == "":
        return
    return insert_row("genres", {"name": name, "description": description})

def add_leave(employee_id, paid, cause, start_date, end_date):
    if employee_id == "" or paid == "" or cause == "" or start_date == "" or end_date == "":
        return
    return insert_row("leaves", {
        "employee_id": employee_id,
        "paid": paid,
        "cause": cause,
        "start_date": start_date,
        "end_date": end_date,
    })

def add_library(name, address):
    if name == "" or address == "":
        return
    return insert_row("libraries", {"name": name, "address": address})

def add_position(name, available, salary = None):
    if name == "" or available == "":
        return
    return insert_row("positions", {
        "name": name,
        "available": available,
        "salary": salary,
    })

def add_reservation(book_id, account_id, library_id):
    if book_id == "" or account_id == "" or library_id == "":
        return
    return insert_row("reservations", {
        "book_id": book_id,
        "account_id": account_id,
        "library_id": library_id,
    })
#endregion

#region Get things
def get_accounts():
    con, cur = connect()
    cur.execute("SELECT id, username, employee FROM accounts")
    accounts = [
        (account_id, username, "[hidden]", employee)
        for account_id, username, employee in cur.fetchall()
    ]
    con.close()
    return accounts

def get_authors():
    con, cur = connect()
    cur.execute("SELECT * FROM authors")
    authors = cur.fetchall()
    con.close()
    return authors

def get_books():
    con, cur = connect()
    cur.execute('''SELECT
                    books.id,
                    books.name,
                    authors.first_name || " " || authors.last_name AS author_name,
                    release_date,
                    genres.name,
                    featured_in_event,
                    events.name
                   FROM books
                   JOIN authors
                       ON books.author_id = authors.id
                   LEFT JOIN genres
                       ON books.genre_id = genres.id
                   LEFT JOIN events
                       ON books.event_id = events.id''')
    books = cur.fetchall()
    con.close()
    return books

def get_employees():
    con, cur = connect()
    cur.execute('''SELECT
                    employees.id, 
                    first_name,
                    last_name,
                    age,
                    libraries.name,
                    libraries.address,
                    accounts.username,
                    positions.name,
                    positions.salary
                   FROM employees
                   JOIN libraries
                       ON employees.library_id = libraries.id
                   JOIN accounts
                       ON employees.account_id = accounts.id
                   JOIN positions
                       ON employees.position_id = positions.id''')
    employees = cur.fetchall()
    con.close()
    return employees

def get_events():
    con, cur = connect()
    cur.execute('''SELECT
                    events.id,
                    libraries.name,
                    libraries.address,
                    events.name,
                    starting_date,
                    ending_date
                   FROM events
                   JOIN libraries
                       ON events.library_id = libraries.id''')
    events = []
    for event_id, library, address, name, starting_date, ending_date in cur.fetchall():
        active = _active_for_range(starting_date, ending_date)
        cur.execute("UPDATE events SET active = ? WHERE id = ? AND active != ?", (
            active, event_id, active
        ))
        events.append((event_id, library, address, name, starting_date, ending_date, active))
    con.commit()
    con.close()
    return events

def get_genres():
    con, cur = connect()
    cur.execute('''SELECT * FROM genres''')
    genres = cur.fetchall()
    con.close()
    return genres

def get_leaves():
    con, cur = connect()
    cur.execute('''SELECT
                    leaves.id,
                    employees.first_name,
                    employees.last_name,
                    paid,
                    cause,
                    start_date,
                    end_date
                   FROM leaves
                   JOIN employees
                       ON leaves.employee_id = employees.id''')
    leaves = []
    for leave_id, employee_first, employee_last, paid, cause, start_date, end_date in cur.fetchall():
        active = _active_for_range(start_date, end_date)
        cur.execute("UPDATE leaves SET active = ? WHERE id = ? AND active != ?", (
            active, leave_id, active
        ))
        leaves.append((leave_id, employee_first, employee_last, paid, cause, start_date, end_date, active))
    con.commit()
    con.close()
    return leaves

def get_libraries():
    con, cur = connect()
    cur.execute('''SELECT * FROM libraries''')
    libraries = cur.fetchall()
    con.close()
    return libraries

def get_positions():
    con, cur = connect()
    cur.execute('''SELECT * FROM positions''')
    positions = cur.fetchall()
    con.close()
    return positions

def get_reservations():
    con, cur = connect()
    cur.execute('''SELECT
                    reservations.id,
                    accounts.username,
                    libraries.name,
                    libraries.address,
                    books.name,
                    authors.first_name,
                    authors.last_name,
                    books.release_date
                   FROM reservations
                   JOIN books
                       ON reservations.book_id = books.id
                   JOIN authors
                       ON books.author_id = authors.id
                   JOIN accounts
                       ON reservations.account_id = accounts.id
                   JOIN libraries
                       ON reservations.library_id = libraries.id''')
    reservations = cur.fetchall()
    con.close()
    return reservations
#endregion

#region List things
def account_list():
    print("\nList of accounts")
    for account in get_accounts():
        account_id, username, _, employee = account
        print(f"ID: {account_id} | Username: {username} | Password: [hidden] | Employee's account: {employee}")

def author_list():
    print("\nList of authors")
    for author in get_authors():
        author_id, first_name, last_name, date_of_birth = author
        if (date_of_birth != None):
            print(f"ID: {author_id} | First name: {first_name} | Last name: {last_name} | Date of birth: {date_of_birth}")
        else:
            print(f"ID: {author_id} | First name: {first_name} | Last name: {last_name}")

def book_list():
    print("\nList of books:")
    for book in get_books():
        book_id, book_name, author_first, author_last, release_date, genre, is_featured, event_name = book


        is_featured = bool(is_featured)
        
        if (is_featured):
            print(f"ID: {book_id} | Title: {book_name} | Author: {author_first} {author_last} | Released: {release_date} | Genre: {genre} | Featured in {event_name}")
        else:
            print(f"ID: {book_id} | Title: {book_name} | Author: {author_first} {author_last} | Released: {release_date} | Genre: {genre}")

def employee_list():
    print("\nList of employees")
    for employee in get_employees():
        employee_id, first_name, last_name, age, library_name, library_address, account_username, position_name, position_salary = employee
        if (age != None):
            print(f"ID: {employee_id} | First name: {first_name} | Last name: {last_name} | Age: {age} | Library: {library_name} {library_address} | Account: {account_username}, | Position: {position_name} {position_salary}")
        else:
            print(f"ID: {employee_id} | First name: {first_name} | Last name: {last_name} | Library: {library_name} {library_address} | Account: {account_username}, | Position: {position_name} {position_salary}")

def event_list():
    print("\nList of events")
    for event in get_events():
        event_id, library_name, library_address, event_name, starting_date, ending_date, active = event
        print(f"ID: {event_id} | Event name: {event_name} | Library: {library_name} {library_address} | From {starting_date} to {ending_date} | Active: {active}")

def genre_list():
    print("\nList of genres")
    for genre in get_genres():
        genre_id, genre_name, genre_description = genre
        if (genre_description != None):
            print(f"ID: {genre_id} | Name: {genre_name} | Description: {genre_description}")
        else:
            print(f"ID: {genre_id} | Name: {genre_name}")

def leave_list():
    print("\nList of leaves")
    for leave in get_leaves():
        leave_id, employee_first, employee_last, paid, cause, start_date, end_date, active = leave
        print(f"ID: {leave_id} | Employee: {employee_first} {employee_last} | Paid?: {paid} | Cause: {cause} | From {start_date} to {end_date} | Active: {active}")

def library_list():
    print("\nList of libraries")
    for library in get_libraries():
        library_id, library_name, library_address = library
        print(f"ID: {library_id} | Name: {library_name} | Address: {library_address}")

def position_list():
    print("\nList of positions")
    for position in get_positions():
        position_id, position_name, available, salary = position
        if (salary != None and salary != 0):
            print(f"ID: {position_id} | Name: {position_name} | Available: {available} | Salary: {salary}")
        else:
            print(f"ID: {position_id} | Name: {position_name} | Available: {available}")

def reservation_list():
    print("\nList of reservations")
    for reservation in get_reservations():
        reservation_id, account_username, library_name, library_address, book_name, author_first, author_last, book_release_date = reservation
        print(f"ID: {reservation_id} | Account: {account_username} | Library: {library_name} {library_address} | Book: {book_name} {book_release_date} | Author: {author_first} {author_last}")
#endregion
#region Edit things
# Fields maps: DB table/column -> user-facing label. "id" excluded, it is fixed.
_edit_targets = {
    "accounts":     [("username", "Username"), ("password", "Password"), ("employee", "Employee (Yes/No)")],
    "authors":      [("first_name", "First Name"), ("last_name", "Last Name"), ("date_of_birth", "Date Of Birth")],
    "books":        [("name", "Name"), ("release_date", "Release Date"), ("author_id", "Author ID"),
                     ("genre_id", "Genre ID"), ("featured_in_event", "Featured In Event (Yes/No)"), ("event_id", "Event ID")],
    "employees":    [("first_name", "First Name"), ("last_name", "Last Name"), ("age", "Age"),
                     ("library_id", "Library ID"), ("account_id", "Account ID"), ("position_id", "Position ID")],
    "events":       [("name", "Name"), ("library_id", "Library ID"), ("starting_date", "Starting Date"),
                     ("ending_date", "Ending Date")],
    "genres":       [("name", "Name"), ("description", "Description")],
    "leaves":       [("employee_id", "Employee ID"), ("paid", "Paid (Yes/No)"), ("cause", "Cause"),
                     ("start_date", "Start Date"), ("end_date", "End Date")],
    "libraries":    [("name", "Name"), ("address", "Address")],
    "positions":    [("name", "Name"), ("available", "Available (Yes/No)"), ("salary", "Salary")],
    "reservations": [("book_id", "Book ID"), ("account_id", "Account ID"), ("library_id", "Library ID")],
}

def get_edit_fields(table):
    """Return [(column, label), ...] editable fields for a table (excluding id)."""
    return _edit_targets[table]

def get_row_by_id(table, row_id):
    """Return a row mapped by column name, or None if the row does not exist."""
    con, cur = connect()
    try:
        cur.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,))
        row = cur.fetchone()
        if row is None:
            return None
        columns = [description[0] for description in cur.description]
        return dict(zip(columns, row))
    finally:
        con.close()

def update_row(table, row_id, values):
    """
    Update an existing row. `values` is a dict {column: new_value} containing
    every editable column of the table (id cannot be changed).
    Returns True on success, False if the row does not exist.
    """
    fields = _edit_targets[table]
    columns = [column for column, _ in fields]
    for column in columns:
        if column not in values:
            raise ValueError(f"Missing value for column '{column}'")
    clean = _normalize_values(table, values)
    if table == "accounts" and not str(values.get("password", "")).strip():
        columns.remove("password")
    if table in ACTIVE_DATE_RANGES:
        start_column, end_column = ACTIVE_DATE_RANGES[table]
        clean["active"] = _active_for_range(clean[start_column], clean[end_column])
        columns.append("active")
    assignments = ", ".join(f"{column} = ?" for column in columns)
    params = [clean[column] for column in columns] + [row_id]
    con, cur = connect()
    cur.execute(f"UPDATE {table} SET {assignments} WHERE id = ?", params)
    changed = cur.rowcount
    con.commit()
    con.close()
    return changed > 0

def delete_row(table, row_id):
    """Delete a row from an editable table and return whether it existed."""
    if table not in _edit_targets:
        raise ValueError(f"Unknown table: {table}")
    con, cur = connect()
    try:
        cur.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
        deleted = cur.rowcount > 0
        con.commit()
        return deleted
    finally:
        con.close()
#endregion

def insert_row(table, values):
    """
    Insert a new row. `values` is a dict {column: value} containing every
    editable column of the table (id is auto-assigned).
    Empty optional fields become NULL. Returns the new row id, or None if the
    required fields are missing.
    """
    fields = _edit_targets[table]
    required = {
        "accounts": ("username", "password"),
        "authors": ("first_name", "last_name"),
        "books": ("name", "release_date", "author_id"),
        "employees": ("first_name", "last_name", "library_id", "account_id", "position_id"),
        "events": ("name", "library_id", "starting_date", "ending_date"),
        "genres": ("name",),
        "leaves": ("employee_id", "paid", "cause", "start_date", "end_date"),
        "libraries": ("name", "address"),
        "positions": ("name", "available"),
        "reservations": ("book_id", "account_id", "library_id"),
    }[table]
    for column in required:
        if str(values.get(column, "")).strip() == "":
            return None
    columns = [column for column, _ in fields]
    clean = _normalize_values(table, values)
    if table in ACTIVE_DATE_RANGES:
        start_column, end_column = ACTIVE_DATE_RANGES[table]
        clean["active"] = _active_for_range(clean[start_column], clean[end_column])
        columns.append("active")
    placeholders = ", ".join("?" for _ in columns)
    con, cur = connect()
    cur.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
        [clean[column] for column in columns],
    )
    con.commit()
    row_id = cur.lastrowid
    con.close()
    return row_id

def _normalize_values(table, values):
    """Normalize editable booleans and dates before writing them to SQLite."""
    normalized = {}
    for field in _edit_targets[table]:
        column = field[0]
        value = values.get(column, "")
        if column in BOOLEAN_FIELDS.get(table, set()):
            if value is None or str(value).strip() == "":
                value = None
            else:
                value = int(normalize_boolean(value))
        elif column in DATE_FIELDS.get(table, set()):
            value = normalize_date(value)
        elif str(value).strip() == "":
            value = None
        normalized[column] = value
    return normalized
