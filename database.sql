### sql for database set up process ###


CREATE DATABASE IF NOT EXISTS atm;
USE atm;

CREATE TABLE IF NOT EXISTS users (
    card_number INT PRIMARY KEY,
    pin INT,
    name VARCHAR(255),
    phone_number VARCHAR(10),
    balance DECIMAL(10, 2)
);
