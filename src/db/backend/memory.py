class Database:
    def __init__(self):
        self._tables = {}
        self._schemas = {}

    def create_table(self, name, fields):
        if name in self._tables:
            raise ValueError(f"Table {name} exists")
        self._schemas[name] = fields
        self._tables[name] = []

    def get_table_names(self):
        return list(self._tables.keys())

    def get_schema(self, name):
        return self._schemas.get(name, [])

    def insert(self, table, values):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        if len(values) != len(self._schemas[table]):
            raise ValueError("Wrong number of fields")
        rid = self._get_next_id(table)
        record = (rid,) + values
        self._tables[table].append(record)
        return record

    def _get_next_id(self, table):
        ids = [r[0] for r in self._tables[table]]
        return max(ids) + 1 if ids else 1

    def get_all(self, table):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        return self._tables[table].copy()

    def select(self, table, filters=None):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        result = self._tables[table].copy()
        if filters:
            for pos, val in filters.items():
                result = [r for r in result if r[pos] == val]
        return result

    def update(self, table, record_id, updates):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        for i, r in enumerate(self._tables[table]):
            if r[0] == record_id:
                new = list(r)
                for pos, val in updates.items():
                    new[pos] = val
                self._tables[table][i] = tuple(new)
                return self._tables[table][i]
        raise ValueError(f"Record {record_id} not found")

    def delete(self, table, record_id):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        for i, r in enumerate(self._tables[table]):
            if r[0] == record_id:
                return self._tables[table].pop(i)
        raise ValueError(f"Record {record_id} not found")