import uuid

from flask import Blueprint

from utils.db_config import db

from utils.scrape import get_gpu_prices, get_cpu_prices

mod = Blueprint("api_stuff", __name__)


def get_from_mongo(col="test"):
    try:
        db_items = db[col].find({})
        items = [item for item in db_items]
        return {"success": "true", "items": items}
    except Exception as e:
        return {"success": "false", "cause": str(e)}


def update_user(_id, salt=None, pw_hash=None, search=None):
    user_col = db["users"]

    query = {"_id": _id}

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
        "configurations": {}
    }
    db["users"].insert_one(data)


@mod.route("/api/products/<product_id>")
def get_from_database(product_id):
    """ TODO
    e = db["product"].find({"product_id": product_id})
    items = [i for i in e]
    print(items)

    print(type(e))

    for i in e:
        items.append(i)

    for x in e:
        print(x)

    return {"something": items}
    """

    product = db["product"].find_one({"_id": product_id})
    print(product)
    return {}


# @mod.route("/api/<uid>")
def get_stuff(uid):
    return {"success": True, "uid": uid, "new_uid": str(uuid.uuid4())}


# TODO placeholder stuff
@mod.route("/api/scrape")
def get_from_scrape():
    # items = []
    # for item in scr:
    # items.append(item)
    return {"success": "false", "cause": "yes"}


# TODO placeholder stuff
@mod.route("/api/load")
def load_stuff():
    return {"success": True}
