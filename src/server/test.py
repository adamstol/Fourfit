from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
import os 
from dotenv import load_dotenv


load_dotenv()
dbpass = os.getenv('DB_PASSWORD')
# create a client
# add db pass
uri = f"mongodb+srv://hackdeeznuts:{dbpass}@htv9mongo.tylcf.mongodb.net/?retryWrites=true&w=majority&appName=htv9mongo"
print(uri)
client = MongoClient(uri, server_api=ServerApi('1')) #iainteverseen dis kinda connect before but change if u want i j need the pass @dvir

# select the database and collection
db = client['htv9db']
collection = db['clothes']

# testing getting kyle object
result = collection.find_one({'item_name': 'kyle'})

if result:
    print(result)  # prints the document
    
else:
    print("No document found")


# use mongo to give frontend image s3 links to display
# how are we selecting specific clothing with certain tags (we have weight scores but how are we using those to choose from the db)
# idk brainstorming wat we doing w mongo so i can make links tai shi