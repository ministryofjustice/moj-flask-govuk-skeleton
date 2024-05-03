# Fixtures defined in this file can be used by all tests in sub-directories.
import pytest
from app import create_app


# Setting the scope to session means that a live_server will exist for all your tests.
# This is good for performance but you can change this to "module", "class" or "function" if you want better test isolation.
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": True,
        "SERVER_NAME": "localhost"
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
