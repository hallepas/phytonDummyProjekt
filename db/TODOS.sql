CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) NOT NULL UNIQUE,
    password VARCHAR(250) NOT NULL
);

CREATE TABLE rezepte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(250) NOT NULL,
    description VARCHAR(250) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE zutaten (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rezept_id INT NOT NULL,
    name VARCHAR(250) NOT NULL,
    number INT,
    einheit VARCHAR(50),
    FOREIGN KEY (rezept_id) REFERENCES rezepte(id)
);

