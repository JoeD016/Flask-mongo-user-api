import os

from flask import Flask, jsonify, request
from flaskr.db import getUsers, get_users_by_name, add_user, get_user, delete_user, update_user, get_user_by_email
from dotenv import load_dotenv


def create_app(test_config=None):
    load_dotenv()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI= os.environ['MONGO_URI']
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/', methods=['GET'])
    def api_get_users():
        names = getUsers()
        size = len(names)

        return {
            "size": size,
            "names": names
        }
    
    @app.route('/user/search/<name>', methods=['GET'])
    def api_get_users_by_name(name):
        cursor = get_users_by_name(name)
        users = []
        for user in cursor:
            print(user['name'])
            users.append({
            "name": user['name'],
            "email": user['email'],
            "password": user['password']
        })
        print(users)
        return jsonify(users)
    
    @app.route('/user/<email>', methods=['GET'])
    def api_get_user_by_name(email):
        user = get_user_by_email(email)
        return jsonify({
            "name": user['name'],
            "email": email,
            "password": user['password']
        })

    @app.route('/user', methods=['POST'])
    def api_create_user():
        """
        Add a new user into databse with email address and password
        """
        post_data = request.get_json()
        try:
        # TODO: Validate data for name, email and password
            name = post_data.get('name')
            email = post_data.get('email')
            password = post_data.get('password')
            insert_result = add_user(name, email, password)
            user_id = insert_result.inserted_id
            return jsonify({
                "user_id": str(user_id)
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/user', methods=["DELETE"])
    def api_delete_user():
        """
        Delete a user. 
        """
        post_data = request.get_json()
        user_email = post_data.get('email')
        try:
            delete_user(user_email)
            return jsonify({'user_email': user_email}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    @app.route('/user', methods=["PUT"])
    def api_update_user_password():
        """
        Update a user's password. 
        """
        post_data = request.get_json()
        user_email = post_data.get('email')
        new_password = post_data.get('password')
        try:
            edit_result = update_user(user_email, new_password)
            if edit_result.modified_count == 0:
                raise ValueError("no document updated")
            return jsonify({
                'user_email': user_email,
                'new_password': new_password
                }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    return app
