-- SAISONS 
INSERT INTO saisons (nom)
VALUES ('Printemps'),
    ('Été'),
    ('Automne'),
    ('Hiver'),
    ('Toutes saisons');
-- UNITES
INSERT INTO unites (nom)
VALUES ('g'),
    ('kg'),
    ('mL'),
    ('L'),
    ('cuillère à soupe'),
    ('cuillère à café'),
    ('pincée');
-- INGREDIENTS
INSERT INTO ingredients (nom)
VALUES ('Poulet'),
    ('Boeuf'),
    ('Porc'),
    ('Poisson'),
    ('Oeuf'),
    ('Lait'),
    ('Farine'),
    ('Sucre'),
    ('Sel'),
    ('Poivre'),
    ('Ail'),
    ('Oignon'),
    ('Tomate'),
    ('Coulis de tomates'),
    ('Concentré de tomates'),
    ('Champignon'),
    ('Courgette'),
    ('Aubergine'),
    ('Carotte'),
    ('Pomme de terre'),
    ('Riz'),
    ('Pâtes'),
    ('Fromage'),
    ('Crème fraîche'),
    ('Lardons'),
    ('Pâte brisée'),
    ('Beurre'),
    ('Huile d olive'),
    ('Vinaigre'),
    ('Herbes de Provence'),
    ('Basilic'),
    ('Thym'),
    ('Romarin'),
    ('Curry'),
    ('Paprika'),
    ('Cumin'),
    ('Gingembre'),
    ('Cannelle'),
    ('Clou de girofle'),
    ('Muscade'),
    ('Anis étoilé'),
    ('Fenouil'),
    ('Coriandre'),
    ('Curcuma'),
    ('Piment'),
    ('Safran'),
    ('Vanille'),
    ('Chocolat'),
    ('Fraise'),
    ('Framboise'),
    ('Myrtille'),
    ('Citron'),
    ('Orange'),
    ('Banane'),
    ('Pomme'),
    ('Poire'),
    ('Cerise'),
    ('Abricot'),
    ('Prune'),
    ('Melon'),
    ('Pastèque'),
    ('Kiwi'),
    ('Mangue'),
    ('Ananas'),
    ('Noix de coco'),
    ('Amande'),
    ('Noisette'),
    ('Pistache'),
    ('Cacahuète'),
    ('Noix'),
    ('Châtaigne'),
    ('Lentille'),
    ('Pois chiche'),
    ('Haricot'),
    ('Quinoa'),
    ('Semoule'),
    ('Boulgour'),
    ('Orge'),
    ('Avoine'),
    ('Sarrasin'),
    ('Raisin'),
    ('Miel'),
    ('Sirop d érable'),
    ('Sirop de glucose'),
    ('Levure chimique'),
    ('Bicarbonate de soude'),
    ('Gélatine'),
    ('Poivron'),
    ('Agar-agar');
-- RECETTES
INSERT INTO recettes (
        nom,
        description,
        temps_preparation,
        nombre_repas
    )
VALUES (
        'Poulet rôti',
        'Un poulet entier rôti au four avec des herbes de Provence.',
        60,
        2
    ),
    (
        'Spaghetti bolognaise',
        'Des pâtes spaghetti servies avec une sauce à la viande et aux tomates.',
        25,
        1
    ),
    (
        'Quiche lorraine',
        'Une tarte salée garnie de lardons, d œufs et de crème fraîche.',
        45,
        2
    ),
    (
        'Ratatouille',
        'Un mélange de légumes mijotés à la provençale, comprenant des courgettes, des aubergines, des poivrons et des tomates.',
        30,
        2
    ) (
        'Tarte aux fromages',
        'Une tarte feuilletée avec des fromages fondus dessus.',
        45,
        2
    ),
    (
        'Steak et patates sautées',
        'Une viande de boeuf type steak ou entrecôte avec des pommes de terres sautées à la poëlle.',
        35,
        1
    ),
    (
        'Pizza 4 fromages',
        'Une pizza faite maison avec autant de fromages que disponibles sur une base de sauce tomates.',
        25,
        2
    ),
    (
        'Pates crevettes curry',
        'Un plat à base de pates dans une sauce à la crème fraiche, au curry et avec des crevettes.',
        30,
        1
    ),
    (
        'Ragout de boeuf',
        'Un plat de boeuf en sauce mijoté à feu doux. Servi avec des pommes de terre, des carrotes, un oignon, des olives et des pois chiches qui ont cuit avec la viande',
        180,
        3
    ),
    (
        'Risotto de poulet',
        'Un risotto cuit à feu doux avec des oignons, du poulet et un bouillon de légume. Ajoutez une portion de mozzarella quelques minutes avant la fin de la cuisson pour plus d onctueusité.',
        60,
        3
    ),
    (
        'Tartines de fromage',
        'Un plat très rapide pour une petite faim: prenez du pain et du fromage, avec un morceau de jambon pour partager avec Nala',
        5,
        1
    ),
    (
        'Bol de céréales',
        'Une petite faim le soir et pas envi de cuisiner? Le bol de céréales est là pour vous.',
        5,
        1
    );
-- RECETTE_INGREDIENTS
-- Exemple d'insertion pour la recette "Poulet rôti"
INSERT INTO recette_ingredients (recette_id, ingredient_id, quantite, unite_id)
VALUES (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poulet'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'kg'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Herbes de Provence'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à soupe'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Ail'
        ),
        3,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Oignon'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Huile d olive'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à soupe'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Sel'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poivre'
        ),
        0.5,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Pomme de terre'
        ),
        500,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    );
-- Exemple d'insertion pour la recette "Spaghetti bolognaise"
INSERT INTO recette_ingredients (recette_id, ingredient_id, quantite, unite_id)
VALUES (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Boeuf'
        ),
        250,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Coulis de tomates'
        ),
        400,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Concentré de tomates'
        ),
        120,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Oignon'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Ail'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Huile d olive'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à soupe'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Sel'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poivre'
        ),
        0.5,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Pâtes'
        ),
        300,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    );
-- Exemple d'insertion pour la recette "Quiche lorraine"
INSERT INTO recette_ingredients (recette_id, ingredient_id, quantite, unite_id)
VALUES (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Lardons'
        ),
        150,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Oeuf'
        ),
        3,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Crème fraîche'
        ),
        200,
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Sel'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poivre'
        ),
        0.5,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Pâte brisée'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    );
-- Exemple d'insertion pour la recette "Ratatouille"
INSERT INTO recette_ingredients (recette_id, ingredient_id, quantite, unite_id)
VALUES (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Courgette'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Aubergine'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poivron'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Tomate'
        ),
        3,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Oignon'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Ail'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Huile d olive'
        ),
        2,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à soupe'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Sel'
        ),
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM ingredients
            WHERE nom = 'Poivre'
        ),
        0.5,
        (
            SELECT id
            FROM unites
            WHERE nom = 'cuillère à café'
        )
    );
-- RECETTE_SAISONS
INSERT INTO recette_saisons (recette_id, saison_id)
VALUES (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Poulet rôti'
        ),
        (
            SELECT id
            FROM saisons
            WHERE nom = 'Toutes saisons'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Spaghetti bolognaise'
        ),
        (
            SELECT id
            FROM saisons
            WHERE nom = 'Toutes saisons'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Quiche lorraine'
        ),
        (
            SELECT id
            FROM saisons
            WHERE nom = 'Toutes saisons'
        )
    ),
    (
        (
            SELECT id
            FROM recettes
            WHERE nom = 'Ratatouille'
        ),
        (
            SELECT id
            FROM saisons
            WHERE nom = 'Été'
        )
    );