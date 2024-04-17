import json

from pymongo import MongoClient


class CrudAutomatisation:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def import_data(self, data):
        self.collection.insert_many(data)

    def insert(self, data):
        self.collection.insert_one(data)

    def read(self, query):
        return self.collection.find(query)

    def update(self, query, data, many=True):
        if many:
            self.collection.update_many(query, data)
        else:
            self.collection.update_one(query, data)

    def delete(self, query):
        self.collection.delete_one(query)

    def close_connection(self):
        self.client.close()


# Usage example
def main():
    # Initialize the CRUD automatisation class
    crud = CrudAutomatisation('db_auto', 'users')

    # Import data from users.json
    with open("./users.json", "r") as f:
        data = json.load(f)
        crud.import_data(data)

    # Query all users with age greater than or equal to 30
    query = {"age": {"$gte": 30}}
    for user in crud.read(query):
        print(user)

    # Update the age of all users by adding 5
    query = {}
    data = {"$inc": {"age": 5}}
    crud.update(query, data)

    # Insert a new user
    data = {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "createdAt": "2021-01-01T00:00:00"
    }
    crud.insert(data)

    # Delete the newly inserted user
    query = {"name": "John Doe"}
    crud.delete(query)

    # Close the connection
    crud.close_connection()


if __name__ == '__main__':
    main()
