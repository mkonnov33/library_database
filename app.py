# PLACEHOLDER FOR FUTURE REFERENCE

import tkinter as tk
import sqlite3
from datetime import date
from tkinter import messagebox, ttk
from funcs import (
    ACTIVE_DATE_RANGES,
    BOOLEAN_FIELDS,
    DATE_FIELDS,
    delete_row,
    get_accounts,
    get_authors,
    get_books,
    get_edit_fields,
    get_employees,
    get_events,
    get_genres,
    get_leaves,
    get_libraries,
    get_positions,
    get_reservations,
    get_row_by_id,
    insert_row,
    normalize_boolean,
    normalize_date,
    parse_date,
    update_row,
)

#region Setup
window = tk.Tk()
window.title("Library database manager")
window.geometry("1100x700")
window.minsize(760, 520)

background = "#e9dcc2"
paper = "#fffaf0"
paper_edge = "#d4c29f"
foreground = "#493a29"
muted = "#806d54"
accent = "#9c6b2f"
window.configure(bg=background)

style = ttk.Style(window)
style.theme_use("clam")
style.configure("TFrame", background=background)
style.configure("Paper.TFrame", background=paper)
style.configure("TLabel", background=background, foreground=foreground, font=("Segoe UI", 10))
style.configure("Paper.TLabel", background=paper, foreground=foreground, font=("Segoe UI", 10))
style.configure("Subtitle.TLabel", foreground=muted, font=("Segoe UI", 10))
style.configure("TLabelframe", background=paper, bordercolor=paper_edge, relief="solid")
style.configure(
    "TLabelframe.Label",
    background=paper,
    foreground=foreground,
    font=("Segoe UI", 10, "bold"),
)
style.configure(
    "TButton",
    background="#ead9b9",
    foreground=foreground,
    padding=(12, 7),
    font=("Segoe UI", 9, "bold"),
)
style.map("TButton", background=[("active", "#ddc59b")])
style.configure(
    "Accent.TButton",
    background="#8b5e2a",
    foreground="#ffffff",
)
style.map("Accent.TButton", background=[("active", "#70491f")])
style.configure("Danger.TButton", background="#a64536", foreground="#ffffff")
style.map("Danger.TButton", background=[("active", "#84382d")])
style.configure("TNotebook", background=background, borderwidth=0, tabmargins=(4, 6, 4, 0))
style.configure(
    "TNotebook.Tab",
    background="#d3b783",
    foreground=muted,
    padding=(13, 9),
    font=("Segoe UI", 9, "bold"),
)
style.map(
    "TNotebook.Tab",
    background=[("selected", paper), ("active", "#e4cca1")],
    foreground=[("selected", foreground)],
)
style.configure(
    "Treeview",
    background=paper,
    fieldbackground=paper,
    foreground=foreground,
    rowheight=28,
    font=("Segoe UI", 9),
)
style.configure(
    "Treeview.Heading",
    background="#eee1c8",
    foreground=foreground,
    padding=(8, 7),
    font=("Segoe UI", 9, "bold"),
)
style.map("Treeview", background=[("selected", accent)], foreground=[("selected", "#ffffff")])

header = ttk.Frame(window, padding=(22, 16, 22, 10))
header.pack(fill="x")
ttk.Label(header, text="Library", font=("Segoe UI", 25, "bold")).pack(anchor="w")
ttk.Label(
    header,
    text="Manage books, members, staff, and library operations.",
    style="Subtitle.TLabel",
).pack(anchor="w", pady=(2, 0))

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

tabControl.pack(expand=1, fill="both", padx=18, pady=(0, 18))
#endregion

#region Get UI
# --- Tables + forms for each tab ---
def make_table_tab(tab, title, columns, headings, data_func, edit_table):
    """Build a responsive form and searchable data table for one entity."""
    fields = get_edit_fields(edit_table)

    #region Form
    form_block = ttk.LabelFrame(
        tab,
        text=f"Add a {edit_table[:-1]}",
        padding=(14, 12),
    )
    form_block.pack(padx=12, pady=(12, 10), fill="x")

    inputs = []
    input_widgets = {}
    field_frame = ttk.Frame(form_block, style="Paper.TFrame")
    field_frame.pack(fill="x")
    field_blocks = []
    current_columns = [0]
    for column, field_label in fields:
        field_block = ttk.Frame(field_frame, style="Paper.TFrame")
        if edit_table == "accounts" and column == "password":
            field_label = "Password (hidden; leave blank to keep current when editing)"
        ttk.Label(field_block, text=field_label, style="Paper.TLabel").pack(anchor="w", pady=(0, 4))
        if column in BOOLEAN_FIELDS.get(edit_table, set()):
            entry = ttk.Combobox(
                field_block,
                width=21,
                state="readonly",
                values=("", "Yes", "No"),
            )
        elif column == "password":
            entry = ttk.Entry(field_block, width=24, show="*")
        else:
            entry = ttk.Entry(field_block, width=24)
        entry.pack(fill="x")
        inputs.append((column, entry))
        input_widgets[column] = entry
        field_blocks.append(field_block)

    active_label = None
    active_range = ACTIVE_DATE_RANGES.get(edit_table)
    if active_range:
        active_block = ttk.Frame(field_frame, style="Paper.TFrame")
        active_label = ttk.Label(active_block, text="Enter a valid date range", style="Paper.TLabel")
        active_label.pack(anchor="w", fill="x", pady=6)
        field_blocks.append(active_block)

    def arrange_fields(event):
        column_count = max(1, min(3, event.width // 280))
        if column_count == current_columns[0]:
            return
        current_columns[0] = column_count
        for field_block in field_blocks:
            field_block.grid_forget()
        for column in range(3):
            field_frame.columnconfigure(column, weight=0, uniform="")
        for column in range(column_count):
            field_frame.columnconfigure(column, weight=1, uniform="form")
        for index, field_block in enumerate(field_blocks):
            field_block.grid(
                row=index // column_count,
                column=index % column_count,
                sticky="ew",
                padx=(0, 14),
                pady=(0, 10),
            )

    field_frame.bind("<Configure>", arrange_fields)

    editing_id = [None]

    def update_active_display(event=None):
        if not active_range or active_label is None:
            return
        if event is not None and event.widget not in input_widgets.values():
            return
        start_value = input_widgets[active_range[0]].get()
        end_value = input_widgets[active_range[1]].get()
        try:
            start = parse_date(start_value)
            end = parse_date(end_value)
        except (TypeError, ValueError):
            active_label.configure(text="Enter a valid date range")
            return
        if start is None or end is None:
            active_label.configure(text="Enter a valid date range")
            return
        active_label.configure(
            text="Active today" if start <= date.today() <= end else "Not active today"
        )

    def normalize_date_input(event):
        entry = event.widget
        value = entry.get()
        if value.strip():
            try:
                normalized = normalize_date(value)
            except ValueError:
                update_active_display()
                return
            if normalized != value:
                entry.delete(0, tk.END)
                entry.insert(0, normalized)
        update_active_display()

    for column, entry in inputs:
        if column in DATE_FIELDS.get(edit_table, set()):
            entry.bind("<FocusOut>", normalize_date_input)
            entry.bind("<KeyRelease>", update_active_display)

    def set_editing_label():
        if editing_id[0] is None:
            form_block.configure(text=f"Add a {edit_table[:-1]}")
            save_button.configure(text="Add")
        else:
            form_block.configure(text=f"Editing {edit_table[:-1]} (ID {editing_id[0]})")
            save_button.configure(text="Update")

    def clear_form():
        editing_id[0] = None
        for entry in input_widgets.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
        if tree.selection():
            tree.selection_remove(tree.selection())
        set_editing_label()
        update_active_display()

    def add_from_form():
        try:
            values = {}
            for column, entry in inputs:
                value = entry.get()
                if column in DATE_FIELDS.get(edit_table, set()) and value.strip():
                    value = normalize_date(value)
                    entry.delete(0, tk.END)
                    entry.insert(0, value)
                values[column] = value
            if editing_id[0] is None:
                if insert_row(edit_table, values) is None:
                    messagebox.showerror(
                        "Missing required fields",
                        "Fill in all required fields before adding this record.",
                        parent=window,
                    )
                    return
            else:
                if not update_row(edit_table, editing_id[0], values):
                    messagebox.showerror(
                        "Update failed",
                        "The selected record no longer exists.",
                        parent=window,
                    )
                    return
        except ValueError as error:
            messagebox.showerror("Invalid value", str(error), parent=window)
            return
        except sqlite3.Error as error:
            messagebox.showerror("Save failed", f"The record could not be saved:\n{error}", parent=window)
            return
        clear_form()
        refresh()

    def load_selected(*_):
        selected = tree.selection()
        if not selected:
            return
        row = tree.item(selected[0], "values")
        row_id = row[0]
        current = get_row_by_id(edit_table, row_id)
        if current is None:
            return
        current_values = current
        editing_id[0] = row_id
        for column, entry in inputs:
            value = current_values[column]
            if column == "password":
                entry.delete(0, tk.END)
            elif column in BOOLEAN_FIELDS.get(edit_table, set()):
                entry.set("" if value is None else ("Yes" if normalize_boolean(value) else "No"))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, "" if value is None else str(value))
        update_active_display()
        set_editing_label()

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Select a record", "Choose a record in the table before deleting it.", parent=window)
            return
        row = tree.item(selected[0], "values")
        row_id = row[0]
        if not messagebox.askyesno(
            "Delete record",
            f"Delete this {edit_table[:-1]} (ID {row_id})? This cannot be undone.",
            parent=window,
        ):
            return
        try:
            deleted = delete_row(edit_table, row_id)
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Record is in use",
                "This record is referenced by other records. Delete those related records first.",
                parent=window,
            )
            return
        except sqlite3.Error as error:
            messagebox.showerror("Delete failed", f"The record could not be deleted:\n{error}", parent=window)
            return
        if not deleted:
            messagebox.showerror("Delete failed", "The selected record no longer exists.", parent=window)
            return
        clear_form()
        refresh()

    #region Buttons
    button_bar = ttk.Frame(form_block, style="Paper.TFrame")
    button_bar.pack(fill="x", pady=(2, 0))
    save_button = ttk.Button(button_bar, text="Add", style="Accent.TButton", command=add_from_form)
    save_button.pack(side="left", padx=(0, 7))
    clear_button_form = ttk.Button(button_bar, text="Clear", command=clear_form)
    clear_button_form.pack(side="left")
    delete_button = ttk.Button(button_bar, text="Delete Selected", style="Danger.TButton", command=delete_selected)
    delete_button.pack(side="right")
    #endregion
    #endregion

    #region Table
    table_block = ttk.LabelFrame(
        tab,
        text=title,
        padding=(12, 10),
    )
    table_block.pack(padx=12, pady=(0, 12), fill="both", expand=True)

    rows = []

    def refresh():
        tree.delete(*tree.get_children())
        rows.clear()
        rows.extend(data_func())
        apply_filter()

    def apply_filter(*_):
        query = search_input.get().lower()
        tree.delete(*tree.get_children())
        for index, row in enumerate(rows):
            if query in " ".join(str(value) for value in row).lower():
                tree.insert(
                    "",
                    "end",
                    values=row,
                    tags=("even" if index % 2 == 0 else "odd",),
                )

    search_bar = ttk.Frame(table_block, style="Paper.TFrame")
    search_bar.pack(side="top", pady=(0, 10), fill="x")
    ttk.Label(search_bar, text="Search").pack(side="left", padx=(0, 8))
    search_input = ttk.Entry(search_bar, width=32)
    search_input.pack(side="left", padx=(0, 8), fill="x", expand=True)
    search_input.bind("<KeyRelease>", apply_filter)
    clear_button = ttk.Button(
        search_bar,
        text="Clear",
        command=lambda: (search_input.delete(0, tk.END), apply_filter()),
    )
    clear_button.pack(side="left")
    refresh_button = ttk.Button(search_bar, text="Refresh", command=refresh)
    refresh_button.pack(side="left", padx=(8, 0))

    table_content = ttk.Frame(table_block, style="Paper.TFrame")
    table_content.pack(fill="both", expand=True)
    table_content.rowconfigure(0, weight=1)
    table_content.columnconfigure(0, weight=1)

    tree = ttk.Treeview(table_content, columns=columns, show="headings")
    tree.tag_configure("even", background=paper)
    tree.tag_configure("odd", background="#f8f0e2")

    for column, heading in zip(columns, headings):
        tree.heading(column, text=heading)
        tree.column(column, width=140, minwidth=90, anchor="w", stretch=True)

    vertical_scrollbar = ttk.Scrollbar(table_content, orient="vertical", command=tree.yview)
    horizontal_scrollbar = ttk.Scrollbar(table_content, orient="horizontal", command=tree.xview)
    tree.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    tree.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    tree.bind("<<TreeviewSelect>>", load_selected)
    #endregion

    refresh()

# Account
make_table_tab(
    tab_account,
    "Accounts",
    ("id", "username", "password", "employee"),
    ("ID", "Username", "Password (hidden)", "Employee?"),
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
    ("id", "name", "description"),
    ("ID", "Name", "Description"),
    get_genres,
    "genres"
)

# Leave
make_table_tab(
    tab_leave,
    "Leaves",
    ("id", "first_name", "last_name", "paid", "cause", "start_date", "end_date", "active"),
    ("ID", "First Name", "Last Name", "Paid", "Cause", "Start Date", "End Date", "Active"),
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
