"""
    Run unit test with command: pytest gptdb/datasource/rdbms/tests/test_conn_doris.py
"""

import pytest

from gptdb.datasource.rdbms.conn_doris import DorisConnector


@pytest.fixture
def db():
    conn = DorisConnector.from_uri_db("localhost", 9030, "root", "", "test")
    yield conn
