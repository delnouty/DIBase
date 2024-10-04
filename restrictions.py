import sqlite3
import csv

# Connect to (or create) the database
conn = sqlite3.connect('boutiqueREST.db')
cursor = conn.cursor()

# Create the Clients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        Client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom TEXT NOT NULL,
        Prenom TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Telephone TEXT,
        Date_Naissance DATE,
        Adresse TEXT,
        Consentement_Marketing BOOLEAN NOT NULL CHECK (Consentement_Marketing IN (0, 1))
    )
''')

# Create the Orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        Commande_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_Commande DATE NOT NULL,
        Montant_Commande REAL NOT NULL,
        Client_ID INTEGER NOT NULL,
        FOREIGN KEY (Client_ID) REFERENCES Clients (Client_ID)
    )
''')

# Function to load data into the Clients table from CSV
def load_clients_data():
    with open('jeu-de-donnees-clients.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        clients_data = [
            (
                row['Nom'],
                row['Prénom'],
                row['Email'],
                row['Téléphone'],
                row['Date_Naissance'],
                row['Adresse'],
                int(row['Consentement_Marketing'])
            ) for row in csv_reader
        ]
        cursor.executemany('''
            INSERT INTO Clients (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', clients_data)

# Function to load data into the Orders table from CSV
def load_orders_data():
    with open('jeu-de-donnees-commandes.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        orders_data = [
            (
                row['Date_Commande'],
                float(row['Montant_Commande']),
                int(row['Client_ID'])
            ) for row in csv_reader
        ]
        cursor.executemany('''
            INSERT INTO Orders (Date_Commande, Montant_Commande, Client_ID)
            VALUES (?, ?, ?)
        ''', orders_data)

# Load data into the tables
load_clients_data()
load_orders_data()

# Commit the changes
conn.commit()

# Functions to query the database

# 1. Get clients who have consented to receive marketing communications
def get_clients_with_marketing_consent():
    cursor.execute('''
        SELECT Client_ID, Nom, Prenom, Email
        FROM Clients
        WHERE Consentement_Marketing = 1
    ''')
    return cursor.fetchall()

# 2. Get all orders for a specific client (by Client_ID)
def get_orders_for_client(client_id):
    cursor.execute('''
        SELECT Commande_ID, Date_Commande, Montant_Commande
        FROM Orders
        WHERE Client_ID = ?
    ''', (client_id,))
    return cursor.fetchall()

# 3. Calculate the total amount of orders for client with ID 61
def get_total_amount_for_client_61():
    cursor.execute('''
        SELECT SUM(Montant_Commande)
        FROM Orders
        WHERE Client_ID = 61
    ''')
    result = cursor.fetchone()[0]
    return result if result is not None else 0.0

# 4. Get clients who have placed orders of more than 100 euros
def get_clients_with_orders_over_100():
    cursor.execute('''
        SELECT DISTINCT C.Client_ID, C.Nom, C.Prenom, C.Email
        FROM Clients C
        JOIN Orders O ON C.Client_ID = O.Client_ID
        WHERE O.Montant_Commande > 100
    ''')
    return cursor.fetchall()

# 5. Get clients who have placed orders after 2023-01-01
def get_clients_with_orders_after(date='2023-01-01'):
    cursor.execute('''
        SELECT DISTINCT C.Client_ID, C.Nom, C.Prenom, C.Email
        FROM Clients C
        JOIN Orders O ON C.Client_ID = O.Client_ID
        WHERE O.Date_Commande > ?
    ''', (date,))
    return cursor.fetchall()

# Example calls to the functions

# 1. Clients who have consented to marketing
clients_with_marketing_consent = get_clients_with_marketing_consent()
print("Clients with marketing consent:")
for client in clients_with_marketing_consent:
    print(client)

# 2. Orders for a specific client (e.g., Client_ID = 2)
client_orders = get_orders_for_client(2)
print("\nOrders for client with ID 2:")
for order in client_orders:
    print(order)

# 3. Total amount of orders for client with ID 61
total_amount_client_61 = get_total_amount_for_client_61()
print("\nTotal amount for client with ID 61:", total_amount_client_61)

# 4. Clients with orders over 100 euros
clients_with_large_orders = get_clients_with_orders_over_100()
print("\nClients with orders over 100 euros:")
for client in clients_with_large_orders:
    print(client)

# 5. Clients with orders after 01/01/2023
clients_with_recent_orders = get_clients_with_orders_after('2023-01-01')
print("\nClients with orders after 2023-01-01:")
for client in clients_with_recent_orders:
    print(client)

# Close the connection
conn.close()
