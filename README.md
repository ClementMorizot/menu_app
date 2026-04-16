# Menu Generator

## Introduction
A backend application that generates weekly menus based on personal recipes. 
Built using a *Domain-Driven Design (DDD)* architecture, the project focuses on clean separation of concerns, domain modeling, and testable business logic. 

This project is part of my transition into software engineering.

## Quick Overview

- 3-layer architecture (Domain / Application / Infrastructure)
- Fully tested domain logic (unit tests with pytest)
- PostgreSQL integration
- Designed for extensibility (multi-meal recipes, reroll, future constraints)

## Project Goal
- Solve a real-life problem (meal planning and groceries list)
- Demonstrate clean architecture
- Build a scalable backend foundation
- Integrate multiple components (database, domain logic, orchestration)

## Features
- Store and manage recipes using PostgreSQL
- Generate a full weekly menu (14 meals)
- Support multi-meal recipes
- Deterministic planning logic

## Architecture

### Domain-Driven Design architecture
- **Domain Layer**: core business logic (Menu, MealBlock, TimeSlot)
- **Application Layer**: orchestration (MenuOrchestrator)
- **Infrastructure Layer**: database access (PostgreSQL)

### Key design principles
- Strict separation of concerns
- Deterministic domain logic
- Full unit test coverage

## Project Structure
```plaintext
menu-generator/
│
├── backend/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── tests/
│   │   ├── application/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   ├── fakes/
│   │   └── test_objects/
│   └── main.py
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── docs/
│
├── README.md
├── pytest.ini
└── .gitignore
```

## Setup and Installation

### Prerequisites
- Python 3.x
- PostgreSQL
- psycopg
- pytest

### Set-up
1. Create a PostgreSQL database
2. Execute `schema.sql` and `seed.sql`
3. Configure database credentials in `db_connection.py`

### Launch
```bash
python backend/main.py
```

## Tests
49 unit tests are implemented using pytest to validate the domain logic and application behavior.
```bash
pytest -v
```
1 test validates database connection

## Current Status
- Backend fully functional
- End-to-end menu generation working
- Console-based interface
- Core domain validated with tests

Limitations:
- No UI yet
- Reroll logic lacks input validation at application level
- No user preferences

## Future Improvements
- User interface
- Recipe management (complete CRUD flow)
- Grocery list generation
- Generation constraints (seasonality, user preferences)
- Advanced planning strategies

## What I learned
This project allowed me to practice:

- Domain-Driven Design (DDD)
- Layered architecture
- Separation of concerns
- Domain modeling and invariants
- Unit testing strategy (pytest)
- PostgreSQL integration
