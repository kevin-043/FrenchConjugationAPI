from models.favorite_verb_model import Favorite_verb
from database.__init__ import database
import app_config as config
from bson.objectid import ObjectId


def Crete_favorite_verb(owner,verb ):
    
    try:
        new_Favorite_verb = Favorite_verb()
        
        new_Favorite_verb.owner = owner
        new_Favorite_verb.verb = verb
        
        collection = database.dataBase[config.CONST_VERBS_COLLECTION]
        
        if collection.find_one({'verb': new_Favorite_verb.verb}):
            return "Duplicated verb"
        
        created_favorite_verb = collection.insert_one(new_Favorite_verb.__dict__)
        
        return created_favorite_verb
        
    except Exception as err:
        print("Error on creating favorite verb: ", err)
        
        
def fetch_favorite_verbs(owner):
    try:
        collection = database.dataBase[config.CONST_VERBS_COLLECTION]
        
        favorite_verbs = []

        
        for verb in collection.find({"owner": owner}):
            current_verb = {"verb": verb["verb"], "id": str(
                verb["_id"])}  
            favorite_verbs.append(current_verb)
            
            
        return favorite_verbs
    except Exception as err:
        print("Error on trying to fetch favorites. ", err)


def delete_favorite_verb(uid):
    try:
        collection = database.dataBase[config.CONST_VERBS_COLLECTION]
        
        result = collection.find_one_and_delete({"_id": ObjectId(uid)})
        
        return result is not None
        
    except Exception as err:
        print("Error on trying to delete favorite verb. ", err)