# PLACEHOLDER FOR FUTURE REFERENCE

import tkinter as tk
from funcs import *
from funcs import yeses

def addAccountFromWindow():
    username = account_username_input.get()
    password = account_password_input.get()
    add_account(username, password)
    account_username_input.delete(0, tk.END)
    account_password_input.delete(0, tk.END)

def addAuthorFromWindow():
    first_name = author_first_name_input.get()
    last_name = author_last_name_input.get()
    date_of_birth = author_date_of_birth_input.get()
    add_author(first_name, last_name, date_of_birth)
    author_first_name_input.delete(0, tk.END)
    author_last_name_input.delete(0, tk.END)
    author_date_of_birth_input.delete(0, tk.END)

def addBookFromWindow():
    name = book_name_input.get()
    release_date = book_release_date_input.get()
    author_id = book_author_id_input.get()
    featured = book_featured_in_event_input.get()
    if (featured.lower() in yeses):
        featured = True
    event_id = book_event_id_input.get()
    genre_id = book_genre_id_input.get()
    add_book(name, release_date, author_id, featured, event_id, genre_id)
    book_name_input.delete(0, tk.END)
    book_release_date_input.delete(0, tk.END)
    book_author_id_input.delete(0, tk.END)
    book_featured_in_event_input.delete(0, tk.END)
    book_event_id_input.delete(0, tk.END)
    book_genre_id_input.delete(0, tk.END)

def addEmployeeFromWindow():
    first_name = employee_first_name_input.get()
    last_name = employee_last_name_input.get()
    library_id = employee_library_id_input.get()
    account_id = employee_account_id_input.get()
    position_id = employee_position_id_input.get()
    age = employee_age_input.get()
    add_employee(first_name, last_name, library_id, account_id, position_id, age)
    employee_first_name_input.delete(0, tk.END)
    employee_last_name_input.delete(0, tk.END)
    employee_library_id_input.delete(0, tk.END)
    employee_account_id_input.delete(0, tk.END)
    employee_position_id_input.delete(0, tk.END)
    employee_age_input.delete(0, tk.END)

def addEventFromWindow():
    name = event_name_input.get()
    library_id = event_library_id_input.get()
    starting_date = event_starting_date_input.get()
    ending_date = event_ending_date_input.get()
    active = event_active_input.get()
    if (active.lower() in yeses):
        active = True
    add_event(name, library_id, starting_date, ending_date, active)
    event_name_input.delete(0, tk.END)
    event_library_id_input.delete(0, tk.END)
    event_starting_date_input.delete(0, tk.END)
    event_ending_date_input.delete(0, tk.END)
    event_active_input.delete(0, tk.END)

def addGenreFromWindow():
    name = genre_name_input.get()
    description = genre_description_input.get()
    add_genre(name, description)
    genre_name_input.delete(0, tk.END)
    genre_description_input.delete(0, tk.END)

def addLeaveFromWindow():
    employee_id = leave_employee_id_input.get()
    paid = leave_paid_input.get()
    cause = leave_cause_input.get()
    starting_date = leave_starting_date_input.get()
    ending_date = leave_ending_date_input.get()
    add_leave(employee_id, paid, cause, starting_date, ending_date)
    genre_name_input.delete(0, tk.END)
    genre_description_input.delete(0, tk.END)

def addLibraryFromWindow():
    name = library_name_input.get()
    address = library_address_input.get()
    add_library(name, address)
    library_name_input.delete(0, tk.END)
    library_address_input.delete(0, tk.END)

def addPositionFromWindow():
    name = position_name_input.get()
    available = position_available_input.get()
    if (available.lower() in yeses):
        available = True
    salary = position_salary_input.get()
    add_position(name, available, salary)
    position_name_input.delete(0, tk.END)
    position_available_input.delete(0, tk.END)
    position_salary_input.delete(0, tk.END)

def addReservationFromWindow():
    book_id = reservation_book_id_input.get()
    account_id = reservation_account_id_input.get()
    library_id = reservation_library_id_input.get()
    add_reservation(book_id, account_id, library_id)
    reservation_book_id_input.delete(0, tk.END)
    reservation_account_id_input.delete(0, tk.END)
    reservation_library_id_input.delete(0, tk.END)

window = tk.Tk()
window.title("Library database manager")
window.geometry("1000x600")

label = tk.Label(window, text="Library", font=("Arial", 24))
label.pack(pady=20)

#region Add an account
account_block = tk.LabelFrame(
    window,
    text="Add an account",
    padx=10,
    pady=10
)
account_block.pack(padx=20, pady=20, fill="x")
tk.Label(account_block, text="Username").pack()
account_username_input = tk.Entry(account_block, width=40)
account_username_input.pack(pady=5)
tk.Label(account_block, text="Password").pack()
account_password_input = tk.Entry(account_block, width=40)
account_password_input.pack(pady=5)
result = tk.Label(account_block, text="", fg="green")
result.pack()
account_button = tk.Button(account_block, text="Add", command=addAccountFromWindow)
account_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add an author
author_block = tk.LabelFrame(
    window,
    text="Add an author",
    padx=10,
    pady=10
)
author_block.pack(padx=20, pady=20, fill="x")
tk.Label(author_block, text="First name").pack()
author_first_name_input = tk.Entry(author_block, width=40)
author_first_name_input.pack(pady=5)
tk.Label(author_block, text="Last name").pack()
author_last_name_input = tk.Entry(author_block, width=40)
author_last_name_input.pack(pady=5)
tk.Label(author_block, text="Date of birth").pack()
author_date_of_birth_input = tk.Entry(author_block, width=40)
author_date_of_birth_input.pack(pady=5)
result = tk.Label(author_block, text="", fg="green")
result.pack()
author_button = tk.Button(author_block, text="Add", command=addAuthorFromWindow)
author_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a book
book_block = tk.LabelFrame(
    window,
    text="Add a book",
    padx=10,
    pady=10
)
book_block.pack(padx=20, pady=20, fill="x")
tk.Label(book_block, text="Name").pack()
book_name_input = tk.Entry(book_block, width=40)
book_name_input.pack(pady=5)
tk.Label(book_block, text="Release date").pack()
book_release_date_input = tk.Entry(book_block, width=40)
book_release_date_input.pack(pady=5)
tk.Label(book_block, text="Author ID").pack()
book_author_id_input = tk.Entry(book_block, width=40)
book_author_id_input.pack(pady=5)
tk.Label(book_block, text="Featured in event?").pack()
book_featured_in_event_input = tk.Entry(book_block, width=40)
book_featured_in_event_input.pack(pady=5)
tk.Label(book_block, text="Event ID").pack()
book_event_id_input = tk.Entry(book_block, width=40)
book_event_id_input.pack(pady=5)
tk.Label(book_block, text="Genre ID").pack()
book_genre_id_input = tk.Entry(book_block, width=40)
book_genre_id_input.pack(pady=5)
result = tk.Label(book_block, text="", fg="green")
result.pack()
book_button = tk.Button(book_block, text="Add", command=addBookFromWindow)
book_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add an employee
employee_block = tk.LabelFrame(
    window,
    text="Add an employee",
    padx=10,
    pady=10
)
employee_block.pack(padx=20, pady=20, fill="x")
tk.Label(employee_block, text="First name").pack()
employee_first_name_input = tk.Entry(employee_block, width=40)
employee_first_name_input.pack(pady=5)
tk.Label(employee_block, text="Last name").pack()
employee_last_name_input = tk.Entry(employee_block, width=40)
employee_last_name_input.pack(pady=5)
tk.Label(employee_block, text="Library ID").pack()
employee_library_id_input = tk.Entry(employee_block, width=40)
employee_library_id_input.pack(pady=5)
tk.Label(employee_block, text="Account ID").pack()
employee_account_id_input = tk.Entry(employee_block, width=40)
employee_account_id_input.pack(pady=5)
tk.Label(employee_block, text="Position ID").pack()
employee_position_id_input = tk.Entry(employee_block, width=40)
employee_position_id_input.pack(pady=5)
tk.Label(employee_block, text="Age").pack()
employee_age_input = tk.Entry(employee_block, width=40)
employee_age_input.pack(pady=5)
result = tk.Label(employee_block, text="", fg="green")
result.pack()
employee_button = tk.Button(employee_block, text="Add", command=addEmployeeFromWindow)
employee_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add an event
event_block = tk.LabelFrame(
    window,
    text="Add an event",
    padx=10,
    pady=10
)
event_block.pack(padx=20, pady=20, fill="x")
tk.Label(event_block, text="Name").pack()
event_name_input = tk.Entry(event_block, width=40)
event_name_input.pack(pady=5)
tk.Label(event_block, text="Library ID").pack()
event_library_id_input = tk.Entry(event_block, width=40)
event_library_id_input.pack(pady=5)
tk.Label(event_block, text="Starting date").pack()
event_starting_date_input = tk.Entry(event_block, width=40)
event_starting_date_input.pack(pady=5)
tk.Label(event_block, text="Ending date").pack()
event_ending_date_input = tk.Entry(event_block, width=40)
event_ending_date_input.pack(pady=5)
tk.Label(event_block, text="Active").pack()
event_active_input = tk.Entry(event_block, width=40)
event_active_input.pack(pady=5)
result = tk.Label(event_block, text="", fg="green")
result.pack()
event_button = tk.Button(event_block, text="Add", command=addEventFromWindow)
event_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a genre
genre_block = tk.LabelFrame(
    window,
    text="Add a genre",
    padx=10,
    pady=10
)
genre_block.pack(padx=20, pady=20, fill="x")
tk.Label(genre_block, text="Username").pack()
genre_name_input = tk.Entry(genre_block, width=40)
genre_name_input.pack(pady=5)
tk.Label(genre_block, text="Password").pack()
genre_description_input = tk.Entry(genre_block, width=40)
genre_description_input.pack(pady=5)
result = tk.Label(genre_block, text="", fg="green")
result.pack()
genre_button = tk.Button(genre_block, text="Add", command=addGenreFromWindow)
genre_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a leave
leave_block = tk.LabelFrame(
    window,
    text="Add a leave",
    padx=10,
    pady=10
)
leave_block.pack(padx=20, pady=20, fill="x")
tk.Label(leave_block, text="Employee ID").pack()
leave_employee_id_input = tk.Entry(leave_block, width=40)
leave_employee_id_input.pack(pady=5)
tk.Label(leave_block, text="Paid").pack()
leave_paid_input = tk.Entry(leave_block, width=40)
leave_paid_input.pack(pady=5)
tk.Label(leave_block, text="Cause").pack()
leave_cause_input = tk.Entry(leave_block, width=40)
leave_cause_input.pack(pady=5)
tk.Label(leave_block, text="Starting date").pack()
leave_starting_date_input = tk.Entry(leave_block, width=40)
leave_starting_date_input.pack(pady=5)
tk.Label(leave_block, text="Ending date").pack()
leave_ending_date_input = tk.Entry(leave_block, width=40)
leave_ending_date_input.pack(pady=5)
result = tk.Label(leave_block, text="", fg="green")
result.pack()
leave_button = tk.Button(leave_block, text="Add", command=addLeaveFromWindow)
leave_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a library
library_block = tk.LabelFrame(
    window,
    text="Add an account",
    padx=10,
    pady=10
)
library_block.pack(padx=20, pady=20, fill="x")
tk.Label(library_block, text="Name").pack()
library_name_input = tk.Entry(library_block, width=40)
library_name_input.pack(pady=5)
tk.Label(library_block, text="Address").pack()
library_address_input = tk.Entry(library_block, width=40)
library_address_input.pack(pady=5)
result = tk.Label(library_block, text="", fg="green")
result.pack()
account_button = tk.Button(library_block, text="Add", command=addLibraryFromWindow)
account_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a position
position_block = tk.LabelFrame(
    window,
    text="Add a position",
    padx=10,
    pady=10
)
position_block.pack(padx=20, pady=20, fill="x")
tk.Label(position_block, text="Name").pack()
position_name_input = tk.Entry(position_block, width=40)
position_name_input.pack(pady=5)
tk.Label(position_block, text="Available?").pack()
position_available_input = tk.Entry(position_block, width=40)
position_available_input.pack(pady=5)
tk.Label(position_block, text="Salary").pack()
position_salary_input = tk.Entry(position_block, width=40)
position_salary_input.pack(pady=5)
result = tk.Label(position_block, text="", fg="green")
result.pack()
account_button = tk.Button(position_block, text="Add", command=addPositionFromWindow)
account_button.pack(pady=10)
label.pack(pady=20)
#endregion

#region Add a reservation
reservation_block = tk.LabelFrame(
    window,
    text="Add a reservation",
    padx=10,
    pady=10
)
reservation_block.pack(padx=20, pady=20, fill="x")
tk.Label(reservation_block, text="Book ID").pack()
reservation_book_id_input = tk.Entry(reservation_block, width=40)
reservation_book_id_input.pack(pady=5)
tk.Label(reservation_block, text="Account ID").pack()
reservation_account_id_input = tk.Entry(reservation_block, width=40)
reservation_account_id_input.pack(pady=5)
tk.Label(reservation_block, text="Library ID").pack()
reservation_library_id_input = tk.Entry(reservation_block, width=40)
reservation_library_id_input.pack(pady=5)
result = tk.Label(reservation_block, text="", fg="green")
result.pack()
account_button = tk.Button(reservation_block, text="Add", command=addReservationFromWindow)
account_button.pack(pady=10)
label.pack(pady=20)
#endregion

window.mainloop()