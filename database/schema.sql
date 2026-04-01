CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE IF NOT EXISTS recettes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    temps_preparation INT,
    nombre_repas INT NOT NULL CHECK (nombre_repas > 0)
);
CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS unites (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS recette_ingredients (
    recette_id UUID NOT NULL REFERENCES recettes(id) ON DELETE CASCADE,
    ingredient_id INT NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    quantite NUMERIC(10, 2) NOT NULL,
    unite_id INT NOT NULL REFERENCES unites(id) ON DELETE CASCADE,
    PRIMARY KEY (recette_id, ingredient_id)
);
CREATE TABLE IF NOT EXISTS saisons (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS recette_saisons (
    recette_id UUID NOT NULL REFERENCES recettes(id) ON DELETE CASCADE,
    saison_id INT NOT NULL REFERENCES saisons(id) ON DELETE CASCADE,
    PRIMARY KEY (recette_id, saison_id)
);