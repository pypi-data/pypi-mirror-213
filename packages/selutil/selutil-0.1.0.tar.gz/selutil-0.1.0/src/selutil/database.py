"""Commonly used database functionality."""

import importlib.util
import pathlib
import sqlite3
import sys
from typing import List, Union

from .time import get_timestamp


def get_tables(connection: sqlite3.Connection) -> List[str]:
    """Return the list of tables in the database.

    Args:
        connection: An open connection to a database.

    Returns:
        A list of table names, or an empty list if there are no tables.
    """
    with connection as conn:
        result = conn.execute(
            'SELECT name FROM sqlite_master WHERE type="table"')
    all_tables = result.fetchall()
    return [a[0] for a in all_tables]


class Database(object):
    """Manage a database connection and provide common functionality.

    Attributes:
        connection: An open connection to the database
        path: The path to the file containing the database

    """

    connection: sqlite3.Connection
    path: pathlib.Path

    def __init__(self,
                 path: Union[pathlib.Path, str],
                 initialize: bool = True):
        """Initialize the database

        Args:
            path: The path to the file containing the database
            initialize: If True then add a "versions" table to the database
        """
        self.path = pathlib.Path(path)
        self.connection = sqlite3.connect(str(self.path))
        self.connection.execute('PRAGMA foreign_keys = 1')
        self.connection.row_factory = sqlite3.Row

        if initialize:
            print(self.get_version())
            if self.get_version() is None:
                self._initialize()

    def __del__(self):
        self.connection.close()

    def _initialize(self):
        with self.connection as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS versions ('
                         '    version_id INTEGER PRIMARY KEY,'
                         '    timestamp TEXT'
                         ')')

    def apply_migrations(self, migrations_directory: Union[pathlib.Path, str]):
        """Apply all the migrations that exist in the supplied directory.

        Migrations are assumed to be named "migration_XX_YYYYYY.py" where
        "XX" is replaced with an integer and "YYYYYY" can be replaced with
        an arbitrary string.  Each migration module should have a method
        called "migrate" with the following signature:

            migrate(connection: sqlite3.Connection,
                    current_migrations: list[int] | None)

        Args:
            migrations_directory: The path to a directory containing migration
                modules.  The directory need not be a package.
        """
        module_paths = pathlib.Path(migrations_directory).glob('*.py')
        for migration_path in sorted(module_paths):
            migration = migration_path.with_suffix('').name
            migration_id = int(migration.split('_')[1])
            finished_migrations = self.get_versions()
            if migration_id in finished_migrations:
                continue
            spec = importlib.util.spec_from_file_location(
                migration, migration_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[migration] = module
            spec.loader.exec_module(module)
            if not hasattr(module, 'migrate'):
                continue
            migrate = getattr(module, 'migrate')
            timestamp = get_timestamp()
            with self.connection as conn:
                migrate(conn, current_migrations=finished_migrations)
                conn.execute('INSERT INTO versions VALUES (?,?)',
                             (migration_id, timestamp))

    def get_tables(self) -> List[str]:
        """Return a list containing the names of all tables in the database."""
        return get_tables(self.connection)

    def get_version(self) -> Union[int, None]:
        """Return the integer id of the last migration applied, or None if
        there have been no migrations."""
        all_versions = self.get_versions()
        if not all_versions:
            return None
        else:
            return all_versions[-1]

    def get_versions(self) -> List[int]:
        """Return a list of integer ids of the migrations applied."""
        all_versions = []
        try:
            with self.connection as conn:
                result = conn.execute('SELECT * FROM versions')
        except sqlite3.OperationalError:
            return []
        else:
            all_versions = result.fetchall()
            all_versions.sort(key=lambda a: a['version_id'])
            if not all_versions:
                return []
            else:
                return [a['version_id'] for a in all_versions]
