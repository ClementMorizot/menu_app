# Menu Generator: Living Technical Reference

This document describes the application as implemented in the repository on 22 September 2026. The repository is the source of truth when this document becomes stale. The v0.1 technical memoir is a historical archive, not a specification for the current code.

The terms used throughout are deliberate:

- **Code guarantee** means a property follows from the current implementation under its stated preconditions.
- **Tested behavior** means an automated test exercises a particular path. A passing test does not establish the property for every possible state or failure.
- **Known limitation or debt** means the implementation has a narrower contract than an architectural intention or has a deliberate simplification. It is not a claim that a future design has already been built.

## 1. System scope and entry point

Menu Generator is a Python CLI application backed by PostgreSQL. It builds a menu for 14 meal slots from stored recipes, supports rerolling a selected meal block, manages recipes and ingredients, lets the user exclude recipes, and produces a shopping list. A recipe can cover more than one slot. The `frontend/` files are empty; there is no operational web interface.

Run the application from the repository root with `python -m backend.main`. Imports use the `backend.*` package path. `backend/main.py` is the composition root: it creates repositories and domain services, shares the exclusion objects between their consumers, creates the application services, and starts `backend/ui/cli.py`. It catches uncaught exceptions at the outermost level and closes its session-long database connection in `finally`.

The code is organized into four layers inspired by DDD:

| Layer | Responsibility and boundary |
| --- | --- |
| `backend/domain/` | Owns the menu model, generation and editing rules, availability filtering, quantities and unit conversion, shopping-list calculation, and repository protocols. It does not import SQL or UI modules. |
| `backend/application/` | Coordinates menu and shopping-list use cases, defines the weekly slot sequence and result objects, and controls transactions for CRUD services through a `UnitOfWork` protocol. |
| `backend/infrastructure/` | Implements the repository protocols and Unit of Work against PostgreSQL through psycopg. SQL names and connection management live here. |
| `backend/ui/` | Reads console input, displays results, and calls application services and orchestrators. It does not own menu planning or shopping-list calculation. |

This is a dependency description, not a claim that every runtime path uses the same persistence lifetime. Section 6 documents the two connection patterns currently present.

## 2. Domain model and invariants

### Recipes, ingredients, blocks, and slots

`Recipe` is a frozen dataclass with `id: UUID`, `name`, `description`, `cooking_time`, and `number_meals`. `NewRecipe` holds the same creation fields without an ID. The database assigns the ID when `SqlRecipeRepository.add_recipe()` inserts a new recipe. `Recipe` has dataclass equality across all its fields; its UUID is not its only equality criterion. `Ingredient` is also frozen, with an ID, name, and standard `Unit`, but explicitly defines equality and hashing by ID. `NewIngredient` represents creation input.

`RecipeIngredient` holds an `Ingredient`, a `Unit`, and a `Decimal` quantity. The recipe ID is supplied separately to repository methods; the value object itself does not identify its parent recipe. `ShoppingListItem` has the same measured fields for aggregated output. Both measured dataclasses reject quantities less than or equal to zero at construction. These checks do not establish that an input unit is compatible with the ingredient's standard unit; conversion checks that later.

`MealBlock` is a frozen pair of `recipe_snapshot` and `length`. Generation sets `length` to the recipe's `number_meals`. The snapshot is the recipe object held by the block; there is no persisted menu, recipe version, or historical copy mechanism. `TimeSlot` is a frozen pair of day and meal time. It accepts arbitrary strings. The application-level `TimeSlotGenerator` supplies the expected weekly values; `TimeSlot` itself does not validate them.

### Menu as the planning boundary

`Menu` stores a mutable `TimeSlot -> MealBlock` dictionary and exposes a shallow copy through its `planning` property. `add_mealblock()` rejects a slot that is already occupied. `replace_mealblock()` and `delete_mealblock()` reject an unplanned slot. Other queries include `get_mealblock()`, `timeslots_for()`, `planned_timeslots()`, and `get_unique_mealblocks()`.

The checks have precise, separate meanings:

- `is_length_consistent()` compares each unique block's number of occurrences with its declared `length`.
- `total_meals()` sums the lengths of unique blocks. `is_stable()` requires both `len(planning) == total_meals()` and length consistency.
- `is_complete(expected_timeslots)` compares only the number of planned slots with the caller's expected number. A stable menu may be incomplete for a 14-slot week.

**Code guarantee:** a duplicate slot cannot be added through `add_mealblock()`, and the query methods return the checks described above. Individual menu mutation methods do not preserve all stability conditions on their own. There is no domain-level validation of day names, meal-time names, or the weekly slot count.

## 3. Menu generation, exclusions, and reroll

### Selecting and placing recipes

`RecipeRepository` is a domain protocol. `AvailableRecipeList` asks it for all recipes and removes those excluded by `RecipeExclusions`. The latter combines `UserExclusions` and `SystemExclusions` by UUID. `is_excluded()` is true when either source contains the ID; `get_exclusion_reasons()` can return `USER`, `SYSTEM`, both, or an empty set. Each exclusion source stores a set in memory. Adding the same ID twice is idempotent, removing an absent ID raises `ValueError`, and list methods return copies. `SystemExclusions` also supports `clear()`.

`MealBlockGenerator.generate_mealblocks(number_meals)` obtains the currently available recipes, repeatedly chooses one with `random.choice`, and keeps a local set of used recipe IDs. It accepts a candidate only when its length fits within the remaining target. It returns blocks whose lengths sum to the request, or raises `ValueError` when no recipes are available or more than 5,000 attempts are made. The generator does not know about `TimeSlot` or construct a `Menu`. Random selection is not seeded or injected, so the same inputs need not produce the same menu. Reaching the attempt limit is not proof that no valid combination exists.

`MenuPlanner.plan(timeslots, mealblocks)` verifies that the block lengths sum to the number of slots and that each supplied length is positive. It then places each block in successive slots and checks the resulting menu's stability. There is one placement strategy: the order of the input lists determines the result. No rule requires leftovers to fall on a following day. A duplicate `TimeSlot` in the supplied sequence is rejected indirectly when `Menu.add_mealblock()` detects the collision.

### Weekly generation use case

`TimeSlotGenerator.generate_timeslots(meal_count)` accepts 1 through 14 and returns that many entries from a fixed sequence, beginning with `sunday lunch` and ending with `saturday dinner`. `MenuOrchestrator.generate_menu()` always requests 14. Its flow is:

1. Clear the current system exclusions.
2. Generate the 14 slots and enough meal blocks from available recipes.
3. Ask `MenuPlanner` to build the menu.
4. Rebuild system exclusions from the IDs of the menu's unique blocks.
5. Return `MenuOrchestratorResult(success, menu, message)`.

The generator's local used-ID set prevents reuse *within* this generation. System exclusions are updated after the completed menu exists; they are not incrementally populated while choosing blocks. A caught `ValueError` produces a functional-failure result with `menu=None`; another caught exception produces a technical-failure result with `menu=None`. Because clearing happens before the `try` block and rebuilding mutates the exclusion set step by step, this is not a general atomicity guarantee for every possible failure.

### Reroll use case

`MenuOrchestrator.reroll_timeslot(menu, target_timeslot)` looks up the current block, requests a replacement of exactly its length, delegates the mutation to `MenuEditor`, then rebuilds system exclusions from the updated menu. `MealBlockGenerator.generate_replacement_mealblock(length)` filters available recipes by `number_meals == length` and randomly chooses a candidate. It takes no explicit exclusion-list argument because `AvailableRecipeList` already applies user and system exclusions.

`MenuEditor.reroll()` requires a planned target, a positive new length, a new block different from the current block and absent from the menu, and equal old and new lengths. It also checks that the old block occupies exactly its declared number of slots. It removes all of those occurrences, adds the new block in their places, and checks final stability. Selecting one slot of a multi-meal recipe therefore replaces the entire block. On success, the same `Menu` object has been mutated.

**Tested behavior:** domain and application tests cover nominal single- and multi-slot rerolls, unavailable replacements, invalid targets, and repository failures before mutation. They check menu and exclusion consistency in these paths. **Known limitation:** `MenuEditor` has no rollback after it begins removing slots. The orchestrator returns the supplied menu on a caught error, but its result object does not prove that the menu remained unchanged for an error after mutation started. Rebuilding system exclusions is also not an atomic operation.

## 4. Shopping-list calculation and units

`ShoppingListGenerator` depends on `RecipeIngredientRepository`. It first requires `menu.is_stable()`. For each unique block it retrieves the recipe's measured ingredients; an empty result raises `ValueError`. Each measured ingredient is normalized to its ingredient's standard unit and added to a `Decimal` total keyed by `Ingredient`, whose equality is ID-based. The output is a list of `ShoppingListItem` objects. A multi-slot block contributes its recipe's quantities once, not once per occupied slot. The calculation does not scale quantities by the block length.

`Unit` contains `mg`, `g`, `kg`, `mL`, `cL`, `L`, `teaspoon`, `tablespoon`, `bunch`, `pack`, and `unit`. `UNIT_CONVERSION_TO_STANDARD` accepts `mg/g/kg` for a `g` standard, `mL/cL/L` for an `mL` standard, and `teaspoon/tablespoon` for a `teaspoon` standard. The `bunch`, `pack`, and `unit` standards accept only themselves. The implementation does not convert between arbitrary dimensions or infer kitchen equivalents. An unsupported standard unit or incompatible recipe unit raises `ValueError` during normalization.

`ShoppingListOrchestrator.generate(menu)` returns `ShoppingListResult(success, shopping_list, message)` and converts `ValueError` into a failure result. Other exception types are not caught there and can reach the outer `main()` exception handler. **Tested behavior:** the domain tests cover normalization, aggregation across recipes, counting a multi-slot block once, unstable menus, and missing recipe ingredients. The repository's seed defines at least one ingredient association for each of its 12 recipes, but a database populated at another time may differ. The automated suite does not constitute an end-to-end CLI shopping-list test against every possible generated menu.

## 5. CRUD contracts and transaction boundary

`backend/domain/repositories.py` defines three protocols: `RecipeRepository`, `IngredientRepository`, and `RecipeIngredientRepository`. They specify list/find/create/update/delete operations for recipes and ingredients, and retrieval/addition/replacement/deletion of a recipe's ingredient associations. SQL implementations translate between these contracts and PostgreSQL rows. `RecipeIngredientRepository.update_recipe_ingredients()` replaces the complete association list, including the possibility of an empty list.

Three application services receive a `Callable[[], UnitOfWork]` and wrap **every method** in `with self._uow_factory() as uow`:

- `RecipeApplicationService` reads recipes and their ingredients, creates a recipe together with its associations, replaces both recipe fields and the full association list on update, and deletes associations before deleting a recipe.
- `IngredientApplicationService` provides ingredient list/get/create/update/delete operations.
- `RecipeIngredientApplicationService` provides direct operations on associations. It is implemented and tested but is not instantiated by `main.py`; the current CLI uses `RecipeApplicationService` for a recipe's associations.

Write methods call `uow.commit()` after their repository operations. Read methods do not commit. `UnitOfWork` is an application protocol exposing the three repositories plus `commit()`, `rollback()`, and context-manager methods. `SqlUnitOfWork` constructs all three SQL repositories with the same connection, rolls back on an exception or on a normal exit without commit, and always closes that connection. It does not suppress exceptions. A read-only service call also reaches rollback on normal exit because no commit was requested.

**Code guarantee for the current composition root:** `uow_factory()` in `main.py` calls `get_connection()` and constructs a fresh `SqlUnitOfWork` each time a CRUD service invokes it. Multiple SQL repository calls within one such service method use that UoW's connection. **Tested behavior:** service tests use fake UoWs to check results, commit calls, rollback calls, unknown IDs, and selected repository failures. SQL repository tests run against PostgreSQL. The fake UoW records rollback but does not restore fake repository state, and its test factories commonly return the same fake object. Those tests do not prove a fresh physical connection per call or SQL rollback semantics; there is no dedicated `SqlUnitOfWork` integration test in `tests/infrastructure/`.

## 6. Persistence and connection lifetimes

The PostgreSQL schema in `database/schema.sql` defines `recettes`, `unites`, `ingredients`, `recette_ingredients`, `saisons`, and `recette_saisons`. UUID primary keys use `gen_random_uuid()` from `pgcrypto`. Recipe, ingredient, and unit names are unique. A recipe has a positive `nombre_repas`; an association has a positive `quantite` and a composite `(recette_id, ingredient_id)` primary key. Foreign keys link associations and season mappings to their parent rows. The schema stores the recipe's measured unit separately from the ingredient's standard unit; unit compatibility is checked by domain conversion when building a shopping list, not by a SQL constraint. Season tables exist, but no current generation path filters by season.

`database/seed.sql` populates seasons, units, ingredients, 12 recipes, their ingredient associations, and some recipe-season associations. Every seeded recipe has at least one ingredient association in the script. The seed is for a fresh development database; its plain inserts are not an idempotent migration. `backend/infrastructure/db_connection.py` contains the current local PostgreSQL connection parameters.

There are **two connection lifetimes in the current implementation**:

| Path | Connection and ownership |
| --- | --- |
| CRUD service method | `uow_factory()` opens a new connection. `SqlUnitOfWork` shares it among its repositories, commits or rolls back according to the method path, and closes it on context exit. |
| Menu generation and shopping list | `main()` opens one connection before starting the CLI. The recipe repository used for availability and the recipe-ingredient repository used for shopping lists share it. `main()` closes it when the CLI exits or an outer exception occurs. These reads do not enter a CRUD UoW. |

This split is an observation of the present composition root, **not an architectural rule to preserve**. The two paths also mean that CRUD changes and later menu or shopping-list reads use different connections. The repository and schema establish the relevant SQL operations; this document does not assume a transaction policy beyond what the code explicitly commits, rolls back, or closes.

## 7. CLI responsibilities and current surface

The CLI offers a main menu for menu generation, recipe management, and ingredient management. The menu submenu exposes user exclusions, generation, reroll, and shopping-list display. `cli_exclusion_list.py` lets the user display, add, and remove excluded recipes; it receives the same `UserExclusions` instance that feeds `AvailableRecipeList`. That set lasts for the process and is not stored in PostgreSQL. The CLI holds the current menu in memory inside its menu submenu.

Recipe and ingredient menus expose list/create/update/delete flows. Recipe updates replace the entered recipe data and the complete ingredient list. `cli_helpers.py` handles display, numerical selection, unit prompts, and interactive measured-ingredient entry. The CLI performs some input checks, while SQL constraints, domain value checks, and repository errors provide additional validation. There is no uniform application-wide validation contract for every CLI input, and there are no automated UI tests in the current `tests/` tree.

## 8. Verification, guarantees, and remaining scope

`pytest.ini` points to `tests/` and adds the repository root to `pythonpath`. On 22 September 2026, `pytest -v` collected **157 tests and all 157 passed in 2.25 seconds**, including the PostgreSQL infrastructure tests in that environment. Tests are organized under application, domain, fakes, infrastructure, and test-object support modules. Their passing result confirms the exercised scenarios, not all possible runtime states.

The following distinctions should remain visible when this document is updated:

| Category | Current position |
| --- | --- |
| Code guarantees | The specific model checks, planner preconditions, generator output on successful return, UoW context behavior, and SQL constraints described above. |
| Tested behavior | The existing nominal and selected failure paths for planning, reroll, exclusions, shopping-list calculation, CRUD services, and SQL repositories. |
| Known limitations and debt | Random generation has a fixed attempt cap; menu and exclusion updates are not generally atomic; the connection lifetime differs between CRUD and generation/shopping paths; exclusions and menus are in memory; there is no operational web UI or season-based filtering. |

The sequential planner, in-memory exclusions, and simple CLI describe current choices. More advanced planning, persisted user preferences, and a graphical interface are possible future work; they are not implemented behavior. The diagrams in `docs/UML_schematics/` are intentionally selective views of the system. This document records the contracts and caveats those diagrams omit.
