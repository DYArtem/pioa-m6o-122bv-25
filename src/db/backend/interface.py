from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def create_table(self, name, fields):
        pass

    @abstractmethod
    def get_table_names(self):
        pass

    @abstractmethod
    def get_schema(self, name):
        pass

    @abstractmethod
    def insert(self, table, values):
        pass

    @abstractmethod
    def get_all(self, table):
        pass

    @abstractmethod
    def select(self, table, filters=None):
        pass

    @abstractmethod
    def update(self, table, record_id, updates):
        pass

    @abstractmethod
    def delete(self, table, record_id):
        pass