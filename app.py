# PLACEHOLDER FOR FUTURE REFERENCE

import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from funcs import *
from funcs import yeses

#region Setup
window = tk.Tk()
window.title("Library database manager")
window.geometry("1000x600")

label = tk.Label(window, text="Library", font=("Arial", 24))
label.pack(pady=10)

# --- Main subtabs (one per table) ---
tabControl = ttk.Notebook(window)

tab_account = ttk.Frame(tabControl)
tab_author = ttk.Frame(tabControl)
tab_book = ttk.Frame(tabControl)
tab_employee = ttk.Frame(tabControl)
tab_event = ttk.Frame(tabControl)
tab_genre = ttk.Frame(tabControl)
tab_leave = ttk.Frame(tabControl)
tab_library = ttk.Frame(tabControl)
tab_position = ttk.Frame(tabControl)
tab_reservation = ttk.Frame(tabControl)

tabControl.add(tab_account, text='Account')
tabControl.add(tab_author, text='Author')
tabControl.add(tab_book, text='Book')
tabControl.add(tab_employee, text='Employee')
tabControl.add(tab_event, text='Event')
tabControl.add(tab_genre, text='Genre')
tabControl.add(tab_leave, text='Leave')
tabControl.add(tab_library, text='Library')
tabControl.add(tab_position, text='Position')
tabControl.add(tab_reservation, text='Reservation')

tabControl.pack(expand=1, fill="both", padx=10, pady=10)
#endregion

#region Get UI
# --- Tables + forms for each tab ---
def make_table_tab(tab, title, columns, headings, data_func, edit_table):
    """Builds one tab: data form on top (Add / Edit Selected), table below."""
    fields = get_edit_fields(edit_table)

    #region Form
    form_block = tk.LabelFrame(
        tab,
        text=f"Add a {edit_table[:-1]}",
        padx=10,
        pady=10
    )
    form_block.pack(padx=20, pady=10, fill="x")

    inputs = []
    for index, (column, field_label) in enumerate(fields):
        row, col = divmod(index, 3)
        tk.Label(form_block, text=field_label).grid(row=row * 2, column=col, sticky="w", padx=10)
        entry = tk.Entry(form_block, width=30)
        entry.grid(row=row * 2 + 1, column=col, padx=10, pady=(0, 8))
        inputs.append((column, entry))

    editing_id = [None]

    def set_editing_label():
        if editing_id[0] is None:
            form_block.configure(text=f"Add a {edit_table[:-1]}")
        else:
            form_block.configure(text=f"Editing {edit_table[:-1]} (ID {editing_id[0]})")

    def clear_form():
        editing_id[0] = None
        for _column, entry in inputs:
            entry.delete(0, tk.END)
        set_editing_label()

    def add_from_form():
        values = {column: entry.get() for column, entry in inputs}
        if editing_id[0] is None:
            insert_row(edit_table, values)
        else:
            update_row(edit_table, editing_id[0], values)
        clear_form()
        refresh()

    def edit_selected():
        selected = tree.selection()
        if not selected:
            return
        row = tree.item(selected[0], "values")
        row_id = row[0]
        current = get_row_by_id(edit_table, row_id)
        if current is None:
            return
        # Map raw row (id, ...) into the form fields.
        raw_columns = ["id"] + [column for column, _ in fields]
        current_values = dict(zip(raw_columns, current))
        editing_id[0] = row_id
        for column, entry in inputs:
            entry.delete(0, tk.END)
            value = current_values[column]
            entry.insert(0, "" if value is None else str(value))
        set_editing_label()

    #region Buttons
    button_bar = tk.Frame(form_block)
    button_bar.grid(row=((len(fields) - 1) // 3 + 1) * 2, column=0, columnspan=3, pady=(5, 0))
    save_button = tk.Button(button_bar, text="Add", command=add_from_form)
    save_button.pack(side="left", padx=5)
    edit_button = tk.Button(button_bar, text="Edit Selected", command=edit_selected)
    edit_button.pack(side="left", padx=5)
    clear_button_form = tk.Button(button_bar, text="Clear", command=clear_form)
    clear_button_form.pack(side="left", padx=5)
    #endregion
    #endregion

    #region Table
    table_block = tk.LabelFrame(
        tab,
        text=title,
        padx=10,
        pady=10
    )
    table_block.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    rows = []

    def refresh():
        tree.delete(*tree.get_children())
        rows.clear()
        rows.extend(data_func())
        apply_filter()

    def apply_filter(*_):
        query = search_input.get().lower()
        tree.delete(*tree.get_children())
        for row in rows:
            if query in " ".join(str(value) for value in row).lower():
                tree.insert("", "end", values=row)

    search_bar = tk.Frame(table_block)
    search_bar.pack(side="top", pady=5, fill="x")
    tk.Label(search_bar, text="Search:").pack(side="left")
    search_input = tk.Entry(search_bar, width=40)
    search_input.pack(side="left", padx=5)
    search_input.bind("<KeyRelease>", apply_filter)
    clear_button = tk.Button(search_bar, text="Clear", command=lambda: (search_input.delete(0, tk.END), apply_filter()))
    clear_button.pack(side="left")
    refresh_button = tk.Button(search_bar, text="Refresh", command=refresh)
    refresh_button.pack(side="left", padx=5)

    tree = ttk.Treeview(table_block, columns=columns, show="headings")

    for column, heading in zip(columns, headings):
        tree.heading(column, text=heading)
        tree.column(column, width=120, anchor="w")

    scrollbar = Scrollbar(table_block, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tree.bind("<Double-1>", lambda _event: edit_selected())
    #endregion

    refresh()

# Account
make_table_tab(
    tab_account,
    "Accounts",
    ("id", "username", "password", "employee_id"),
    ("ID", "Username", "Password", "Employee ID"),
    get_accounts,
    "accounts"
)

# Author
make_table_tab(
    tab_author,
    "Authors",
    ("id", "first_name", "last_name", "date_of_birth"),
    ("ID", "First Name", "Last Name", "Date Of Birth"),
    get_authors,
    "authors"
)

# Book
make_table_tab(
    tab_book,
    "Books",
    ("id", "name", "author", "release_date", "genre", "featured_in_event", "event"),
    ("ID", "Name", "Author", "Release Date", "Genre", "Featured In Event", "Event"),
    get_books,
    "books"
)

# Employee
make_table_tab(
    tab_employee,
    "Employees",
    ("id", "first_name", "last_name", "age", "library", "address", "username", "position", "salary"),
    ("ID", "First Name", "Last Name", "Age", "Library", "Address", "Username", "Position", "Salary"),
    get_employees,
    "employees"
)

# Event
make_table_tab(
    tab_event,
    "Events",
    ("id", "library", "address", "name", "starting_date", "ending_date", "active"),
    ("ID", "Library", "Address", "Name", "Starting Date", "Ending Date", "Active"),
    get_events,
    "events"
)

# Genre
make_table_tab(
    tab_genre,
    "Genres",
    ("id", "name"),
    ("ID", "Name"),
    get_genres,
    "genres"
)

# Leave
make_table_tab(
    tab_leave,
    "Leaves",
    ("id", "first_name", "last_name", "paid", "cause", "start_date", "end_date"),
    ("ID", "First Name", "Last Name", "Paid", "Cause", "Start Date", "End Date"),
    get_leaves,
    "leaves"
)

# Library
make_table_tab(
    tab_library,
    "Libraries",
    ("id", "name", "address"),
    ("ID", "Name", "Address"),
    get_libraries,
    "libraries"
)

# Position
make_table_tab(
    tab_position,
    "Positions",
    ("id", "name", "available", "salary"),
    ("ID", "Name", "Available", "Salary"),
    get_positions,
    "positions"
)

# Reservation
make_table_tab(
    tab_reservation,
    "Reservations",
    ("id", "username", "library", "address", "book", "author", "release_date"),
    ("ID", "Username", "Library", "Address", "Book", "Author", "Release Date"),
    get_reservations,
    "reservations"
)
#endregion

window.mainloop()
