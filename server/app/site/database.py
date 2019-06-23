import os

from app.tables import TABLES

import rethinkdb


class RethinkDB:
    def __init__(self):
        self.host = os.environ.get("RETHINKDB_HOST", "127.0.0.1")
        self.port = os.environ.get("RETHINKDB_PORT", "28015")
        self.database = os.environ.get("RETHINKDB_DATABASE", "slangeuib")

        self.conn = None
        rethinkdb.set_loop_type("gevent")

        with self.get_connection() as self.conn:
            try:
                rethinkdb.db_create(self.database).run(self.conn)
                print("Database created")
            except rethinkdb.RqlRuntimeError:
                print("Database found")

    def create_tables(self):
        created = []

        for table, obj in TABLES.items():
            if self.create_table(table, obj.primary_key):
                created.append(table)

        return created

    def get_connection(self, connection_database=True):
        """
        Grab a connection to the RethinkDb server
        """
        if connection_database:
            return rethinkdb.connect(
                host=self.host, port=self.port, 
                db=self.database
            )
        else:
            return rethinkdb.connect(
                host=self.host, port=self.port
            )

    def create_table(
                     self,
                     table_name: str,
                     primary_key: str = "id",
                     durability: str = "hard",
                     shards: int = 1,
                     replicas=1,
                     primary_replica_tab=None) -> bool:

        with self.get_connection() as conn:
            all_tables = rethinkdb.db(self.database).table_list().run(conn)

            if table_name in all_tables:
                return False

            kwargs = {
                "primary_key": primary_key,
                "durability": durability,
                "shards": shards,
                "replicas": replicas
            }

            if primary_replica_tab is not None:
                kwargs["primary_replica_tab"] = primary_replica_tab

            rethinkdb.db(self.database).table_create(
                table_name, **kwargs
            ).run(conn)

            return True

    def delete(
                self,
                table_name: str,
                primary_key=None,
                durability="hard",
                return_changes=False) -> dict:

        if primary_key:
            query = self.query(table_name).get(primary_key).delete(
                durability=durability, return_changes=return_changes
            )
        else:
            query = self.query(table_name).delete(
                durability=durability, return_changes=return_changes
            )

        if return_changes:
            return self.run(query, coerce=dict)
        self.run(query)

    def drop_table(self, table_name):
        with self.get_connection() as conn:
            all_tables = rethinkdb.db(self.database).table_list().run(conn)

            if table_name not in all_tables:
                return False

            rethinkdb.db(self.database).table_drop(table_name).run(conn)
            return True

    def query(self, table_name):
        if table_name not in TABLES:
            print(f"Table not declared in TABLES {table_name}")

        return rethinkdb.table(table_name)

    def run(self, query, *, new_connection=False,
            connect_database=True, coerce=None):

        if not new_connection:
            try:
                result = query.run(self.conn)
            except rethinkdb.errors.ReqlDriverError as e:
                if e.args[0] == "Connection is closed.":
                    result = query.run(self.get_connection(connect_database))
                else:
                    raise

        else:
            result = query(self.get_connection(connect_database))

        if coerce:
            return coerce(result) if result else coerce()
        return result

    def filter(self, table_name, predicate, default=False):
        return self.run(
            self.query(table_name).filter(predicate, default=default),
            coerce=list
        )

    def get(self, table_name, key):
        result = self.run(
            self.query(table_name).get(key)
        )

        return dict(result) if result else None

    def get_all(self, table_name, *keys, index="id"):
        if keys:
            return self.run(
                self.query(table_name).get_all(*keys, index=index),
                coerce=list
            )
        else:
            return self.run(
                self.query(table_name),
                coerce=list
            )

    def insert(
               self,
               table_name,
               *objects,
               durability="hard",
               return_changes=False,
               conflict="error"):

        query = self.query(table_name).insert(
            objects, durability=durability,
            return_changes=return_changes, conflict=conflict
        )

        return self.run(query, coerce=dict)

    def map(self, table_name, func):
        return self.run(
            self.query(table_name).map(func),
            coerce=list
        )
