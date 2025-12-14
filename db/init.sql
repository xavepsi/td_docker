CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT
);

INSERT INTO items (title, description) VALUES
('Tâche 1', 'Faire le TD Docker'),
('Tâche 2', 'Écrire le rapport');
