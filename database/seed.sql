-- SAISONS 
INSERT INTO saisons (nom)
VALUES ('Printemps'),
    ('Été'),
    ('Automne'),
    ('Hiver'),
    ('Toutes saisons');
-- UNITES
INSERT INTO unites (nom)
VALUES ('mg'),
    ('g'),
    ('kg'),
    ('mL'),
    ('cL'),
    ('L'),
    ('tablespoon'),
    ('teaspoon'),
    ('bunch'),
    ('pack'),
    ('unit');
-- INGREDIENTS
INSERT INTO ingredients (nom, unite_standard_id)
VALUES (
        'Poulet',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Boeuf',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Porc',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Poisson',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Oeuf',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Lait',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Farine',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Sucre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Sel',
        (
            SELECT id
            FROM unites
            WHERE nom = 'bunch'
        )
    ),
    (
        'Poivre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'bunch'
        )
    ),
    (
        'Ail',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Oignon',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Tomate',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Coulis de tomates',
        (
            SELECT id
            FROM unites
            WHERE nom = 'pack'
        )
    ),
    (
        'Concentré de tomates',
        (
            SELECT id
            FROM unites
            WHERE nom = 'pack'
        )
    ),
    (
        'Champignon',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Courgette',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Aubergine',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Carotte',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pomme de terre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Riz',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pâtes',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Fromage',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Crème fraîche',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Lardons',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pâte brisée',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Beurre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Huile d olive',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Vinaigre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Herbes de Provence',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Basilic',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Thym',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Romarin',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Curry',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Paprika',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Cumin',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Gingembre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Cannelle',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Clou de girofle',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Muscade',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Anis étoilé',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Fenouil',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Coriandre',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Curcuma',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Piment',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Safran',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Vanille',
        (
            SELECT id
            FROM unites
            WHERE nom = 'teaspoon'
        )
    ),
    (
        'Chocolat',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Fraise',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Framboise',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Myrtille',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Citron',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Orange',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Banane',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Pomme',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Poire',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Cerise',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Abricot',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Prune',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Melon',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Pastèque',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Kiwi',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Mangue',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Ananas',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    ),
    (
        'Noix de coco',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Amande',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Noisette',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pistache',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Cacahuète',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Noix',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Châtaigne',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Lentille',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pois chiche',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Haricot',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Quinoa',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Semoule',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Boulgour',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Orge',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Avoine',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Sarrasin',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Raisin',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Miel',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Sirop d érable',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Sirop de glucose',
        (
            SELECT id
            FROM unites
            WHERE nom = 'mL'
        )
    ),
    (
        'Levure chimique',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Bicarbonate de soude',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Gélatine',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Poivron',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Agar-agar',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Crevettes',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Olives',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Mozzarella',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Pain',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Jambon',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Céréales',
        (
            SELECT id
            FROM unites
            WHERE nom = 'g'
        )
    ),
    (
        'Bouillon de légumes',
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
        )
    );
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
    ),
    (
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
            WHERE nom = 'tablespoon'
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
            WHERE nom = 'unit'
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
            WHERE nom = 'tablespoon'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'pack'
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
            WHERE nom = 'pack'
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
        1,
        (
            SELECT id
            FROM unites
            WHERE nom = 'unit'
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
            WHERE nom = 'tablespoon'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'unit'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'unit'
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
            WHERE nom = 'unit'
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
            WHERE nom = 'tablespoon'
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
            WHERE nom = 'bunch'
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
            WHERE nom = 'bunch'
        )
    );
-- Associations des huit recettes restantes.
INSERT INTO recette_ingredients (recette_id, ingredient_id, quantite, unite_id)
SELECT recettes.id,
    ingredients.id,
    associations.quantite,
    unites.id
FROM (
        VALUES ('Tarte aux fromages', 'Fromage', 250, 'g'),
            ('Tarte aux fromages', 'Pâte brisée', 1, 'unit'),
            ('Tarte aux fromages', 'Crème fraîche', 100, 'mL'),
            ('Steak et patates sautées', 'Boeuf', 250, 'g'),
            (
                'Steak et patates sautées',
                'Pomme de terre',
                400,
                'g'
            ),
            ('Steak et patates sautées', 'Beurre', 20, 'g'),
            ('Pizza 4 fromages', 'Fromage', 300, 'g'),
            ('Pizza 4 fromages', 'Farine', 300, 'g'),
            (
                'Pizza 4 fromages',
                'Coulis de tomates',
                1,
                'pack'
            ),
            (
                'Pizza 4 fromages',
                'Huile d olive',
                1,
                'tablespoon'
            ),
            ('Pates crevettes curry', 'Pâtes', 250, 'g'),
            ('Pates crevettes curry', 'Crevettes', 200, 'g'),
            (
                'Pates crevettes curry',
                'Crème fraîche',
                150,
                'mL'
            ),
            ('Pates crevettes curry', 'Curry', 2, 'teaspoon'),
            ('Ragout de boeuf', 'Boeuf', 500, 'g'),
            ('Ragout de boeuf', 'Pomme de terre', 500, 'g'),
            ('Ragout de boeuf', 'Carotte', 300, 'g'),
            ('Ragout de boeuf', 'Oignon', 150, 'g'),
            ('Ragout de boeuf', 'Olives', 100, 'g'),
            ('Ragout de boeuf', 'Pois chiche', 200, 'g'),
            ('Risotto de poulet', 'Riz', 300, 'g'),
            ('Risotto de poulet', 'Poulet', 300, 'g'),
            ('Risotto de poulet', 'Oignon', 100, 'g'),
            (
                'Risotto de poulet',
                'Bouillon de légumes',
                1,
                'unit'
            ),
            ('Risotto de poulet', 'Mozzarella', 125, 'g'),
            ('Tartines de fromage', 'Pain', 200, 'g'),
            ('Tartines de fromage', 'Fromage', 100, 'g'),
            ('Tartines de fromage', 'Jambon', 100, 'g'),
            ('Bol de céréales', 'Céréales', 100, 'g'),
            ('Bol de céréales', 'Lait', 250, 'mL')
    ) AS associations(recette, ingredient, quantite, unite)
    JOIN recettes ON recettes.nom = associations.recette
    JOIN ingredients ON ingredients.nom = associations.ingredient
    JOIN unites ON unites.nom = associations.unite;
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