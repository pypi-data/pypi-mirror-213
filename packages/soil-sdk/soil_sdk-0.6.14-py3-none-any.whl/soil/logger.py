""" Exports the soil logger """
import logging
import logging.handlers
from typing import cast, LiteralString
from os.path import exists
import sqlite3

from soil.types import TypeLog

_SOIL_LOGGER = "soil_logger"
PROCESSED_FILES_DB = "/rain-data/processed_files.db"

logger = logging.getLogger(_SOIL_LOGGER)  # pylint: disable=invalid-name


def logger_extra_kwarg(*, type_log: TypeLog, file_name: str) -> dict[str, str]:
    """Creates the extra kwarg for the logger."""
    return {
        HashFileHandler.type_log: type_log.value,
        HashFileHandler.hashfile: file_name,
    }


class HashFileHandler(logging.StreamHandler):
    """Handler of logs to store file to sqlite."""

    type_log = "type"
    hashfile = "file"
    state_name_column = "state_description"
    message_column = "message"

    def emit(self, record: logging.LogRecord) -> None:
        type_log = cast(TypeLog | None, getattr(record, "type", None))
        hashfile = cast(str | None, getattr(record, "file", None))
        if (
            type_log is not None
            and hashfile is not None
            and type_log in [*TypeLog]
            and exists(PROCESSED_FILES_DB)
        ):
            self._process_file_in_storage(
                hashfile=hashfile, type_log=type_log, message=record.getMessage()
            )

    def _process_file_in_storage(self, **kwargs) -> None:
        """Process the file hash to update the DB."""
        with sqlite3.connect(PROCESSED_FILES_DB) as connection:
            cursor = connection.cursor()
            # pylint:disable=use-maxsplit-arg
            table_name = PROCESSED_FILES_DB.split("/")[-1].split(".", maxsplit=1)[0]
            self._alter_table_if_necessary(cursor=cursor, table_name=table_name)
            self._update_hashfile(cursor=cursor, table_name=table_name, **kwargs)

    def _update_hashfile(
        self,
        *,
        cursor: sqlite3.Cursor,
        table_name: LiteralString,
        hashfile: str,
        type_log: TypeLog,
        message: str,
    ) -> None:
        cursor.execute(
            f"UPDATE {table_name} "
            f"SET {self.state_name_column} = ?, {self.message_column} = ? WHERE file_name = ?"
            f" and ({self.state_name_column} IS NULL or {self.state_name_column} = ?)",
            (type_log, message, hashfile, TypeLog.NOT_PROCESSED.value),
        )

    def _alter_table_if_necessary(
        self, *, cursor: sqlite3.Cursor, table_name: LiteralString
    ) -> None:
        pragmas = cursor.execute(f"PRAGMA table_info({table_name});")
        columns: list[str] = [n for _, n, *_ in pragmas.fetchall()]
        if self.state_name_column not in columns:
            # sqlite current version does not support adding checks on existing tables.
            cursor.execute(
                f"ALTER TABLE {table_name}"
                f"\n\tADD COLUMN {self.state_name_column} VARCHAR;"
            )
        if self.message_column not in columns:
            cursor.execute(
                f"ALTER TABLE {table_name}"
                f"\n\tADD COLUMN {self.message_column} VARCHAR;"
            )


logger.addHandler(HashFileHandler())
