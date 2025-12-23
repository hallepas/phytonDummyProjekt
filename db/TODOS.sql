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

-- Sample recipes (assuming user_id 1 exists)
INSERT INTO rezepte (user_id, name, description) VALUES
(1, 'Spaghetti Bolognese', 'Klassische italienische Pasta mit Hackfleischsauce'),
(1, 'Hähnchen-Curry', 'Cremiges indisches Curry mit zartem Hähnchenfleisch'),
(1, 'Caesar Salad', 'Frischer Salat mit Parmesan und knusprigen Croutons'),
(1, 'Tomatensuppe', 'Cremige Suppe aus frischen Tomaten'),
(1, 'Pfannkuchen', 'Fluffige amerikanische Pancakes zum Frühstück'),
(1, 'Guacamole', 'Mexikanischer Avocado-Dip'),
(1, 'Rührei', 'Einfaches Frühstück mit Eiern');

-- Ingredients for Spaghetti Bolognese (rezept_id 1)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(1, 'Spaghetti', 500, 'g'),
(1, 'Hackfleisch', 400, 'g'),
(1, 'Tomaten', 800, 'g'),
(1, 'Zwiebeln', 2, 'Stück'),
(1, 'Knoblauch', 3, 'Zehen'),
(1, 'Olivenöl', 3, 'EL'),
(1, 'Salz', NULL, NULL),
(1, 'Pfeffer', NULL, NULL);

-- Ingredients for Hähnchen-Curry (rezept_id 2)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(2, 'Hähnchenbrustfilet', 600, 'g'),
(2, 'Kokosmilch', 400, 'ml'),
(2, 'Currypaste', 2, 'EL'),
(2, 'Zwiebeln', 1, 'Stück'),
(2, 'Paprika', 1, 'Stück'),
(2, 'Reis', 300, 'g'),
(2, 'Ingwer', 1, 'Stück'),
(2, 'Koriander', NULL, NULL);

-- Ingredients for Caesar Salad (rezept_id 3)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(3, 'Römersalat', 1, 'Stück'),
(3, 'Parmesan', 80, 'g'),
(3, 'Croutons', 100, 'g'),
(3, 'Hähnchenbrustfilet', 300, 'g'),
(3, 'Caesar Dressing', 100, 'ml'),
(3, 'Zitrone', 1, 'Stück');

-- Ingredients for Tomatensuppe (rezept_id 4)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(4, 'Tomaten', 1000, 'g'),
(4, 'Zwiebeln', 1, 'Stück'),
(4, 'Knoblauch', 2, 'Zehen'),
(4, 'Gemüsebrühe', 500, 'ml'),
(4, 'Sahne', 100, 'ml'),
(4, 'Basilikum', NULL, NULL);

-- Ingredients for Pfannkuchen (rezept_id 5)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(5, 'Mehl', 300, 'g'),
(5, 'Milch', 400, 'ml'),
(5, 'Eier', 3, 'Stück'),
(5, 'Zucker', 2, 'EL'),
(5, 'Backpulver', 1, 'TL'),
(5, 'Butter', 50, 'g');

-- Ingredients for Guacamole (rezept_id 6)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(6, 'Avocado', 3, 'Stück'),
(6, 'Tomaten', 2, 'Stück'),
(6, 'Zwiebeln', 1, 'Stück'),
(6, 'Limette', 1, 'Stück'),
(6, 'Koriander', NULL, NULL),
(6, 'Salz', NULL, NULL);

-- Ingredients for Rührei (rezept_id 7)
INSERT INTO zutaten (rezept_id, name, number, einheit) VALUES
(7, 'Eier', 4, 'Stück'),
(7, 'Milch', 50, 'ml'),
(7, 'Butter', 20, 'g'),
(7, 'Salz', NULL, NULL),
(7, 'Pfeffer', NULL, NULL);

