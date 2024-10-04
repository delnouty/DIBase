import sqlite3
import csv

# Connect to (or create) the database
conn = sqlite3.connect('boutique.db')
cursor = conn.cursor()

# Create the Clients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        Client_ID INTEGER PRIMARY KEY,
        Nom TEXT NOT NULL,
        Prenom TEXT NOT NULL,
        Email TEXT NOT NULL,
        Telephone TEXT NOT NULL,
        Date_Naissance TEXT NOT NULL,
        Adresse TEXT NOT NULL,
        Consentement_Marketing BOOLEAN
    )
''')

# Create the Orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        Commande_ID INTEGER PRIMARY KEY,
        Client_ID INTEGER NOT NULL,
        Date_Commande TEXT NOT NULL,
        Montant_Commande REAL NOT NULL,
        FOREIGN KEY (Client_ID) REFERENCES Clients (Client_ID)
    )
''')

# Function to load data into the Clients table from CSV
def load_clients_data():
    with open('jeu-de-donnees-clients.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        clients_data = [(int(row['Client_ID']), row['Nom'], row['Prénom'], row['Email'], row['Téléphone'], row['Date_Naissance'], row['Adresse'], int(row['Consentement_Marketing'])) for row in csv_reader]
        cursor.executemany('''
            INSERT INTO Clients (Client_ID, Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', clients_data)

# Function to load data into the Orders table from CSV
def load_orders_data():
    with open('jeu-de-donnees-commandes.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        orders_data = [(int(row['Commande_ID']), int(row['Client_ID']), row['Date_Commande'], float(row['Montant_Commande'])) for row in csv_reader]
        cursor.executemany('''
            INSERT INTO Orders (Commande_ID, Client_ID, Date_Commande, Montant_Commande)
            VALUES (?, ?, ?, ?)
        ''', orders_data)

# Load data into the tables
load_clients_data()
load_orders_data()

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully into boutique.db")
