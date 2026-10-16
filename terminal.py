from funcs import *
from funcs import *
from enum import Enum

class States(Enum):
    FUNC_CHOICE = 1,
    ADD_DATA_CHOICE = 2,
    GET_DATA_CHOICE = 3

current_state = States.FUNC_CHOICE

yeses = ["true", "yes", "t", "y", "+", "sure", "yeah", "ye", "yup"]

while True:
    match current_state:
        case States.FUNC_CHOICE:
            print("\nLibrary")
            print("\n 1. - Add data")
            print("\n 2. - Get data")
            print("\n 0. - Exit")

            choice = input("\nChoose: ")

            match choice:
                case "1":
                    current_state = States.ADD_DATA_CHOICE
                case "2":
                    current_state = States.GET_DATA_CHOICE
                case "0":
                    break
                case _:
                    print("Choice out of range")
        #region ADD_DATA_CHOICE
        case States.ADD_DATA_CHOICE:
            print("\nLibrary")
            print("\n 1. - Add an account")
            print("\n 2. - Add an author")
            print("\n 3. - Add a book")
            print("\n 4. - Add an employee")
            print("\n 5. - Add an event")
            print("\n 6. - Add a genre")
            print("\n 7. - Add a leave")
            print("\n 8. - Add a library")
            print("\n 9. - Add a position")
            print("\n 10. - Add a reservation")
            print("\n 0. - Back")
            print("\n 1. - Add an account")
            print("\n 2. - Add an author")
            print("\n 3. - Add a book")
            print("\n 4. - Add an employee")
            print("\n 5. - Add an event")
            print("\n 6. - Add a genre")
            print("\n 7. - Add a leave")
            print("\n 8. - Add a library")
            print("\n 9. - Add a position")
            print("\n 10. - Add a reservation")
            print("\n 0. - Back")

            choice = input("\nChoose: ")

            match choice:
                case "1":
                    print("\nAdding an account:")
                    username = input("Username*: ")
                    password = input("Password*: ")
                    employee = bool(input("Employee?: "))
                    print(employee)
                    account_id = add_account(username, password, employee)
                    print("Account added. ID:", account_id)
                case "2":
                    print("\nAdding an author:")
                    first_name = input("First name*: ")
                    last_name = input("Last name*: ")
                    date_of_birth = input("Date of birth: ")
                    author_id = add_author(first_name, last_name, date_of_birth)
                    author_id = add_author(first_name, last_name, date_of_birth)
                    print("Author added. ID:", author_id)
                case "3":
                    print("\nAdding a book:")
                    name = input("Name*: ")
                    release_date = input("Release date*: ")
                    author_list()
                    author_id = input("Author ID*: ")
                    author_id = input("Author ID*: ")
                    featured_in_event = input("Featured in event?*: ")
                    if (featured_in_event.lower() in yeses):
                        if (get_events() != []):
                            event_list()
                            event_id = input("Event ID: ")
                        else:
                            event_id = None
                    else:
                        featured_in_event = False
                        event_id = None
                    if (get_genres() != []):
                        genre_list()
                        genre_id = input("Genre ID: ")
                    else:
                        genre_id = None
                    book_id = add_book(name, release_date, author_id, featured_in_event, event_id, genre_id)
                    print("Book added. ID:", book_id)
                case "4":
                    print("\nAdding an employee:")
                    first_name = input("First name*: ")
                    last_name = input("Last name*: ")
                    age = input("Age: ")
                    if (get_libraries() != []):
                        library_list()
                        library_id = input("Library ID*: ")
                    else:
                        library_id = None
                    if (get_accounts() != []):
                        account_list()
                        account_id = input("Account ID*: ")
                    else:
                        account_id = None
                    if (get_positions() != []):
                        position_list()
                        position_id = input("Position ID*: ")
                    else:
                        position_id = None
                    employee_id = add_employee(first_name, last_name, age, library_id, account_id, position_id)
                    print("Employee added. ID:", employee_id)
                case "5":
                    print("\nAdding an event:")
                    name = input("Name*: ")
                    if (get_libraries() != []):
                        library_list()
                        library_id = input("Library ID*: ")
                    else:
                        library_id = None
                    starting_date = input("Starting date*: ")
                    ending_date = input("Ending date*: ")
                    active = input("Active*: ")
                    event_id = add_event(name, library_id, starting_date, ending_date, active)
                    print("Event added. ID:", event_id)
                case "6":
                    print("\nAdding a genre:")
                    name = input("Name*: ")
                    description = input("Description: ")
                    genre_id = add_genre(name, description)
                    print("Genre added. ID:", genre_id)
                case "7":
                    print("\nAdding a leave:")
                    if (get_employees() != []):
                        employee_list()
                        employee_id = input("Employee ID*: ")
                    else:
                        employee_id = None
                    paid = input("Paid?*: ")
                    cause = input("Cause*: ")
                    starting_date = input("Starting date*: ")
                    ending_date = input("Ending date*: ")
                    leave_id = add_leave(employee_id, paid, cause, starting_date, ending_date)
                    print("Leave added. ID:", leave_id)
                case "8":
                    print("\nAdding a library:")
                    name = input("Name*: ")
                    address = input("Adress*: ")
                    library_id = add_library(name, address)
                    print("Leave added. ID:", leave_id)
                case "9":
                    print("\nAdding a position:")
                    name = input("Name*: ")
                    available = input("Available?*: ")
                    salary = input("Salary: ")
                    position_id = add_position(name, available, salary)
                    print("Position added. ID:", position_id)
                case "10":
                    print("\nAdding a reservation:")
                    if (get_books() != []):
                        book_list()
                        book_id = input("Book ID*: ")
                    else:
                        book_id = None
                    if (get_accounts() != []):
                        account_list()
                        account_id = input("Account ID*: ")
                    else:
                        account_id = None
                    if (get_libraries() != []):
                        library_list()
                        library_id= input("Library ID*: ")
                    else:
                        library_id = None
                    reservation_id = add_reservation(book_id, account_id, library_id)
                    print("Reservation added. ID:", reservation_id)
                case "0":
                    current_state = States.FUNC_CHOICE
                    continue
                    current_state = States.FUNC_CHOICE
                    continue
                case _:
                    print("Choice out of range")
            input()
        #endregion
        
        #region GET_DATA_CHOICE
        case States.GET_DATA_CHOICE:
            print("\nLibrary")
            print("\n 1. - Get accounts")
            print("\n 2. - Get authors")
            print("\n 3. - Get books")
            print("\n 4. - Get employees")
            print("\n 5. - Get events")
            print("\n 6. - Get genres")
            print("\n 7. - Get leaves")
            print("\n 8. - Get libraries")
            print("\n 9. - Get positions")
            print("\n 10. - Get reservations")
            print("\n 0. - Back")
            
            choice = input("\nChoose: ")
            
            match choice:
                case "1":
                    print("\n")
                    account_list()
                case "2":
                    print("\n")
                    author_list()
                case "3":
                    print("\n")
                    book_list()
                case "4":
                    print("\n")
                    employee_list()
                case "5":
                    print("\n")
                    event_list()
                case "6":
                    print("\n")
                    genre_list()
                case "7":
                    print("\n")
                    leave_list()
                case "8":
                    print("\n")
                    library_list()
                case "9":
                    print("\n")
                    position_list()
                case "10":
                    print("\n")
                    reservation_list()
                case "0":
                    current_state = States.FUNC_CHOICE
                    continue
                case _:
                    print("Choice out of range")
            input()
        #endregion

    
    