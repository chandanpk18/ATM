# ATM
Atm interpreter python program with MySQL database connection

#Explanation:
Database Configuration:

Set up DATABASE_CONFIG with your MySQL credentials and database details.
Database Connection (connect_db function):

Uses mysql.connector to connect to the MySQL database.
Table Creation (create_table function):

Creates a table in the MySQL database if it does not already exist.
Registration (register function):

Inserts new user data into the atm table in MySQL.
ATM Access (atm function):

Fetches user data from the database and validates the PIN.
ATM Services (function function):

Updates balance for withdrawals and deposits.
Fetches the balance for display.
Main Menu (main_menu function):

Provides options to register, access ATM services, or exit.
