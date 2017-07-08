import gc
import os
import pytest
import sqlite3
import tempfile
from aws_sg_mngr.sqliteStore import SqliteStore
from aws_sg_mngr.registeredCidr import RegisteredCidr

MOCK_DB_FILE = tempfile.mkstemp()[1]
TEST_CIDR = '1.2.3.4/32'
TEST_DESCRIPTION = 'DESCRIPTION OF THE CIDR'
TEST_LOCATION = 'CIDR LOCATION'
TEST_OWNER = 'OWNER NAME'
TEST_EXPIRATION = 1000


class MockConfig(object):

    def get(self, first, second):
        if 'path' in second:
            return MOCK_DB_FILE


@pytest.mark.order1
def test_init():

    # Delete existing DB to init from a clean state
    if os.path.exists(MOCK_DB_FILE):
        os.remove(MOCK_DB_FILE)

    db = SqliteStore(MockConfig())
    assert db
    # Only the Global CIDR should appear here
    assert len(db.query_all()) == 1

    # Forcibly destroy DB object to close connection
    gc.disable()
    del db
    gc.enable()

    # Test the existing DB
    db = SqliteStore(MockConfig())
    # Again, only the Global CIDR should appear
    assert len(db.query_all()) == 1

    # Cleanup
    os.remove(MOCK_DB_FILE)


@pytest.mark.order2
def test_store_cidr():
    db = SqliteStore(config=MockConfig())
    expected_cidr = RegisteredCidr(
        cidr=TEST_CIDR, description=TEST_DESCRIPTION, owner=TEST_OWNER,
        location=TEST_LOCATION, expiration=TEST_EXPIRATION)

    db.store_cidr(expected_cidr)

    actual_cidr = db.query_one(TEST_CIDR)

    assert actual_cidr.cidr == TEST_CIDR
    assert actual_cidr.description == TEST_DESCRIPTION
    assert actual_cidr.location == TEST_LOCATION
    assert actual_cidr.owner == TEST_OWNER
    assert actual_cidr.expiration == TEST_EXPIRATION


@pytest.mark.order3
def test_query_one():
    db = SqliteStore(config=MockConfig())

    # Due to pytest.mark, this test runs after the insert,
    # so we should have this RegisteredCidr
    cidr = db.query_one(TEST_CIDR)
    assert cidr.cidr == TEST_CIDR
    assert cidr.description == TEST_DESCRIPTION
    assert cidr.location == TEST_LOCATION
    assert cidr.owner == TEST_OWNER
    assert cidr.expiration == TEST_EXPIRATION

    fake_cidr = db.query_one("FAKE CIDR")
    assert fake_cidr is None


@pytest.mark.order3
def test_query_all():
    db = SqliteStore(config=MockConfig())
    cidrs = db.query_all()

    # This test also runs after the insert, so we should still have two
    assert len(cidrs) == 2
