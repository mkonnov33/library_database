# Library Database Manager

A small Python application for managing a library database. It includes a
desktop interface built with Tkinter and a menu-driven command-line interface.
Both interfaces use SQLite and the local `library.db` database.

![Library database manager](https://github.com/user-attachments/assets/1bf2a860-87e2-4c3e-b958-158bb0477abb)

## Features

Manage the following records:

- Accounts
- Authors
- Books
- Employees
- Events
- Genres
- Leaves
- Libraries
- Positions
- Reservations

The desktop app (`app.py`) provides searchable tables and forms to add, update,
and delete records. Select a row to load its values into the form; deleting a
record requires confirmation. Records referenced by other records cannot be
deleted until those references are removed.

Boolean fields use Yes/No choices. Date fields are normalized to
`DD/MM/YYYY`. Events and leaves are marked active when today's date falls
between their start and end dates, inclusive. These normalizations also apply
to records added through the command-line interface.

Account passwords are stored as entered, but are hidden in account listings.
When editing an account, leave the password field blank to keep its current
password.

The command-line app (`terminal.py`) provides menus for adding records and
listing database contents.

## Requirements

- Python 3.10 or newer
- Tkinter for the desktop interface (usually included with Python)
- SQLite (included with Python)

No third-party Python packages are required.

## Getting started

Clone the repository and change into its directory:

```bash
git clone https://github.com/mkonnov33/library_database.git
cd library_database
```

The repository includes a sample `library.db`. To start the desktop app:

```bash
python app.py
```

To use the command-line interface instead:

```bash
python terminal.py
```

Run these commands from the project directory so the applications use the
expected `library.db` file.

### Initialize an empty database

If `library.db` is missing or empty, create the schema and populate it with
sample records:

```bash
python seed_data.py --reset
```

The seed script skips adding sample records when it detects existing authors.
It is safe to run on an already populated database; it does not erase existing
records.

## Data and dates

The SQLite database is stored in `library.db`. Its schema is defined in
`library.sql`. The `seed_data.py` script contains example libraries, books,
authors, staff, events, and related records.

Dates are displayed and stored as `DD/MM/YYYY`. Existing ISO-formatted dates
are converted automatically when the application opens the database.
Event and leave activity is calculated from each record's date range.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Tkinter desktop application |
| `terminal.py` | Menu-driven command-line application |
| `funcs.py` | Shared database operations and data helpers |
| `library.sql` | SQLite table definitions |
| `library.db` | Local database with sample data |
| `seed_data.py` | Creates sample records in an empty database |
