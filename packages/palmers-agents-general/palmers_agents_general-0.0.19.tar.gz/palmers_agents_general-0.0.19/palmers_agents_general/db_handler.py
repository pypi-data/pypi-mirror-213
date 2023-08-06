import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


class PostgresHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def read_sql_query(self, query, params=None):
        df = pd.read_sql_query(query, self.conn, params=params)
        return df

    def execute_update(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def insert_records(self, table_name, records):
        columns = records[0].keys()
        values = [tuple(record.values()) for record in records]

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(records))
        )

        self.execute_update(insert_query, values)

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
