import csv
import os

class CSVDatabase:
    def __init__(self, filename="data.csv"):
        self.filename = filename
        self._tables = {}
        self._schemas = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows:
                    self._schemas = eval(rows[0][0])
                    self._tables = eval(rows[0][1])
        except Exception:
            raise Exception("Error loading CSV database")

    def _save(self):
        with open(self.filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(self._schemas), str(self._tables)])

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