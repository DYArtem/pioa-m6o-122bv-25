import csv
import os
from .interface import DatabaseInterface

class CSVDatabase(DatabaseInterface):
    def __init__(self, filename="data.csv"):
        self.filename = filename
        self._tables = {}
        self._schemas = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows:
                    self._schemas = eval(rows[0][0])
                    self._tables = {}
                    for row in rows[1:]:
                        table_name = row[0]
                        record = eval(row[1])
                        if table_name not in self._tables:
                            self._tables[table_name] = []
                        self._tables[table_name].append(tuple(record))
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")

    def _save(self):
        with open(self.filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(self._schemas)])
            for table_name, records in self._tables.items():
                for record in records:
                    writer.writerow([table_name, list(record)])

    def create_table(self, name, fields):
        if name in self._tables:
            raise ValueError(f"Table {name} already exists")
        self._schemas[name] = fields
        self._tables[name] = []
        self._save()

    def get_table_names(self):
        return list(self._tables.keys())

    def get_schema(self, name):
        return self._schemas.get(name, [])

    def _get_next_id(self, table):
        ids = [r[0] for r in self._tables[table]]
        return max(ids) + 1 if ids else 1

    def insert(self, table, values):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        expected = len(self._schemas[table])
        if len(values) != expected:
            raise ValueError(f"Expected {expected} fields, got {len(values)}")
        rid = self._get_next_id(table)
        record = (rid,) + values
        self._tables[table].append(record)
        self._save()
        return record

    def get_all(self, table):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        return self._tables[table].copy()

    def select(self, table, filters=None):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        schema = self._schemas[table]
        result = self._tables[table].copy()
        if filters:
            for field, value in filters.items():
                if field not in schema:
                    raise ValueError(f"Unknown field {field}")
                pos = schema.index(field) + 1
                result = [r for r in result if r[pos] == value]
        return result

    def update(self, table, record_id, updates):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        schema = self._schemas[table]
        for i, r in enumerate(self._tables[table]):
            if r[0] == record_id:
                new = list(r)
                for field, value in updates.items():
                    if field not in schema:
                        raise ValueError(f"Unknown field {field}")
                    pos = schema.index(field) + 1
                    new[pos] = value
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