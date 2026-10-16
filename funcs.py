import sqlite3

def connect():
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    con.execute("PRAGMA foreign_keys = ON")
    return con, cur

#region Add things
def add_account(username, password, employee = False):
    if username == "" or password == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO accounts (username, password, employee) VALUES (?, ?, ?)", (username, password, employee))
    con.commit()
    account_id = cur.lastrowid
    con.close()
    return account_id

def add_author(first_name, last_name, date_of_birth = None):
    if first_name == "" or last_name == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO authors (first_name, last_name, date_of_birth) VALUES (?, ?, ?)", (first_name, last_name, date_of_birth))
    con.commit()
    author_id = cur.lastrowid
    con.close()
    return author_id

def add_book(name, release_date, author_id, featured_in_event, event_id = None, genre_id = None):
    if name == "" or release_date == "" or author_id == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO books (name, release_date, author_id, genre_id, featured_in_event, event_id) VALUES (?, ?, ?, ?, ?, ?)", (name, release_date, author_id, genre_id, featured_in_event, event_id))
    con.commit()
    book_id = cur.lastrowid
    con.close()
    return book_id

def add_employee(first_name, last_name, library_id, account_id, position_id, age = None):
    if first_name == "" or last_name == "" or library_id == "" or account_id == "" or position_id == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO employees (first_name, last_name, age, library_id, account_id, position_id) VALUES (?, ?, ?, ?, ?, ?)", (first_name, last_name, age, library_id, account_id, position_id))
    con.commit()
    employee_id = cur.lastrowid
    con.close()
    return employee_id

def add_event(name, library_id, starting_date, ending_date, active):
    if name == "" or library_id == "" or starting_date == "" or ending_date == "" or active == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO events (name, library_id, starting_date, ending_date, active) VALUES (?, ?, ?, ?, ?)", (name, library_id, starting_date, ending_date, active))
    con.commit()
    event_id = cur.lastrowid
    con.close()
    return event_id

def add_genre(name, description = None):
    if name == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO genres (name, description) VALUES (?, ?)", (name, description))
    con.commit()
    genre_id = cur.lastrowid
    con.close()
    return genre_id

def add_leave(employee_id, paid, cause, start_date, end_date):
    if employee_id == "" or paid == "" or cause == "" or start_date == "" or end_date == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO leaves (employee_id, paid, cause, start_date, end_date) VALUES (?, ?, ?, ?, ?)", (employee_id, paid, cause, start_date, end_date))
    con.commit()
    leave_id = cur.lastrowid
    con.close()
    return leave_id

def add_library(name, address):
    if name == "" or address == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO libraries (name, address) VALUES (?, ?)", (name, address))
    con.commit()
    library_id = cur.lastrowid
    con.close()
    return library_id

def add_position(name, available, salary = None):
    if name == "" or available == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO positions (name, available, salary) VALUES (?, ?, ?)", (name, available, salary))
    con.commit()
    position_id = cur.lastrowid
    con.close()
    return position_id

def add_reservation(book_id, account_id, library_id):
    if book_id == "" or account_id == "" or library_id == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO reservations (book_id, account_id, library_id) VALUES (?, ?, ?)", (book_id, account_id, library_id))
    con.commit()
    reservation_id = cur.lastrowid
    con.close()
    return reservation_id
#endregion

#region Get things
def get_accounts():
    con, cur = connect()
    cur.execute("SELECT * FROM accounts")
    accounts = cur.fetchall()
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
                    authors.first_name,
                    authors.last_name,
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
                    position.name,
                    position.salary
                   FROM employees
                   JOIN libraries
                       ON employees.library_id = library.id
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
                    ending_date,
                    active
                   FROM events
                   JOIN libraries
                       ON events.library_id = libraries.id''')
    events = cur.fetchall()
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
    events = cur.fetchall()
    con.close()
    return events

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
                    books.release_date,
                    genres.name
                   FROM reservations
                   JOIN books
                       ON reservations.book_id = books.id
                    JOIN authors
                       ON books.author_id = authors.id
                    JOIN genres
                       ON books.genres_id = genres.id''')
    reservations = cur.fetchall()
    con.close()
    return reservations
#endregion

#region List things
def account_list():
    print("\nList of accounts")
    for account in get_accounts():
        print(account)

def author_list():
    print("\nList of authors")
    for author in get_authors():
        print(author)

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
        print(employee)

def event_list():
    print("\nList of events")
    for event in get_events():
        print(event)

def genre_list():
    print("\nList of genres")
    for genre in get_genres():
        print(genre)

def leave_list():
    print("\nList of leaves")
    for leave in get_leaves():
        print(leave)

def library_list():
    print("\nList of libraries")
    for library in get_libraries():
        print(library)

def position_list():
    print("\nList of positions")
    for position in get_positions():
        print(position)

def reservation_list():
    print("\nList of reservations")
    for reservation in get_reservations():
        print(reservation)
#endregion