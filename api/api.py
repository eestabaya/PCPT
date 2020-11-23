import uuid

from flask import Blueprint

from utils.db_config import db
# from utils.scrape import scr

mod = Blueprint("api_stuff", __name__)


def get_from_mongo():
    try:
        db_items = db["test"].find({})
        items = []
        for item in db_items:
            items.append(item)
        return {"success": True, "items": items}
    except Exception as e:
        return {"success": False, "cause": str(e)}


@mod.route("/api/<uid>")
def get_stuff(uid):
    return {"success": True, "uid": uid, "new_uid": str(uuid.uuid4())}


@mod.route("/api/mongo/add")
def add_to_mongo():
    db["test"].insert_one({"_id": str(uuid.uuid4())})
    return {"success": True}


@mod.route("/api/mongo")
def mongo_route():
    return get_from_mongo()


@mod.route("/api/scrape")
def get_from_scrape():
    #items = []
    #for item in scr:
        #items.append(item)
    return {"success": False, "cause": "yes"}


@mod.route("/api/load")
def load_stuff():

    return {"success": True}
