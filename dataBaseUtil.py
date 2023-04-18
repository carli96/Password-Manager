import pymongo
from pymongo.server_api import ServerApi

def connect():
    # Replace the following with your MongoDB Atlas cluster connection string
    # Don't forget to replace <username>, <password>, and <dbname> with your own values
    connection_string = "mongodb+srv://luis:QvcHEiYx59Svisag@passmanager.sixpzvi.mongodb.net/?retryWrites=true&w=majority"

    # Create a MongoClient object
    client = pymongo.MongoClient(connection_string, server_api=ServerApi('1'))

    # Access the database
    db = client.PassManager

    # Access a collection within the database
    collection = db.<collection-name>


def find():
    # Access the collection you want to search
    collection = db.<collection-name>

    # Search for all documents in the collection
    results = collection.find()

    # Iterate over the results and print each document
    for result in results:
        print(result)

def insert():
    # Create a document to insert
    document = {"name": "Jane Doe", "age": 30}

    # Insert the document into the collection
    result = collection.insert_one(document)

    # Print the ID of the inserted document
    print(result.inserted_id)

