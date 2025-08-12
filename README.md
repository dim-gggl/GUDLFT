[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) [![Static Badge](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-%233775A9?style=plastic&logo=python&logoColor=%23FFE569)](https://www.python.org/) [![Static Badge](https://img.shields.io/badge/flask-3.1.1-%239ECEE3?style=plastic&logo=flask)](https://github.com/pallets/flask/)  
[![Static Badge](https://img.shields.io/badge/pytest-8.4.1-%233775A9?style=plastic&logo=pytest)](https://github.com/pytest-dev/pytest/) [![Static Badge](https://img.shields.io/badge/coverage.py-7.10.3-%231AE058?style=plastic&logo=coverage)](https://github.com/nedbat/coveragepy) [![Static Badge](https://img.shields.io/badge/locust-2.38.1-%23125338?style=plastic&logo=locust)](https://locust.io/)  
  
> [Français](#-gudlft--portail-dinscription-aux-compétitions)

# <div align="center"> 🇬🇧 GUDLFT <br> *Competition registration portal*

GUDLFT is a **Flask** application that enables powerlifting clubs to
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

> _What does **GUDLFT** do ?_

- Displays a list of registered clubs with their points.
- Is accessible via an e-mail address.
- Allows to reserve places according to:
  - the number of points the club has.
  - the number of places available.
- Is covered by unit and functional tests.
- Data management via two JSON files: 
  - `clubs.json`
  - `competitions.json`

---

## Business rules

| **RULE** | **DETAIL** |
| --- | --- | 
| **Places limit** | A club may not reserve more than 12 places in any one competition. |
| **Places availability** | The reservation cannot exceed the number of places remaining for the competition. |
| **Points requirement** | The club must have **at least** as many points as the number of places requested.
| **Past competitions** | It is not possible to book a competition that has already passed. |

   > _These rules are centralized in `validators.py`._

---

## Setup

1. **Clone this repo**  

```bash
git clone https://github.com/dim-gggl/GUDLFT.git
cd GUDLFT
```
2. **Create a virtual environment** (recommended)  
  
```bash
python3 -m venv .venv
source .venv/bin/activate # under macOS/Linux
.venv\Scripts\activate # under Windows
```
3. **Install dependencies**
  
There's a lot of packages listed in the requirements (see the end of the README to check [the dependency tree](#dependencies-tree-generated-with-uv-tree)).
   ```bash
   pip install -r requirements.txt
   ```

---

## Launch **GUDLFT**

```bash
python server.py
```

By default, the application listens on `http://127.0.0.1:5000`.  
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
pytest            # run all tests
pytest -q         # silent mode
coverage report   # display a coverage report in the terminal
coverage html     # generate an HTML report in the `htmlcov/` directory
```

- **Unit tests**: business logic (`tests/unit_tests/`).
- **Functional tests**: user scenarios via Flask client (`tests/functional_tests/`).
- **Integration tests**: files ready for future tests (`tests/integration_tests/`).

The HTML coverage report is generated in `htmlcov/` and can be open
with any browser.

---

## Performance testing (Locust)

To launch the performance tests, we need to start with a bit of installation:

```bash
# Under macOS/Linux :
export LOCUST_LOCUSTFILE="tests/locust_files/locustfile.py"

# Under Windows :
set LOCUST_LOCUSTFILE="tests/locust_files/locustfile.py"
```

Then, we can launch the tests using the command:
```bash
locust --config .locust.conf
```

- You should see a message indicating that the web interface is running at `http://0.0.0.0:8089/`  
- Open your browser and navigate to this address.
- The Locust web interface should appear with the fields pre-filled according to the parameters available in the `.locust.conf` file
- Finally, let yourself be guided through the interface to generate a performance report.


---

## Project structure

```bash
GUDLFT
├── clubs.json
├── README.md
├── competitions.json
├── config.py
├── data_manager.py
├── htmlcov                  # Coverage Report    
│   ├── __init___py.html
│   ├── class_index.html
│   ├── config_py.html
│   ├── ... 
│   ├── ...
├── server.py                # Entry point to the app
├── static
│   └── style.css
├── templates
│   ├── base.html
│   ├── booking.html
│   ├── index.html
│   ├── macros
│   │   └── display_message.html
│   ├── points.html
│   └── welcome.html
├── test_runner.py
├── tests
│   ├── functional_tests
│   │   ├── conftest.py
│   │   ├── test_authentication.py
│   │   ├── test_points_display.py
│   │   └── test_reservations.py
│   ├── integration_tests
│   │   └── test_booking_integration.py
│   ├── load_tests
│   │   └── locustfile.py
│   └── unit_tests
│       ├── test_config.py
│       ├── test_data_manager.py
│       ├── test_server.py
│       └── test_validators.py
└── validators.py
```

## Dependencies Tree (Generated with `uv tree`)

```bash
├── coverage v7.10.3
├── flask v3.1.1
│   ├── blinker v1.9.0
│   ├── click v8.2.1
│   ├── itsdangerous v2.2.0
│   ├── jinja2 v3.1.6
│   │   └── markupsafe v3.0.2
│   ├── markupsafe v3.0.2
│   └── werkzeug v3.1.3
│       └── markupsafe v3.0.2
├── locust v2.38.1            # Most of the required packages are Locust dependencies.
│   ├── configargparse v1.7.1
│   ├── flask v3.1.1 (*)
│   ├── flask-cors v6.0.1
│   │   ├── flask v3.1.1 (*)
│   │   └── werkzeug v3.1.3 (*)
│   ├── flask-login v0.6.3
│   │   ├── flask v3.1.1 (*)
│   │   └── werkzeug v3.1.3 (*)
│   ├── gevent v25.5.1
│   │   ├── greenlet v3.2.4
│   │   ├── zope-event v5.1.1
│   │   │   └── setuptools v80.9.0
│   │   └── zope-interface v7.2
│   │       └── setuptools v80.9.0
│   ├── geventhttpclient v2.3.4
│   │   ├── brotli v1.1.0
│   │   ├── certifi v2025.8.3
│   │   ├── gevent v25.5.1 (*)
│   │   └── urllib3 v2.5.0
│   ├── locust-cloud v1.26.3
│   │   ├── configargparse v1.7.1
│   │   ├── gevent v25.5.1 (*)
│   │   ├── platformdirs v4.3.8
│   │   ├── python-engineio v4.12.2
│   │   │   └── simple-websocket v1.1.0
│   │   │       └── wsproto v1.2.0
│   │   │           └── h11 v0.16.0
│   │   └── python-socketio[client] v5.13.0
│   │       ├── bidict v0.23.1
│   │       ├── python-engineio v4.12.2 (*)
│   │       ├── requests v2.32.4 (extra: client)
│   │       │   ├── certifi v2025.8.3
│   │       │   ├── charset-normalizer v3.4.3
│   │       │   ├── idna v3.10
│   │       │   └── urllib3 v2.5.0
│   │       └── websocket-client v1.8.0 (extra: client)
│   ├── msgpack v1.1.1
│   ├── psutil v7.0.0
│   ├── pyzmq v27.0.1
│   ├── requests v2.32.4 (*)
│   ├── setuptools v80.9.0
│   └── werkzeug v3.1.3 (*)
└── pytest v8.4.1
    ├── iniconfig v2.1.0
    ├── packaging v25.0
    ├── pluggy v1.6.0
    └── pygments v2.19.2

(*) Package tree already displayed
```  
  
---

# <div align="center"> 🇫🇷 GUDLFT <br> *Portail d’inscription aux compétitions*

GUDLFT est une application **Flask** qui permet aux clubs d'haltérophilie de
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

> _Que fait **GUDLFT** ?_

- Affiche la liste des clubs inscrits avec leur capital de points.
- Est accessible via une adresse e-mail.
- Permet de réserver des places selon :
  - le nombre de points disponibles.
  - le nombre de places disponibles.
- Est couvert par des tests unitaires et fonctionnels.
- Gestion des données via deux fichiers JSON :  
  - `clubs.json`
  - `competitions.json`

---

## Règles métier

| **RÈGLE** | **DÉTAIL** |
|-------|--------|
| **Limite de places** | Un club ne peut pas réserver **plus de 12 places** sur une même compétition. |
| **Places disponibles** | La réservation ne peut pas dépasser le nombre de places restantes pour la compétition. |
| **Points du club** | Le club doit posséder **au moins** autant de points que de places demandées. |
| **Compétitions passées** | Il est impossible de réserver une compétition déjà passée dans le temps. |

> _Ces règles sont centralisées dans `validators.py`._

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
> Il y a beaucoup de packages listés dans le fichier requirements.txt (voir la fin du README pour vérifier l'arbre des dépendances).
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
coverage report # affiche un rapport de couverture
coverage html # génère un rapport HTML
```

- **Tests unitaires** : logique métier (`tests/unit_tests/`).
- **Tests fonctionnels** : scénarios utilisateur via le client Flask (`tests/functional_tests/`).
- **Tests d’intégration** : dossiers prêts pour accueillir vos futurs tests (`tests/integration_tests/`).

Le rapport HTML de couverture est généré dans `htmlcov/` et peut être ouvert
avec n’importe quel navigateur.

---

## Test de charge et de performance (Locust)

Pour lancer les tests de chargement et de performance, il faut commencer par un peu d'installation :
```bash
# Sur macOS/Linux :
export LOCUST_LOCUSTFILE="tests/locust_files/locustfile.py"

# Sur Windows :
set LOCUST_LOCUSTFILE="tests/locust_files/locustfile.py"
```
Ensuite, il ne reste qu'à lancer les tests à l'aide la commande :
```bash
locust --config .locust.conf
```

- Vous devrier voir apparaître un message spécifiant que l'interface web est lancée à `http://0.0.0.0:8089/`  
- Ouvrez votre navigateur et rendez-vous à cette adresse.
- L'interface web de Locust devrait apparaître avec les champs pré-remplis selon les paramètres disponibles dans le fichier `.locust.conf`
- Enfin, laissez-vous guider par l'interface afin de générer un rapport de performance.
---

## Structure du projet

```bash
GUDLFT
├── clubs.json
├── README.md
├── competitions.json
├── config.py
├── data_manager.py
├── htmlcov                  # Rapport de Coverage 
│   ├── __init___py.html
│   ├── class_index.html
│   ├── config_py.html
│   ├── ... 
│   ├── ...
├── server.py                # Point d'entrée de l'application
├── static
│   └── style.css
├── templates
│   ├── base.html
│   ├── booking.html
│   ├── index.html
│   ├── macros
│   │   └── display_message.html
│   ├── points.html
│   └── welcome.html
├── test_runner.py
├── tests
│   ├── functional_tests
│   │   ├── conftest.py
│   │   ├── test_authentication.py
│   │   ├── test_points_display.py
│   │   └── test_reservations.py
│   ├── integration_tests
│   │   └── test_booking_integration.py
│   ├── load_tests
│   │   └── locustfile.py
│   └── unit_tests
│       ├── test_config.py
│       ├── test_data_manager.py
│       ├── test_server.py
│       └── test_validators.py
└── validators.py
```

## Arbre des dépendances (Généré avec `uv tree`)

```bash
├── coverage v7.10.3
├── flask v3.1.1
│   ├── blinker v1.9.0
│   ├── click v8.2.1
│   ├── itsdangerous v2.2.0
│   ├── jinja2 v3.1.6
│   │   └── markupsafe v3.0.2
│   ├── markupsafe v3.0.2
│   └── werkzeug v3.1.3
│       └── markupsafe v3.0.2
├── locust v2.38.1            # La plupart des packages requis sont des dépendances de Locust.
│   ├── configargparse v1.7.1
│   ├── flask v3.1.1 (*)
│   ├── flask-cors v6.0.1
│   │   ├── flask v3.1.1 (*)
│   │   └── werkzeug v3.1.3 (*)
│   ├── flask-login v0.6.3
│   │   ├── flask v3.1.1 (*)
│   │   └── werkzeug v3.1.3 (*)
│   ├── gevent v25.5.1
│   │   ├── greenlet v3.2.4
│   │   ├── zope-event v5.1.1
│   │   │   └── setuptools v80.9.0
│   │   └── zope-interface v7.2
│   │       └── setuptools v80.9.0
│   ├── geventhttpclient v2.3.4
│   │   ├── brotli v1.1.0
│   │   ├── certifi v2025.8.3
│   │   ├── gevent v25.5.1 (*)
│   │   └── urllib3 v2.5.0
│   ├── locust-cloud v1.26.3
│   │   ├── configargparse v1.7.1
│   │   ├── gevent v25.5.1 (*)
│   │   ├── platformdirs v4.3.8
│   │   ├── python-engineio v4.12.2
│   │   │   └── simple-websocket v1.1.0
│   │   │       └── wsproto v1.2.0
│   │   │           └── h11 v0.16.0
│   │   └── python-socketio[client] v5.13.0
│   │       ├── bidict v0.23.1
│   │       ├── python-engineio v4.12.2 (*)
│   │       ├── requests v2.32.4 (extra: client)
│   │       │   ├── certifi v2025.8.3
│   │       │   ├── charset-normalizer v3.4.3
│   │       │   ├── idna v3.10
│   │       │   └── urllib3 v2.5.0
│   │       └── websocket-client v1.8.0 (extra: client)
│   ├── msgpack v1.1.1
│   ├── psutil v7.0.0
│   ├── pyzmq v27.0.1
│   ├── requests v2.32.4 (*)
│   ├── setuptools v80.9.0
│   └── werkzeug v3.1.3 (*)
└── pytest v8.4.1
    ├── iniconfig v2.1.0
    ├── packaging v25.0
    ├── pluggy v1.6.0
    └── pygments v2.19.2

(*) Package tree already displayed
```