import pymongo
from bson.objectid import ObjectId

connection_string = "mongodb+srv://luis:Df66p3obwpropSEd@passmanager.sixpzvi.mongodb.net/?retryWrites=true&w=majority"
# Create a MongoClient object
client = pymongo.MongoClient(connection_string)
# Access the database
db = client["PassManager"]
# Access a collection within the database
collection = db["Accounts"]


# Searchs all the accounts from a user
def searchByUserID(user_id):
    # Access the collection you want to search
    collection = db.Accounts
    result = []
    try: 
        # Search for documents that match the userID
        results = collection.find({"userID": user_id})
        for record in results:
            result.append(record)
    except:
        result = ["newUser"]
    
    return result

#Inserts an element into the DB
def insert(userID, web, EncryptedKey, HashedKey, IV):
    # Create a document to insert
    account = {"userID":userID, "EncryptedKey":EncryptedKey, "HashedKey":HashedKey, "IV": IV, "web": web}

    # Insert the document into the collection
    result = collection.insert_one(account)

    # Print the ID of the inserted document
    return str(result.inserted_id)

# removes the element where id == _id
def remove(id):
    collection.delete_one({"_id": ObjectId(id)})

'''# WARNING, REMOVES ALL THE DB, FOR DEVELOPING PURPOSES
def clearDB():
    collection.delete_many({})

def main():
    clearDB()

if __name__ == "__main__":
    main()'''