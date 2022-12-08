import datetime   # This will be needed later
import os
import bson

from dotenv import load_dotenv
from pymongo import MongoClient

# Import the `pprint` function to print nested data:
from pprint import pprint

# Load config from a .env file:
load_dotenv()
MONGO_URI = os.environ['MONGO_URI']

# Connect to your MongoDB cluster:
client = MongoClient(MONGO_URI)

db = client['sample_mflix']

# List all the databases in the cluster:

collections = db.list_collection_names()
# for collection in collections:
#    print(collection)



# Get a reference to the 'movies' collection:
movies = db['movies']

# Get the document with the title 'Blacksmith Scene':
# pprint(movies.find_one({'title': 'Blacksmith Scene'}))

# Insert a document for the movie 'Parasite':
insert_result = movies.insert_one({
      "title": "Parasite",
      "year": 2020,
      "plot": "A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks. "
      "But their easy life gets complicated when their deception is threatened with exposure.",
      "released": datetime.datetime(2020, 2, 7, 0, 0, 0),
   })

# Save the inserted_id of the document you just created:
parasite_id = insert_result.inserted_id
# print("_id of inserted document: {parasite_id}".format(parasite_id=parasite_id))



# Look up the document you just created in the collection:
# print(movies.find_one({'_id': bson.ObjectId(parasite_id)}))

# for doc in movies.find({
#    'year': {
#       '$lt': 1920
#    }, 
#    'genres': 'Romance'
# }):
#     pprint(doc)

# Update the document with the correct year:
update_result = movies.update_many({ '_id': parasite_id }, {
   '$set': {"year": 2019}
})

# Print out the updated record to make sure it's correct:
pprint(movies.find_one({'_id': bson.ObjectId(parasite_id)}))

# movies.delete_many(
#    {"title": "Parasite",}
# )