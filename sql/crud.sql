-- Select the database
USE etudiants;

-- Drop old table if it exists, to make the script repeatable
DROP TABLE IF EXISTS etudiants;

-- Create table
CREATE TABLE etudiants (
    id INT PRIMARY KEY,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    age INT,
    filiere VARCHAR(100)
);

-- CREATE: insert students
INSERT INTO etudiants (id, nom, prenom, age, filiere)
VALUES
(1, 'Cheikh', 'Ahmed', 22, 'Informatique'),
(2, 'Mohamed', 'Sara', 21, 'Cloud Computing'),
(3, 'Ali', 'Youssef', 23, 'Marketing');

-- READ: display all students
SELECT * FROM etudiants;

-- UPDATE: modify one student
UPDATE etudiants
SET age = 23
WHERE id = 1;

-- READ after update
SELECT * FROM etudiants;

-- DELETE: remove one student
DELETE FROM etudiants
WHERE id = 2;

-- FINAL READ
SELECT * FROM etudiants;