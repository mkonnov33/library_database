import sqlite3

def connect():
    con = sqlite3.connect("veikals.db")
    cur = con.cursor()
    con.execute("PRAGMA foreign_keys = ON")
    return con, cur

def add_client(name, surname):
    if name == "" or surname == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO klienti (vards, uzvards) VALUES (?, ?)", (name, surname))
    con.commit()
    klienti_id = cur.lastrowid
    con.close()
    return klienti_id

def add_product(name, cena):
    if name == "" or cena == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO preces (nosaukums, cena) VALUES (?, ?)", (name, cena))
    con.commit()
    preces_id = cur.lastrowid
    con.close()
    return preces_id

def add_order(client_id, product_id):
    if client_id == "" or product_id == "":
        return
    con, cur = connect()
    cur.execute("INSERT INTO pasutijumi (klienta_id, preces_id) VALUES (?, ?)", (client_id, product_id))
    con.commit()
    pasutijumi_id = cur.lastrowid
    con.close()
    return pasutijumi_id

def get_products():
    con, cur = connect()
    cur.execute("SELECT preces_id, nosaukums, cena FROM preces")
    products = cur.fetchall()
    con.close()
    return products

def get_clients():
    con, cur = connect()
    cur.execute("SELECT klienti_id, vards, uzvards FROM klienti")
    clients = cur.fetchall()
    con.close()
    return clients

def get_orders():
    con, cur = connect()
    cur.execute('''SELECT
                    pasutijumi.pasutijuma_id,
                    klienti.vards,
                    klienti.uzvards,
                    preces.nosaukums,
                    preces.cena
                   FROM pasutijumi
                   JOIN klienti
                       ON pasutijumi.klienta_id = klienti.klienti_id
                   JOIN preces
                       ON pasutijumi.preces_id = preces.preces_id''')
    orders = cur.fetchall()
    con.close()
    return orders