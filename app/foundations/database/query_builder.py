class QueryBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._query = ""

    def select(self, table, columns="*"):
        self._query += f"SELECT {columns} FROM {table} "
        return self

    def where(self, condition):
        self._query += f"WHERE {condition} "
        return self

    def insert_into(self, table, columns, values):
        self._query += f"INSERT INTO {table} ({columns}) VALUES ({values}) "
        return self

    def update(self, table):
        self._query += f"UPDATE {table} "
        return self

    def set(self, values):
        self._query += f"SET {values} "
        return self

    def delete_from(self, table):
        self._query += f"DELETE FROM {table} "
        return self

    def build(self):
        result = self._query
        self.reset()
        return result
