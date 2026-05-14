import csv
import os

class CSVDatabase:
    def __init__(self, filename="data.csv"):
        self.filename = filename
        self._tables = {}
        self._next_ids = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows:
                self._tables = eval(rows[0][0])
                self._next_ids = eval(rows[0][1])

    def _save(self):
        with open(self.filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(self._tables), str(self._next_ids)])

    def create_table(self, name):
        if name in self._tables:
            raise ValueError(f"Table {name} exists")
        self._tables[name] = []
        self._next_ids[name] = 1
        self._save()

    def get_table_names(self):
        return list(self._tables.keys())

    def _get_next_id(self, name):
        cur = self._next_ids.get(name, 1)
        self._next_ids[name] = cur + 1
        return cur

    def create_record(self, table, fields, values):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        if len(fields) != len(values):
            raise ValueError("Fields and values count mismatch")
        rid = self._get_next_id(table)
        rec = (rid,) + values
        self._tables[table].append(rec)
        self._save()
        return rec

    def get_all(self, table):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        return self._tables[table].copy()

    def select_record(self, table, filters=None):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        res = self._tables[table].copy()
        if filters:
            for pos, val in filters.items():
                res = [r for r in res if r[pos] == val]
        return res

    def update_record(self, table, rid, updates):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        for i, rec in enumerate(self._tables[table]):
            if rec[0] == rid:
                new = list(rec)
                for pos, val in updates.items():
                    new[pos] = val
                upd = tuple(new)
                self._tables[table][i] = upd
                self._save()
                return upd
        raise ValueError(f"Record {rid} not found")

    def delete_record(self, table, rid):
        if table not in self._tables:
            raise ValueError(f"Table {table} not found")
        for i, rec in enumerate(self._tables[table]):
            if rec[0] == rid:
                deleted = self._tables[table].pop(i)
                self._save()
                return deleted
        raise ValueError(f"Record {rid} not found")