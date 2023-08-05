import pathlib
import sqlite3
import tempfile

from selutil.database import Database, get_tables


def test_get_tables_empty():
    conn = sqlite3.connect(':memory:')
    assert get_tables(conn) == []


def test_get_tables_not_empty():
    conn = sqlite3.connect(':memory:')
    with conn:
        conn.execute('CREATE TABLE test1 (test1_id INTEGER PRIMARY KEY)')
        conn.execute('CREATE TABLE test2 (test2_id INTEGER PRIMARY KEY)')
    assert get_tables(conn) == ['test1', 'test2']


def test_Database_apply_migrations_all():
    db = Database(':memory:')
    assert db.get_tables() == ['versions']
    db.apply_migrations(pathlib.Path(__file__).parent / 'migrations')
    assert db.get_version() == 2
    assert db.get_tables() == ['versions', 'table1', 'table2']


def test_Database_apply_migrations_already_exists():
    with tempfile.NamedTemporaryFile() as tmp:
        db = Database(tmp.name)
        assert db.get_tables() == ['versions']
        db.apply_migrations(pathlib.Path(__file__).parent / 'migrations')
        assert db.get_version() == 2
        assert db.get_tables() == ['versions', 'table1', 'table2']
        del db
        db = Database(tmp.name)
        assert db.get_version() == 2
        assert db.get_tables() == ['versions', 'table1', 'table2']
        db.apply_migrations(pathlib.Path(__file__).parent / 'migrations')
        assert db.get_version() == 2
        assert db.get_tables() == ['versions', 'table1', 'table2']


def test_Database_apply_migrations_only_second():
    db = Database(':memory:')
    assert db.get_tables() == ['versions']
    with db.connection as conn:
        conn.execute('INSERT INTO versions VALUES(1,"now")')
    db.apply_migrations(pathlib.Path(__file__).parent / 'migrations')
    assert db.get_version() == 2
    assert db.get_tables() == ['versions', 'table2']


def test_Database_get_tables():
    db = Database(':memory:')
    assert db.get_tables() == ['versions']


def test_Database_get_tables_empty():
    db = Database(':memory:', initialize=False)
    assert db.get_tables() == []


def test_Database_get_version():
    db = Database(':memory:')
    with db.connection as conn:
        conn.execute('INSERT INTO versions VALUES(1,"now")')
        conn.execute('INSERT INTO versions VALUES(2,"now")')
    assert db.get_version() == 2


def test_Database_get_version_none():
    db = Database(':memory:', initialize=False)
    assert db.get_version() is None


def test_Database_get_versions():
    db = Database(':memory:')
    with db.connection as conn:
        conn.execute('INSERT INTO versions VALUES(1,"now")')
        conn.execute('INSERT INTO versions VALUES(2,"now")')
    assert db.get_versions() == [1, 2]


def test_Database_get_versions_empty():
    db = Database(':memory:', initialize=False)
    assert db.get_versions() == []
