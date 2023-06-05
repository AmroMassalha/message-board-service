class QueryBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._query = ""

    def select_all(self, table):
        self._query += f"SELECT * FROM {table}"
        return self.build()

    def select_where(self, table, conditions):
        condition_str = ' AND '.join([f"{key} = '{value}'" for key, value in conditions.items()])
        self._query += f"SELECT * FROM {table} WHERE {condition_str}"
        return self.build()

    def insert(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{value}'" for value in data.values()])
        self._query += f"INSERT INTO {table} ({columns}) VALUES ({values})"
        return self.build()

    def delete(self, table, conditions):
        condition_str = ' AND '.join([f"{key} = '{value}'" for key, value in conditions.items()])
        self._query += f"DELETE FROM {table} WHERE {condition_str}"
        return self.build()

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
