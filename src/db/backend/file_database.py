import json
import os

class FileDatabase:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self._tables = {}
        self._next_ids = {}
        self._indexes = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self._tables = data.get("tables", {})
            self._next_ids = data.get("next_ids", {})
            self._indexes = data.get("indexes", {})

    def _save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump({
                "tables": self._tables,
                "next_ids": self._next_ids,
                "indexes": self._indexes
            }, f, ensure_ascii=False, indent=4)

    def create_index(self, table_name, field_name, field_pos):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        if table_name not in self._indexes:
            self._indexes[table_name] = {}
        idx = {}
        for record in self._tables[table_name]:
            key = record[field_pos]
            if key not in idx:
                idx[key] = []
            idx[key].append(record[0])
        self._indexes[table_name][field_name] = {"pos": field_pos, "data": idx}
        self._save()

    def select_with_index(self, table_name, field_name, value):
        if table_name not in self._indexes:
            return None
        if field_name not in self._indexes[table_name]:
            return None
        idx = self._indexes[table_name][field_name]
        pos = idx["pos"]
        ids = idx["data"].get(value, [])
        result = []
        for record in self._tables[table_name]:
            if record[0] in ids:
                result.append(record)
        return result

    def create_table(self, table_name):
        if table_name in self._tables:
            raise ValueError(f"Table {table_name} already exists")
        self._tables[table_name] = []
        self._next_ids[table_name] = 1
        self._save()

    def get_table_names(self):
        return list(self._tables.keys())

    def _get_next_id(self, table_name):
        current = self._next_ids.get(table_name, 1)
        self._next_ids[table_name] = current + 1
        return current

    def create_record(self, table_name, fields, values):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        if len(fields) != len(values):
            raise ValueError("Fields count does not match values count")
        record_id = self._get_next_id(table_name)
        record = (record_id,) + values
        self._tables[table_name].append(record)
        for idx_name, idx_data in self._indexes.get(table_name, {}).items():
            pos = idx_data["pos"]
            key = record[pos]
            if key not in idx_data["data"]:
                idx_data["data"][key] = []
            idx_data["data"][key].append(record_id)
        self._save()
        return record

    def get_all(self, table_name):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        return self._tables[table_name].copy()

    def select_record(self, table_name, filters=None):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        result = self._tables[table_name].copy()
        if filters:
            for pos, value in filters.items():
                result = [r for r in result if r[pos] == value]
        return result

    def update_record(self, table_name, record_id, updates):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        for i, record in enumerate(self._tables[table_name]):
            if record[0] == record_id:
                new_record = list(record)
                for pos, value in updates.items():
                    new_record[pos] = value
                updated = tuple(new_record)
                self._tables[table_name][i] = updated
                for idx_name, idx_data in self._indexes.get(table_name, {}).items():
                    pos = idx_data["pos"]
                    old_key = record[pos]
                    new_key = updated[pos]
                    if old_key != new_key:
                        idx_data["data"][old_key].remove(record_id)
                        if not idx_data["data"][old_key]:
                            del idx_data["data"][old_key]
                        if new_key not in idx_data["data"]:
                            idx_data["data"][new_key] = []
                        idx_data["data"][new_key].append(record_id)
                self._save()
                return updated
        raise ValueError(f"Record {record_id} not found in {table_name}")

    def delete_record(self, table_name, record_id):
        if table_name not in self._tables:
            raise ValueError(f"Table {table_name} not found")
        for i, record in enumerate(self._tables[table_name]):
            if record[0] == record_id:
                deleted = self._tables[table_name].pop(i)
                for idx_name, idx_data in self._indexes.get(table_name, {}).items():
                    pos = idx_data["pos"]
                    key = record[pos]
                    if key in idx_data["data"]:
                        idx_data["data"][key].remove(record_id)
                        if not idx_data["data"][key]:
                            del idx_data["data"][key]
                self._save()
                return deleted
        raise ValueError(f"Record {record_id} not found in {table_name}")