SELECT r.nom AS recette,
    i.nom AS ingredient,
    ri.quantite,
    u.nom AS unite
FROM recettes r
    JOIN recette_ingredients ri ON r.id = ri.recette_id
    JOIN ingredients i ON i.id = ri.ingredient_id
    JOIN unites u ON u.id = ri.unite_id
ORDER BY r.nom;