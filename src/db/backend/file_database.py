import json
import os

class FileDatabase:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self._tables = {}
        self._schemas = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self._tables = data.get("tables", {})
                self._schemas = data.get("schemas", {})
        except Exception:
            raise Exception("Error loading JSON database")

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump({
                "tables": self._tables,
                "schemas": self._schemas
            }, f, indent=4)

    def create_table(self, name, fields):
        if name in self._tables:
            raise ValueError(f"Table {name} exists")
        self._schemas[name] = fields
        self._tables[name] = []
        self._save()

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
        self._save()
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
                self._save()
                return self._tables[table][i]
        raise ValueError(f"Record {record_id} not found")

    def delete(self, table, record_id):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        for i, r in enumerate(self._tables[table]):
            if r[0] == record_id:
                deleted = self._tables[table].pop(i)
                self._save()
                return deleted
        raise ValueError(f"Record {record_id} not found")