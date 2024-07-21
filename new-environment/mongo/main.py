import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)

# Create a database
db = client.testdb

# Create a collection
collection = db.test_collection

cars = db.cars

cars.create_index([('user_id', pymongo.ASCENDING)])
cars.insert_one({'id': 'Audi', 'name': 'Audi'})

# Insert a document
collection.create_index([('name', pymongo.ASCENDING)])
collection.insert_one({'name': 'John Doe'})

# find foreign key

carname = cars.find_one({'id': 'Audi'})['name']

# Update a document
collection.update_one({'name': 'John Doe'}, {'$set': {'name': 'Jane Doe', 'age': 50, 'cars': ['Audi', 'BMW', 'Chevrolet']}})

# Insert a document with a foreign key
print(collection.find_one({'cars': carname}))


# Find a document
# print(collection.find_one({'name': 'Jane Doe'}))

# Delete a document
collection.delete_one({'name': 'Jane Doe'})

# show databases
# print(client.list_database_names())
