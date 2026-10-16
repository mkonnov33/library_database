import tkinter as tk
from funkcijas import *

def addClientFromWindow():
    name = name_input.get()
    surname = surname_input.get()
    add_client(name, surname)
    name_input.delete(0, tk.END)
    surname_input.delete(0, tk.END)

def addProdFromWindow():
    prodname = prodname_input.get()
    cena = cena_input.get()
    add_product(prodname, cena)
    prodname_input.delete(0, tk.END)
    cena_input.delete(0, tk.END)

def addOrderFromWindow():
    client_id = client_id_input.get()
    prod_id = product_id_input.get()
    add_order(client_id, prod_id)
    client_id_input.delete(0, tk.END)
    product_id_input.delete(0, tk.END)

window = tk.Tk()
window.title("Lidl datubāze")
window.geometry("1000x600")

label = tk.Label(window, text="Lidl", font=("Arial", 24))
label.pack(pady=20)

#Pievienot klientu
client_block = tk.LabelFrame(
    window,
    text="Pievienot klientu",
    padx=10,
    pady=10
)
client_block.pack(padx=20, pady=20, fill="x")
tk.Label(client_block, text="Vārds").pack()
name_input = tk.Entry(client_block, width=40)
name_input.pack(pady=5)
tk.Label(client_block, text="Uzvārds").pack()
surname_input = tk.Entry(client_block, width=40)
surname_input.pack(pady=5)
result = tk.Label(client_block, text="", fg="green")
result.pack()
client_button = tk.Button(client_block, text="Pievienot", command=addClientFromWindow)
client_button.pack(pady=10)
label.pack(pady=20)

#Pievienot preci
product_block = tk.LabelFrame(
    window,
    text="Pievienot preci",
    padx=10,
    pady=10
)
product_block.pack(padx=20, pady=20, fill="x")
tk.Label(product_block, text="Nosaukums").pack()
prodname_input = tk.Entry(product_block, width=40)
prodname_input.pack(pady=5)
tk.Label(product_block, text="Cena").pack()
cena_input = tk.Entry(product_block, width=40)
cena_input.pack(pady=5)
product_button = tk.Button(product_block, text="Pievienot", command=addProdFromWindow)
product_button.pack(pady=10)
label.pack(pady=20)

#Pievienot pasūtījumu
order_block = tk.LabelFrame(
    window,
    text="Pievienot pasūtījumu",
    padx=10,
    pady=10
)
order_block.pack(padx=20, pady=20, fill="x")
tk.Label(order_block, text="Klienta ID").pack()
client_id_input = tk.Entry(order_block, width=40)
client_id_input.pack(pady=5)
tk.Label(order_block, text="Preces ID").pack()
product_id_input = tk.Entry(order_block, width=40)
product_id_input.pack(pady=5)
order_button = tk.Button(order_block, text="Pievienot", command=addOrderFromWindow)
order_button.pack(pady=10)
label.pack(pady=20)

window.mainloop()