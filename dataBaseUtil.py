import pymongo, base64
from pymongo.server_api import ServerApi


connection_string = "mongodb+srv://luis:Df66p3obwpropSEd@passmanager.sixpzvi.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient object
client = pymongo.MongoClient(connection_string)

# Access the database
db = client["PassManager"]

# Access a collection within the database
collection = db["Accounts"]


def searchByUserID(user_id):
    # Access the collection you want to search
    collection = db.Accounts
    result = []
    try: 
        # Search for documents that match the userID
        results = collection.find({"userID": user_id})
        #results = collection.find()
        for record in results:
            result.append(record)
    except:
        result = ["newUser"]
    
    return result

def insert(userID, web, EncryptedKey, HashedKey, IV):
    # Create a document to insert
    account = {"userID":userID, "EncryptedKey":EncryptedKey, "HashedKey":HashedKey, "IV": IV, "web": web}
    

    # Insert the document into the collection
    result = collection.insert_one(account)

    # Print the ID of the inserted document
    return str(result.inserted_id)
'''
if __name__ == '__main__':
    insert("accountPK", "userID","EncryptedKey", "HashedKey", "IV")
'''