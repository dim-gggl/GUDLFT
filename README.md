# <div align="center"> 🇬🇧 GUDLFT <br> *Competition registration portal*

GUDLFT is a **Flask** application that enables climbing clubs to
reserve places for competitions while managing their points capital.
This project is part of the OpenClassrooms *Python Developer* course
and focuses on **code quality**: 
- **AUTOMATED TESTING**
- **REFACTORING**
- **GOOD PRACTICES**
- **VERSION CONTROL**
- **TEST COVERAGE**

---

## Contents
1. [Features](#features)
2. [Business rules](#business-rules)
3. [Installation](#installation)
4. [Application launch](#lancement-de-lappication)
5. [Test execution](#test-execution)
6. [Project structure](#project-structure)
7. [Contribute](#contribute)
8. [License](#licence)

---

## Features

What the application does:

- Easy access connection to the app via e-mail address.
- A view of upcoming competitions.
- A platform to reserve places according to the number of points available.
- A real-time display of remaining points by club.
- Data management via two JSON files: `clubs.json` and `competitions.json`.

---

## Business rules

| **RULE** | **DETAIL** |
| --- | --- | 
| **Places limit** | A club may not reserve more than 12 places in any one competition. |
| **Places availability** | The reservation cannot exceed the number of places remaining for the competition. |
| **Points requirement** | The club must have **at least** as many points as the number of places requested.
| **Past competitions** | It is not possible to book a competition that has already passed. |

    These rules are centralized in `validators.py` and covered by unit and functional tests.

---

## Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/dim-gggl/GUDLFT.git
   cd GUDLFT
   ```
2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate # under macOS/Linux
   venv\Scripts\activate # under Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Launch application

```bash
python server.py
```

By default, the application listens on `http://localhost:5000`.  
The following environment variables can be overridden:

| Variable | Default value | Description |
|:-:|:-:|:-:|
| `SECRET_KEY` | `something_special` | Flask secret key |
| `FLASK_DEBUG` | `1` | Enable hot reload and debugging |
| `FLASK_RUN_PORT` | `5000` | Listening port |

---

## Test execution

The test suite is written with **pytest** :

```bash
pytest # run all tests
pytest -q # silent mode
coverage run -m pytest # adds a coverage report
coverage html # generates an HTML report
```

- **Unit tests**: business logic (`tests/unit_tests/`).
- **Functional testing**: user scenarios via Flask client (`tests/functional_tests/`).
- **Integration tests**: files ready for future tests (`tests/integration_tests/`).

The HTML coverage report is generated in `htmlcov/index.html` and can be opened
with any browser.

---

## Load testing

```bash
########################################################
#                   IN PROGRESS                        
########################################################
```


---

## Project structure

```bash
GUDLFT/
├── __init__.py
├── clubs.json
├── competitions.json
├── config.py
├── data_manager.py
├── htmlcov/                     # Rapport de couverture de tests
├── pytest.ini
├── README.md
├── requirements.txt
├── server.py
├── static/
│   └── style.css               # Feuille de style globale
├── templates/
│   ├── base.html               # Gabarit principal
│   ├── booking.html
│   ├── index.html
│   ├── points.html
│   ├── welcome.html
│   └── macros/
│       └── display_message.html
├── test_runner.py
├── tests/
│   ├── functional_tests/
│   │   ├── __init_.py
│   │   ├── conftest.py
│   │   ├── test_authentication.py
│   │   ├── test_points_display.py
│   │   └── test_reservations.py
│   ├── integration_tests/
│   └── unit_tests/
│       ├── __init__.py
│       ├── test_config.py
│       ├── test_data_manager.py
│       ├── test_server.py
│       └── test_validators.py
└── validators.py
```
---

# <div align="center"> 🇫🇷 GUDLFT <br> *Portail d’inscription aux compétitions*

GUDLFT est une application **Flask** qui permet aux clubs d’escalade de
réserver des places pour des compétitions tout en gérant leur capital de
points.  
Ce projet s’inscrit dans le cadre du parcours *Tests en Python* d’OpenClassrooms
et met l’accent sur la **qualité du code** : 
- **TESTS AUTOMATISÉS**
- **REFACTORING**
- **BONNES PRATIQUES**
- **VERSION CONTROL**
- **COUVERTURE DE CODE**

---

## Sommaire
1. [Fonctionnalités](#fonctionnalités)
2. [Règles métier](#règles-métier)
3. [Installation](#installation)
4. [Lancement de l’application](#lancement-de-lapplication)
5. [Exécution des tests](#exécution-des-tests)
6. [Structure du projet](#structure-du-projet)
7. [Contribuer](#contribuer)
8. [Licence](#licence)

---

## Fonctionnalités

Ce que permet l'application :

- Connexion rapide d’un club par adresse e-mail.
- Visualisation des compétitions à venir.
- Réservation de places selon le nombre de points disponibles.
- Affichage en temps réel des points restants par club.
- Gestion des données via deux fichiers JSON :  
  `clubs.json` et `competitions.json`.

---

## Règles métier

| **RÈGLE** | **DÉTAIL** |
|-------|--------|
| **Limite de places** | Un club ne peut pas réserver **plus de 12 places** sur une même compétition. |
| **Places disponibles** | La réservation ne peut pas dépasser le nombre de places restantes pour la compétition. |
| **Points du club** | Le club doit posséder **au moins** autant de points que de places demandées. |
| **Compétitions passées** | Il est impossible de réserver une compétition déjà passée dans le temps. |

Ces règles sont centralisées dans `validators.py` et couvertes par des tests
unitaires et fonctionnels.

---

## Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/dim-gggl/GUDLFT.git
   cd GUDLFT
   ```
2. **Créer un environnement virtuel** (optionnel mais recommandé)  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # sous macOS/Linux
   venv\Scripts\activate      # sous Windows
   ```
3. **Installer les dépendances**  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Lancement de l’application

```bash
python server.py
```

Par défaut, l’application écoute sur `http://localhost:5000`.  
Les variables d’environnement suivantes peuvent être surchargées :

| Variable | Valeur par défaut | Description |
|:-:|:-:|:-:|
| `SECRET_KEY` | `something_special` | Clé secrète Flask |
| `FLASK_DEBUG` | `1` | Active le rechargement à chaud et le debug |
| `FLASK_RUN_PORT` | `5000` | Port d’écoute |

---

## Exécution des tests

La suite de tests est écrite avec **pytest** :

```bash
pytest          # lance tous les tests
pytest -q       # mode silencieux
coverage run -m pytest # ajoute un rapport de couverture
coverage html # génère un rapport HTML
```

- **Tests unitaires** : logique métier (`tests/unit_tests/`).
- **Tests fonctionnels** : scénarios utilisateur via le client Flask (`tests/functional_tests/`).
- **Tests d’intégration** : dossiers prêts pour accueillir vos futurs tests (`tests/integration_tests/`).

Le rapport HTML de couverture est généré dans `htmlcov/` et peut être ouvert
avec n’importe quel navigateur.

---

## Load testing

```bash
########################################################
#                   IN PROGRESS                        
########################################################
```

---

## Structure du projet

```bash
GUDLFT/
├── __init__.py
├── clubs.json
├── competitions.json
├── config.py
├── data_manager.py
├── htmlcov/                     # Rapport de couverture de tests
├── pytest.ini
├── README.md
├── requirements.txt
├── server.py
├── static/
│   └── style.css               # Feuille de style globale
├── templates/
│   ├── base.html               # Gabarit principal
│   ├── booking.html
│   ├── index.html
│   ├── points.html
│   ├── welcome.html
│   └── macros/
│       └── display_message.html
├── test_runner.py
├── tests/
│   ├── functional_tests/
│   │   ├── __init_.py
│   │   ├── conftest.py
│   │   ├── test_authentication.py
│   │   ├── test_points_display.py
│   │   └── test_reservations.py
│   ├── integration_tests/
│   └── unit_tests/
│       ├── __init__.py
│       ├── test_config.py
│       ├── test_data_manager.py
│       ├── test_server.py
│       └── test_validators.py
└── validators.py
```
