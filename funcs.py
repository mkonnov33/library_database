import sqlite3

yeses = ["true", "yes", "t", "y", "+", "sure", "yeah", "ye", "yup"]

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
                    positions.name,
                    positions.salary
                    positions.name,
                    positions.salary
                   FROM employees
                   JOIN libraries
                       ON employees.library_id = libraries.id
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
        account_id, username, password, employee = account
        print(f"ID: {account_id} | Username: {username} | Password: {password} | Employee's account: {employee}")
        account_id, username, password, employee = account
        print(f"ID: {account_id} | Username: {username} | Password: {password} | Employee's account: {employee}")

def author_list():
    print("\nList of authors")
    for author in get_authors():
        author_id, first_name, last_name, date_of_birth = author
        if (date_of_birth != None):
            print(f"ID: {author_id} | First name: {first_name} | Last name: {last_name} | Date of birth: {date_of_birth}")
        else:
            print(f"ID: {author_id} | First name: {first_name} | Last name: {last_name}")
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
        genre_id, genre_name, genre_description = genre
        if (genre_description != None):
            print(f"ID: {genre_id} | Name: {genre_name} | Description: {genre_description}")
        else:
            print(f"ID: {genre_id} | Name: {genre_name}")

def leave_list():
    print("\nList of leaves")
    for leave in get_leaves():
        leave_id, employee_first, employee_last, paid, cause, start_date, end_date = leave
        print(f"ID: {leave_id} | Employee: {employee_first} {employee_last} | Paid?: {paid} | Cause: {cause} | From {start_date} to {end_date}")
        leave_id, employee_first, employee_last, paid, cause, start_date, end_date = leave
        print(f"ID: {leave_id} | Employee: {employee_first} {employee_last} | Paid?: {paid} | Cause: {cause} | From {start_date} to {end_date}")

def library_list():
    print("\nList of libraries")
    for library in get_libraries():
        library_id, library_name, library_address = library
        print(f"ID: {library_id} | Name: {library_name} | Address: {library_address}")
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
