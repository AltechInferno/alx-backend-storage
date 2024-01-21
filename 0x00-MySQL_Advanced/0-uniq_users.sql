-- This SQL script creates the 'users' table with 'id', 'email' and 'name' columns, where 'id' is the primary key & AI,
-- 'email' is unique and not null, 'name' is not null.

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
