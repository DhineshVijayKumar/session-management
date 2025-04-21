class DatabaseNotFoundError(Exception):
    pass

class CollectionNotFoundError(Exception):
    pass

class DocumentNotFoundError(Exception):
    pass

class MongoOperationError(Exception):
    pass