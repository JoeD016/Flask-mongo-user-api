import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def getUsers():
    """
    Return an overview of users.
    """
    userNames = []
    cursor = db.users.find({})
    for user in cursor:
        userNames.append(user['name'])
    return userNames

def get_users_by_name(name):
    """
    Given a user name, return a list of user profile data with that name.
    """
    try:
        cursor = db.users.find({"name": name})
        return cursor
    # TODO: Error Handling
    # If an invalid user name is passed to `get_usesr_by_name`, it should return None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}

def get_user_by_email(email):
    """
    Given a user email, return a user profile associated with that email.
    """
    try:

        pipeline = [
            {
                "$match": {
                    "email": email
                }
            }
        ]

        user = db.users.aggregate(pipeline).next()
        return user

    # TODO: Error Handling
    # If an invalid ID is passed to `get_user`, it should return None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}

def add_user(name, email, password):
    """
    Add a new user into the users collection, with the following fields:

    - "name"
    - "email"
    - "password"

    Name and email must be retrieved from the "user" object.
    """
    
    user_doc = { 'name' : name, 'email' : email,'password' : password}
    return db.users.insert_one(user_doc)

def get_user(id):
    """
    Given a user's id, return a user profile data with that id.
    """
    try:

        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            }
        ]

        user = db.users.aggregate(pipeline).next()
        return user

    # TODO: Error Handling
    # If an invalid ID is passed to `get_user`, it should return None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}

def delete_user(email):
    """
    Given a user's email deletes that user from collection
    """

    response = db.users.delete_one( { "email": email } )
    return response

def update_user(user_email, new_password):
    """
    Updates the user password in the users collection.
    """
    response = db.users.update_one(
        { "email": user_email },
        { "$set": { "password": new_password} }
    )

    return response
