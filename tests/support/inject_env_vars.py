import os

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    # This is needed because pytest django creates a database, so schema should not be used
    os.environ["DB_DATABASE"] = os.getenv("DB_MASTER_DATABASE")
    os.environ["DB_USER"] = os.getenv("DB_MASTER_USER")
    os.environ["DB_PASSWORD"] = os.getenv("DB_MASTER_PASSWORD")
