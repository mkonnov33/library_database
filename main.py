import sqlite3

database = sqlite3.connect("veikals.db")
cursor = database.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS klienti(
        klienti_id INTEGER PRIMARY KEY,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS preces(
        preces_id INTEGER PRIMARY KEY,
        nosaukums TEXT NOT NULL,
        cena REAL NOT NULL)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pasutijumi(
        pasutijuma_id INTEGER PRIMARY KEY,
        klienta_id INTEGER NOT NULL,
        preces_id INTEGER NOT NULL,
                 
        FOREIGN KEY (klienta_id)
            REFERENCES klienti(klienti_id),

        FOREIGN KEY (preces_id)
            REFERENCES preces(preces_id))
""")

cursor.execute("""
INSERT OR IGNORE INTO klienti (klienti_id, vards, uzvards)
    VALUES (1, 'Kirills', 'Alohins')
""")
cursor.execute("""
INSERT OR IGNORE INTO klienti (klienti_id, vards, uzvards)
    VALUES (2, 'Aleksandrs', 'Abbas')
""")
cursor.execute("""
INSERT OR IGNORE INTO klienti (klienti_id, vards, uzvards)
    VALUES (3, 'Tamir', 'Abdarahman')
""")

cursor.execute("""
INSERT INTO preces (preces_id, nosaukums, cena)
    VALUES (1, 'Dators', 2999.99)
""")
cursor.execute("""
INSERT OR IGNORE INTO preces (preces_id, nosaukums, cena)
    VALUES (2, 'RTX videokarta', 999.99)
""")
cursor.execute("""
INSERT OR IGNORE INTO preces (preces_id, nosaukums, cena)
    VALUES (3, 'Ryzen processors', 499.99)
""")

cursor.execute("""
INSERT OR IGNORE INTO pasutijumi (pasutijuma_id, klienta_id, preces_id)
    VALUES (1, 2, 3)
""")
cursor.execute("""
INSERT OR IGNORE INTO pasutijumi (pasutijuma_id, klienta_id, preces_id)
    VALUES (2, 1, 2)
""")
cursor.execute("""
INSERT OR IGNORE INTO pasutijumi (pasutijuma_id, klienta_id, preces_id)
    VALUES (3, 3, 1)
""")

database.commit()
cursor.execute("""
    SELECT
        klienti.vards,
        klienti.uzvards,
        preces.nosaukums,
        preces.cena
    FROM pasutijumi
    JOIN klienti
        ON pasutijumi.klienta_id = klienti.klienti_id
    JOIN preces
        ON pasutijumi.preces_id = preces.preces_id
""")

pasutijumi_saraksts = cursor.fetchall()
print("\nPASUTIJUMI")
for vards, uzvards, nosaukums, cena in pasutijumi_saraksts:
    print(vards, uzvards, nosaukums, cena)
