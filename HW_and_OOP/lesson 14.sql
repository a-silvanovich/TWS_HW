create database lesson14;
use lesson14;
CREATE TABLE Users (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);
CREATE TABLE seller (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(50) NOT NULL,
    phone INTEGER NOT NULL
);
CREATE TABLE products (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cost INTEGER NOT NULL,
    count INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    FOREIGN KEY (seller_id)
        REFERENCES seller (id)
);
CREATE TABLE orders (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    count INTEGER NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES Users (id),
    FOREIGN KEY (product_id)
        REFERENCES products (id)
);


-- drop table Users, seller, products, orders;