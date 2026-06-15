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
        elif tp == "3":
            self.db = CSVDatabase("data.csv")
        else:
            self.db = Database()

        self.current_table = None

    def _print_menu(self):
        print(f"\n=== Current table: {self.current_table or 'none'} ===")
        print("1. Create table")
        print("2. Select table")
        print("3. Insert record")
        print("4. Show all")
        print("5. Select by filters")
        print("6. Update record")
        print("7. Delete record")
        print("0. Exit")

    def _read_int(self, p):
        while True:
            try:
                return int(input(p))
            except ValueError:
                print("Need number")
            except EOFError:
                print("\nExiting...")
                return 0

    def run(self):
        while True:
            try:
                self._print_menu()
                cmd = input("> ").strip()
                if cmd == "1":
                    name = input("Table name: ").strip()
                    fields = input("Fields (comma): ").strip()
                    fields = [f.strip() for f in fields.split(",")]
                    try:
                        self.db.create_table(name, fields)
                        print(f"Table {name} created")
                    except ValueError as e:
                        print(e)
                elif cmd == "2":
                    tables = self.db.get_table_names()
                    if not tables:
                        print("No tables")
                        continue
                    print("Tables:", ", ".join(tables))
                    name = input("Select: ").strip()
                    if name in tables:
                        self.current_table = name
                        print(f"Selected {name}")
                    else:
                        print("Not found")
                elif cmd == "3":
                    if not self.current_table:
                        print("No table selected")
                        continue
                    schema = self.db.get_schema(self.current_table)
                    values = []
                    for f in schema:
                        v = input(f"{f}: ").strip()
                        values.append(v)
                    try:
                        r = self.db.insert(self.current_table, tuple(values))
                        print(f"Inserted: {r}")
                    except ValueError as e:
                        print(e)
                elif cmd == "4":
                    if not self.current_table:
                        print("No table selected")
                        continue
                    for r in self.db.get_all(self.current_table):
                        print(r)
                elif cmd == "5":
                    if not self.current_table:
                        print("No table selected")
                        continue
                    schema = self.db.get_schema(self.current_table)
                    filters = {}
                    for f in schema:
                        v = input(f"{f} (enter to skip): ").strip()
                        if v:
                            filters[f] = v
                    try:
                        for r in self.db.select(self.current_table, filters):
                            print(r)
                    except ValueError as e:
                        print(e)
                elif cmd == "6":
                    if not self.current_table:
                        print("No table selected")
                        continue
                    rid = self._read_int("Record ID: ")
                    schema = self.db.get_schema(self.current_table)
                    updates = {}
                    for f in schema:
                        v = input(f"{f} (new, enter to skip): ").strip()
                        if v:
                            updates[f] = v
                    try:
                        self.db.update(self.current_table, rid, updates)
                        print("Updated")
                    except ValueError as e:
                        print(e)
                elif cmd == "7":
                    if not self.current_table:
                        print("No table selected")
                        continue
                    rid = self._read_int("Record ID: ")
                    try:
                        self.db.delete(self.current_table, rid)
                        print("Deleted")
                    except ValueError as e:
                        print(e)
                elif cmd == "0":
                    break
                else:
                    print("Wrong command")
            except EOFError:
                print("\nExiting...")
                break