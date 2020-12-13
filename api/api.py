from flask import Blueprint, request

from utils.db_config import db

mod = Blueprint("api_stuff", __name__)


def get_from_mongo(col="test"):
    try:
        db_items = db[col].find({})
        items = [item for item in db_items]
        return {"success": "true", "items": items}
    except Exception as e:
        return {"success": "false", "cause": str(e)}


def get_product_from_mongo(model_num):
    return db["product"].find_one({"_id": model_num})


def update_user(_id, salt=None, pw_hash=None, search=None, pc_part=None, remove=False):
    user_col = db["users"]

    query = {"_id": _id}

    if pc_part is not None:
        if remove:
            update = {
                "$pull": {
                    "configuration": pc_part
                }
            }
            user_col.update_one(query, update)
        else:
            update = {
                "$push": {
                    "configuration": pc_part
                }
            }
            user_col.update_one(query, update)

    if salt is not None and pw_hash is not None:
        update = {
            "$set": {
                "password": {
                    "salt": salt,
                    "hashed": pw_hash
                }
            }
        }
        user_col.update_one(query, update)

    if search is not None:
        update = {
            "$push": {
                "search_history": {
                    "$each": [search],
                    "$position": 0
                }
            }
        }
        user_col.update_one(query, update)


def find_user(username, email=False):
    if email:
        return db["users"].find_one({"email": username.lower()})
    return db["users"].find_one({"name_lower": username.lower()})


def create_user(u):
    data = {
        "_id": u.name,
        "name_lower": u.name.lower(),
        "email": u.email,
        "password": {"salt": u.salt, "hashed": u.pw_hash},
        "search_history": [],
        "configuration": []
    }
    db["users"].insert_one(data)


@mod.route("/api/product")
def get_from_database():

    product_id = request.args.get('model_num')

    if product_id is None or product_id is "" or product_id.isspace():
        return {"success": "false", "reason": "Missing model_num parameter"}, 400

    product = db["product"].find_one({"_id": product_id})

    return {"success": "true", "product": product}
