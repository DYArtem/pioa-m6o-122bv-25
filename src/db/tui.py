from .backend.memory import Database
from .backend.file_database import FileDatabase
from .backend.csv_database import CSVDatabase


class TUI:
    def __init__(self):
        print("1. In-memory")
        print("2. File (JSON)")
        print("3. File (CSV)")
        tp = input("Choice: ").strip()

        if tp == "2":
            self.db = FileDatabase("data.json")
            print("Using JSON database")
        elif tp == "3":
            self.db = CSVDatabase("data.csv")
            print("Using CSV database")
        else:
            self.db = Database()
            print("Using in-memory database")

        self.current = None
        self.fields = {}
        self._init_sample()

    def _init_sample(self):
        try:
            self.db.create_table("students")
            self.fields["students"] = ["name", "age"]
            self.db.create_record("students", ("name", "age"), ("Ivan", 20))
            self.db.create_record("students", ("name", "age"), ("Maria", 19))
            self.current = "students"
        except ValueError:
            pass

    def _print_menu(self):
        print(f"\n=== Table: {self.current or 'none'} ===")
        print("1. Create table")
        print("2. Select table")
        print("3. Add record")
        print("4. Show all")
        print("5. Find records")
        print("6. Update record")
        print("7. Delete record")
        print("0. Exit")

    def _read_int(self, p):
        while True:
            try:
                return int(input(p))
            except ValueError:
                print("Error: need number")

    def _read_opt_int(self, p):
        s = input(p).strip()
        if s == "":
            return None
        try:
            return int(s)
        except ValueError:
            print("Error: need number or empty")
            return None

    def _show(self, recs, flds):
        if not recs:
            print("No records")
            return
        print("\nid | " + " | ".join(flds))
        print("-" * 40)
        for r in recs:
            print(" | ".join(str(x) for x in r))

    def _create_table(self):
        name = input("Table name: ").strip()
        if not name:
            return
        flds = input("Fields (comma): ").strip()
        if not flds:
            return
        flds = [f.strip() for f in flds.split(",")]
        try:
            self.db.create_table(name)
            self.fields[name] = flds
            print(f"Table {name} created")
        except ValueError as e:
            print(f"Error: {e}")

    def _select_table(self):
        tables = self.db.get_table_names()
        if not tables:
            print("No tables")
            return
        print("Tables:", ", ".join(tables))
        name = input("Name: ").strip()
        if name in tables:
            self.current = name
            print(f"Switched to {name}")
        else:
            print("Not found")

    def _add_record(self):
        if not self.current:
            print("Select table first")
            return
        flds = self.fields.get(self.current, [])
        if not flds:
            return
        vals = []
        for f in flds:
            v = input(f"{f}: ").strip()
            if f == "age":
                try:
                    v = int(v)
                except ValueError:
                    print("Age must be number")
                    return
            vals.append(v)
        try:
            r = self.db.create_record(self.current, tuple(flds), tuple(vals))
            print(f"Added: {r}")
        except ValueError as e:
            print(f"Error: {e}")

    def _show_all(self):
        if not self.current:
            print("Select table first")
            return
        try:
            recs = self.db.get_all(self.current)
            flds = self.fields.get(self.current, [])
            self._show(recs, flds)
        except ValueError as e:
            print(f"Error: {e}")

    def _find(self):
        if not self.current:
            print("Select table first")
            return
        flds = self.fields.get(self.current, [])
        filt = {}
        for i, f in enumerate(flds, 1):
            v = input(f"{f} (Enter to skip): ").strip()
            if v:
                if f == "age":
                    try:
                        v = int(v)
                    except ValueError:
                        print("Age must be number")
                        return
                filt[i] = v
        try:
            recs = self.db.select_record(self.current, filt or None)
            self._show(recs, flds)
        except ValueError as e:
            print(f"Error: {e}")

    def _update(self):
        if not self.current:
            print("Select table first")
            return
        flds = self.fields.get(self.current, [])
        rid = self._read_int("Record ID: ")
        if rid is None:
            return
        upd = {}
        for i, f in enumerate(flds, 1):
            v = input(f"{f} (new, Enter to skip): ").strip()
            if v:
                if f == "age":
                    try:
                        v = int(v)
                    except ValueError:
                        print("Age must be number")
                        return
                upd[i] = v
        if not upd:
            return
        try:
            r = self.db.update_record(self.current, rid, upd)
            print(f"Updated: {r}")
        except ValueError as e:
            print(f"Error: {e}")

    def _delete(self):
        if not self.current:
            print("Select table first")
            return
        rid = self._read_int("Record ID: ")
        if rid is None:
            return
        try:
            r = self.db.delete_record(self.current, rid)
            print(f"Deleted: {r}")
        except ValueError as e:
            print(f"Error: {e}")

    def run(self):
        while True:
            self._print_menu()
            cmd = input("> ").strip()
            if cmd == "1":
                self._create_table()
            elif cmd == "2":
                self._select_table()
            elif cmd == "3":
                self._add_record()
            elif cmd == "4":
                self._show_all()
            elif cmd == "5":
                self._find()
            elif cmd == "6":
                self._update()
            elif cmd == "7":
                self._delete()
            elif cmd == "0":
                break
            else:
                print("Wrong command")