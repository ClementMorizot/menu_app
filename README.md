# Menu Generator

Menu Generator is a personal Python application that builds a weekly menu from recipes stored in PostgreSQL. It supports rerolling a recipe in the menu, managing recipes and ingredients through a command-line interface, and generating a shopping list.

## Current features

- A 14-meal menu from Sunday lunch through Saturday dinner. A `Recipe` can cover several `TimeSlot` instances within one `MealBlock`; the same recipe cannot appear in more than one block of a generated menu.
- Rerolling a selected `TimeSlot` replaces its entire `MealBlock` with an available recipe that covers the same number of meals.
- `UserExclusions` persist during the application session, while `SystemExclusions` are synchronized with recipes in the current menu.
- CRUD operations for recipes and ingredients, including management of the ingredients associated with a recipe.
- A shopping list calculated from the menu's unique blocks, with quantities converted to each ingredient's standard unit and aggregated.

The current interface is a **CLI**. The files in `frontend/` are empty; there is no operational web interface. Season tables exist in the database, but menu generation does not filter recipes by season.

## Architecture

The application has four layers inspired by DDD:

| Layer | Location | Responsibility |
| --- | --- | --- |
| Domain | `backend/domain/` | Models, menu invariants, generation, planning, reroll, exclusions, units, shopping-list calculation, and repository protocols. |
| Application | `backend/application/` | Use-case orchestrators, `TimeSlot` generation, CRUD services, and the `UnitOfWork` protocol. |
| Infrastructure | `backend/infrastructure/` | PostgreSQL connection, SQL repositories, and `SqlUnitOfWork`. |
| UI | `backend/ui/` | Console menus, input, and output. |

`backend/main.py` assembles the components. Tests live in `tests/`; the database schema and development seed live in `database/`.

The current code uses two connection lifetimes: each CRUD service operation creates its own `SqlUnitOfWork` and connection, while menu generation and shopping-list calculation use repositories bound to a connection kept open for the CLI session. This describes the implementation, not an architectural rule to preserve.

The [living technical reference](docs/technical_notes.md) explains contracts, data flows, tests, and their limits. The [PlantUML diagrams](docs/UML_schematics/) provide focused views. The [v0.1 technical memoir](docs/Memoire_Technique_Application_Generation_Menu_v0.1.docx) is a **historical archive**: it describes the v0.1 milestone and is not the reference for the current application.

## Setup and execution

The application was developed and tested with Python 3.13, PostgreSQL, `psycopg`, and `pytest` for the test suite. The repository has no dependency manifest; install these packages in the Python environment you choose.

1. Create a PostgreSQL database and user matching the development connection settings in `backend/infrastructure/db_connection.py`.
2. Run `database/schema.sql`, then `database/seed.sql`, against a fresh development database. The seed supplies ingredient associations for all 12 recipes it inserts. It is neither a migration nor a script designed to be rerun against an already seeded database.
3. From the repository root, start the application as a module:

```powershell
python -m backend.main
```

The entry point uses absolute `backend.*` imports, which is why it is launched as a module from the repository root.

## Tests

```powershell
pytest -v
```

On 22 September 2026, `pytest -v` collected and ran **157 tests; all 157 passed in 2.25 seconds**. This included the infrastructure tests against PostgreSQL. Domain and application tests also use fakes.

## Current scope

Planning remains sequential, and recipe selection uses `random.choice` with an attempt limit. Persistent user preferences, advanced planning strategies, and a graphical interface are not implemented. Exclusions are not persisted between application runs.
