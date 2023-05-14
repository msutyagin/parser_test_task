import os
import pytest
from database import SqliteDatabaseConnector


@pytest.fixture(scope='session')
def setup_db():
    test_db_path = './parse_db_test.db'
    if not os.path.exists(test_db_path):
        with open(test_db_path, 'w') as f:
            f.write('')
    engine = SqliteDatabaseConnector().get_connection(test_db_path)
    yield engine
    os.remove(test_db_path)
