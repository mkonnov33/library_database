from funkcijas import *

def client_list():
    print("\nKlientu saraksts:")
    for client in get_clients():
        print(client)
def product_list():
    print("\nPreču saraksts:")
    for product in get_products():
        print(product)

while True:
    print("\nLidl")
    print("\n 1. - Pievienot klientu")
    print("\n 2. - Pievienot preci")
    print("\n 3. - Pievienot pasūtījumu")
    print("\n 4. - Parādīt klientus")
    print("\n 4. - Parādīt preces")
    print("\n 6. - Parādīt pasūtījumu")
    print("\n 0. - Iziet")

    choice = input("Izvēle: ")

    match choice:
        case "1":
            name = input("Klienta vārds: ")
            surname = input("Klienta uzvārds: ")
            client_id = add_client(name, surname)
            print("Klients pievienots. ID:", client_id)
        case "2":
            name = input("Preces nosaukums: ")
            cena = input("Preces cena: ")
            product_id = add_product(name, cena)
            print("Prece pievienota. ID:", product_id)
        case "3":
            client_list()
            client_id = input("Klienta ID: ")
            product_list()
            product_id = input("Preces ID: ")
            order_id = add_order(client_id, product_id)
            print("Pasūtījums pievienots. ID:", order_id)
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
    