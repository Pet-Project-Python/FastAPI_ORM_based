ORM based microservice project layout
----------

Stack in project
----------

**Python 3.10.4**

**Postgres 14.3**

``Сonnect to RDBMS``
**asyncpg**

``For working with db``
**sqlalchemy[asyncio]**

Install
----------
``Install Poetry``

https://python-poetry.org/docs/

Quickstart
----------

First, run the following commands to bootstrap your environment with ``poetry``:

    git clone https://github.com/kvell-group/your-project.git
    cd your-project
    poetry shell
    poetry install

Then create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application:

    touch .env
    echo APP_ENV=dev
    echo DATABASE_URL=postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB >> .env
    echo SECRET_KEY=$(openssl rand -hex 32) >> .env

To run the web application in debug use:

    alembic revision --autogenerate -m "init”
    alembic upgrade head
    uvicorn app.main:app --reload

Docker
----------
Keep in mind in the Dockerfile poetry is configured to install dependencies
to prod for install all packages on your local docker images remove ``poetry install --no-dev``
and put ``poetry install``in Dockerfile

To run the web application in docker use:

    docker-compose up -d --build
    docker-compose exec db psql --username=db_user --dbname=db_name
    docker-compose exec app poetry run alembic init -t async migrations
    docker-compose logs app
    docker-compose exec app poetry run alembic revision --autogenerate -m "init"
    docker-compose exec app poetry run alembic upgrade head

Application will be available on ``localhost:8080`` in your browser.

Run tests
---------

Tests for this project are defined in the ``tests/`` folder.

Set up environment variable ``DATABASE_URL`` or set up ``database_url`` in ``app/core/settings/test.py``

This project uses `pytest <https://docs.pytest.org/>`_ to define tests because it allows you to
use the ``assert`` keyword with good formatting for failed assertations.

To run all the tests on your local machine of a project, simply run the ``pytest`` command
or if you want to run in docker images use this command
``docker-compose exec app poetry run pytest -s``:

    $ pytest
    ================================================= test session starts ==================================================
    platform linux -- Python 3.8.3, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
    rootdir: /home/some-user/user, inifile: setup.cfg, testpaths: tests
    plugins: env-0.6.2, cov-2.9.0, asyncio-0.12.0
    collected 90 items

    tests/test_api/test_errors/test_422_error.py .                                                                   [  1%]
    tests/test_api/test_errors/test_error.py .                                                                       [  2%]
    tests/test_api/test_routes/test_tags.py ..                                                                       [ 67%]
    tests/test_db/test_queries/test_tables.py ...                                                                    [ 93%]
    tests/test_schemas/test_rw_model.py .                                                                            [ 94%]

    ============================================ 6 passed in 7.50s (0:00:10)=============================================
    $

If you want to run a specific test, you can do this with `this
<https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`_ pytest feature: ::

    $ pytest tests/test_api/test_routes/test_users.py::test_user_can_not_take_already_used_credentials

If you want to see the coverage of your tests in your browser you must use the command in console `coverage html` after the
library coverage will create for you the directory `htmlcov`, inside the directory `htmlcov` you must open the file `index.html` in your browser

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.

Project structure
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are::

    app
    ├── api              - web related stuff.
    │   ├── dependencies - dependencies for routes definition.
    │   ├── handler      - definition of error handlers.
    │   └── endpoints    - web routes.
    ├── core             - application configuration, startup events, logging.
    ├── db               - db related stuff.
    │   ├── alembic      - manually written alembic migrations.
    │   ├── models       - sqlalchemy models.
    │   └── repositories - all crud stuff.
    ├── models           - pydantic models for this application.
    │   ├── domain       - main models that are used almost everywhere.
    │   └── schemas      - schemas for using in web routes.
    ├── resources        - strings that are used in web responses.
    ├── services         - logic that is not just crud related.
    └── main.py          - FastAPI application creation and configuration.

Fork hints
----------

After forking this project, you should change the following things:

-  ``app/core/settings/base.py`` - change ``PROJECT_NAME`` and ``PROJECT_DESCRIPTION`` variables.
-  ``pyproject.toml`` - change ``name`` and ``description`` variables.
-  ``README.md`` - change project description.
-  ``docker-compose.yml`` - change ``volumes`` and ``image`` variables.
