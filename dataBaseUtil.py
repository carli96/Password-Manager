import pymongo
from pymongo.server_api import ServerApi


connection_string = "mongodb+srv://luis:QvcHEiYx59Svisag@passmanager.sixpzvi.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient object
client = pymongo.MongoClient(connection_string, server_api=ServerApi('1'))

# Access the database
db = client.PassManager

# Access a collection within the database
collection = db.Accounts


def find():
    # Access the collection you want to search
    collection = db.Accounts

    # Search for all documents in the collection
    results = collection.find()

    # Iterate over the results and print each document
    for result in results:
        print(result)

def searchByUserID(user_id):
    # Access the collection you want to search
    collection = db.Accounts

    # Search for documents that match the userID
    results = collection.find({"userID": user_id})

    # Iterate over the results and print each document
    for result in results:
        print(result)

def insert(accountPK, userID,EncryptedKey, HashedKey, IV):
    # Create a document to insert
    account = {"accountPK":accountPK, "userID":userID, "EncryptedKey":EncryptedKey, "HashedKey":HashedKey, "IV": IV}

    # Insert the document into the collection
    result = collection.insert_one(account)

    # Print the ID of the inserted document
    print(result.inserted_id)

if __name__ == '__main__':
    insert("accountPK", "userID","EncryptedKey", "HashedKey", "IV")
