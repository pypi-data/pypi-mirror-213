import sqlite3

import mysql.connector
from loguru import logger


class SQLite:
    def __init__(
        self,
        path: str
    ):
        """
        SQLite3 database connection class.

        - `path` str\n
            - e.g., `'/home/user/database.db'`
        - `database` str\n
            - e.g., `'config'`
        """
        try:
            self.db = sqlite3.connect(path, check_same_thread=False)
            self.cur = self.db.cursor()
            logger.info(f'Connected to SQLite3 database via "{path}"')
        except Exception as err:
            logger.error(f'SQLite3 database connection failed: {err}')
            quit()

    def query(self, SQL):
        try:
            logger.debug(f'SQL query: {SQL}')
            self.cur.execute(str(SQL))
            return self.cur.fetchall()
        except Exception as err:
            logger.error(f'Query error: {err}')
            self.db.close()
            quit()

    def exec(self, SQL):
        try:
            logger.debug(f'SQL query: {SQL}')
            self.cur.execute(str(SQL))
            self.db.commit()
            return self.cur.rowcount
        except Exception as err:
            logger.error(f'Query error: {err}')
            self.db.rollback()
            self.db.close()
            quit()


class MySQL:
    def __init__(
        self,
        user: str,
        password: str,
        database: str,
        host: str = '127.0.0.1',
        port: int = 3306,
        unix_socket: str = False
    ) -> None:
        """
        MySQL database connection class.

        If `unix_socket` is passed, the connection will be made via unix socket. Else, the connection will be made via TCP/IP.

        - `user` str\n
        - `password` str\n
        - `database` str\n
        - *`host` str: `'127.0.0.1'`\n
            - e.g., `'localhost'` or `'127.0.0.1'`
        - *`port` int: `3306`\n
            - Database port
        - *`unix_socket` str: `False`\n
            - e.g., `'/home/mysql/mysql.sock'`
        """
        if unix_socket:
            self.db = mysql.connector.connect(
                user=user,
                password=password,
                database=database,
                unix_socket=unix_socket
            )
            self.db_addr = unix_socket
        else:
            self.db = mysql.connector.connect(
                user=user,
                password=password,
                database=database,
                host=host,
                port=port
            )
            self.db_addr = f"{host}:{port}"
        if self.db.is_connected():
            self.cur = self.db.cursor()
            logger.info(f'Connected to MySQL database via "{self.db_addr}"')
        else:
            logger.error('MySQL database connection failed')
            quit()

    def reconnect(self) -> None:
        self.db.reconnect()
        if self.db.is_connected():
            logger.success(f'Re-connected to database via "{self.db_addr}"')
        else:
            logger.error('Database re-connection failed')
            self.db.close()
            quit()

    def query(self, SQL):
        try:
            logger.debug(f'SQL query: {SQL}')
            self.cur.execute(str(SQL))
            return self.cur.fetchall()
        except mysql.connector.errors.OperationalError as err:
            if err.errno == mysql.connector.errorcode.CR_SERVER_LOST:
                logger.warning('Connection to database lost, reconnecting...')
                self.reconnect()
                self.query(str(SQL))
            else:
                logger.error(f'Other OperationalError: {err}')
                self.db.close()
                quit()

    def exec(self, SQL):
        try:
            logger.debug(f'SQL exec: {SQL}')
            self.cur.execute(str(SQL))
            self.db.commit()
            return self.cur.rowcount
        except mysql.connector.errors.OperationalError as err:
            if err.errno == mysql.connector.errorcode.CR_SERVER_LOST:
                logger.warning('Connection to database lost, reconnecting...')
                self.reconnect()
                self.exec(str(SQL))
            else:
                logger.error(f'Other OperationalError: {err}')
                self.db.rollback()
                self.db.close()
                quit()
