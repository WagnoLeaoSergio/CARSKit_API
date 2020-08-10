import pickledb

class Database(object):
    def __init__(self, db_path="": str):
        self.database_path = db_path
        self.database_obj = None
    
    # Futuramente pode ser trocado por self.connect_database()
    def load_database(self) -> bool:
        self.database_obj = pickledb.load(self.database_path, True)
        if self.database_obj:
            return True
        return False

    def create(self, query: str) -> bool:
        return self.database_obj.set(query, None)

    def read(self, query: str) -> bool:
        return self.database_obj.get(query)

    def update(self, query: str, value: any) -> bool:
        return self.database_obj.set(query, value)

    def delete(self, query: str) -> bool:
        return self.database_obj.rem(query)

    def save(self) -> bool:
        return self.database_obj.dump()

    def exists(self, query: str) -> bool:
        return self.database_obj.exists(query)

    # def disconnect(self)

