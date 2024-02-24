from flask import Blueprint, request, jsonify
from database.__init__ import database
from models.user_model import User
import json
from bson.objectid import ObjectId
from controllers.user_controller import create_user, login_user, fetch_users
from helpers.token_validation import validate_token
import requests
from models.favorite_verb_model import Favorite_verb
import app_config as config
from controllers.verb_controller import Crete_favorite_verb, fetch_favorite_verbs, delete_favorite_verb

verb_blueprint = Blueprint('verb_blueprint', __name__)

# ----------------- 1.1--------------------------


@verb_blueprint.route('/verbs/', methods=['GET'])
def get_verb():

    try:

        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401

        data = json.loads(request.data)

        # Check for 'verb' in the request body
        if "verb" not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400

        verb = data["verb"]

        response = requests.get(config.VERB_EXTERNAL_API_URL,
                                headers={
                                    'token': config.VERB_EXTERNAL_API_TOKEN
                                },
                                json={'verb': verb})

        if response.status_code == 200:
            return jsonify({"verb": response.json()}), 200
        else:
            return jsonify({"error": response.json()["errorMessage"]}), 500

    except Exception as err:
        return jsonify({'error': 'Something happened while trying load verb'}), 500


# --------------------------------------------1.2-------------------------------

@verb_blueprint.route('/verbs/random/', methods=['GET'])
def get_random_verbs():

    try:

        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401

        data = json.loads(request.data)

        # Check for 'verb' in the request body
        if "quantity" not in data:
            return jsonify({'error': 'quantity is needed in the request.'}), 400

        quantity = data["quantity"]

        response = requests.get(config.RANDOM_VERBS_EXTERNAL_API_URL,
                                headers={
                                    'token': config.RANDOM_VERBS_EXTERNAL_API_TOKEN},
                                json={'quantity': quantity})

        if response.status_code == 200:
            return jsonify({"verb": response.json()}), 200
        else:
            return jsonify({"error": response.json()["errorMessage"]}), 500

    except Exception as err:
        return jsonify({'error': 'Something happened while trying load quantity'}), 500


# ---------------------------------------------1.3-------------------------------------------

@verb_blueprint.route('/verbs/favorites/', methods=['POST'])
def Add_favorite_verbs():

    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401

        data = json.loads(request.data)

        if "verb" not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400

        if "uid" not in token:
            return jsonify({'error': 'uid in token is not property extracted.'}), 400

        verb = data["verb"]
        owner = token["uid"]

        created_favorite_verb = Crete_favorite_verb(owner=owner, verb=verb)

        

        if not created_favorite_verb.inserted_id:
            return jsonify({'error': 'Something happened when creating user.'}), 500

        return jsonify({'id': str(created_favorite_verb.inserted_id), "owner": owner, "verb": verb})

    except Exception as err:
        return jsonify({'error': 'Something happened while trying load quantity'}), 500


# --------------------------------1.4-----------------------------------------------

@verb_blueprint.route('/verbs/favorites/<favoriteUid>/', methods=['GET'])
def Get_one_favorite_verb(favoriteUid):

    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401

        collection = database.dataBase[config.CONST_VERBS_COLLECTION].find_one({
                                                                               "_id": ObjectId(favoriteUid)})
        
        if collection is None:
            return jsonify({'error': 'Favorite verb not found.'}), 404
        
        return jsonify({"id": str(collection["_id"]), "owner": collection["owner"], "verb": collection["verb"]})

    except Exception as err:
        return jsonify({'error': 'Favorite verb not found.'}), 500


# ------------------------------------1.5-------------------------------------------


@verb_blueprint.route('/verbs/favorites/', methods=['GET'])
def Get_all_favorite_verbs():
    
    try:
        
        token = validate_token()
        
        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401
        
        try:
            owner = token["uid"]
        except Exception as err:
            print(err, "owner not found")
            
        favorite_verbs = fetch_favorite_verbs(owner)
        
        return jsonify({"favorites": favorite_verbs})

        
        
    except Exception as err:
        return jsonify({'error': 'Something happened while getting all favorite verbs'}), 500





# ------------------------------------1.6-------------------------------------------

@verb_blueprint.route('/verbs/favorites/<favoriteUid>/', methods=['DELETE'])
def Delete_favorite_verb(favoriteUid):

    try:
        
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401
        
        delete_result = delete_favorite_verb(favoriteUid)
        
        if delete_result:
            return jsonify({'message': 'Favorite verb deleted successfully'}), 200
        else:
            return jsonify({'error': 'Favorite verb not found or could not be deleted'}), 404

        
    except Exception as err:
        return jsonify({'error': 'Something happened while deleting favorite verbs'}), 500



