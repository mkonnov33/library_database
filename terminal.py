from funkcijas import *
from enum import Enum

class States(Enum):
    FUNC_CHOICE = 1,
    ADD_DATA_CHOICE = 2,
    GET_DATA_CHOICE = 3

current_state = States.FUNC_CHOICE

def client_list():
    print("\nKlientu saraksts:")
    for client in get_clients():
        print(client)
def product_list():
    print("\nPreču saraksts:")
    for product in get_products():
        print(product)

while True:
    match current_state:
        case States.FUNC_CHOICE:
            print("\nLibrary")
            print("\n 1. - Add data")
            print("\n 2. - Get data")
            print("\n 0. - Exit")

            choice = input("Choose: ")

            match choice:
                case "1":
                    current_state = States.ADD_DATA_CHOICE
                case "2":
                    current_state = States.GET_DATA_CHOICE
                case "0":
                    break
                case _:
                    print("Choice out of range")
        case States.ADD_DATA_CHOICE:
            print("\nLibrary")
            print("\n 1. - Add account")
            print("\n 2. - Add author")
            print("\n 3. - Add book")
            print("\n 4. - Add employee")
            print("\n 5. - Add event")
            print("\n 6. - Add genre")
            print("\n 7. - Add leave")
            print("\n 8. - Add library")
            print("\n 9. - Add position")
            print("\n 10. - Add reservation")
            print("\n 0. - Exit")

            choice = input("Choose: ")

            match choice:
                case "1":
                    print("\nAdding an account:")
                    username = input("Username*: ")
                    password = input("Password*: ")
                    account_id = add_client(username, password)
                    print("Account added. ID:", account_id)
                case "2":
                    print("\nAdding an author:")
                    first_name = input("First name*: ")
                    last_name = input("Last name*: ")
                    date_of_birth = input("Date of birth: ")
                    author_id = add_client(first_name, last_name, date_of_birth)
                    print("Author added. ID:", author_id)
                case "3":
                    print("\nAdding a book:")
                    name = input("Name*: ")
                    release_date = input("Release date*: ")
                    author_list()
                    author_id = input("Author id*: ")
                    featured_in_event = input("Featured in event?*: ")
                    if (featured_in_event):
                        event_list()
                        event_id = input("Event id: ")
                    else:
                        event_id = None
                    genre_list()
                    genre_id = input("Genre id: ")
                    book_id = add_client(name, release_date, date_of_birth, author_id, featured_in_event, event_id, genre_id)
                    print("Book added. ID:", book_id)
                case "4":
                    client_list()
                case "5":
                    product_list()
                case "6":
                    orders = get_orders()
                    for order in orders:
                        print(order)
                case "0":
                    break
                case _:
                    print("Vecīt, kas par sūdu, paprasīju izvelēties no 1 līdz 6")
            input()

    
    