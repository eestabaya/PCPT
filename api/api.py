import uuid

from flask import Blueprint

from utils.db_config import db
from utils.scrape import scr

mod = Blueprint("api_stuff", __name__)


@mod.route("/api/<uid>")
def get_stuff(uid):
    return {"success": True, "uid": uid, "new_uid": str(uuid.uuid4())}


@mod.route("/api/mongo/add")
def add_to_mongo():
    db["test"].insert_one({"_id": str(uuid.uuid4())})
    return {"success": True}


@mod.route("/api/mongo")
def get_from_mongo():
    db_items = db["test"].find({})
    items = []
    for item in db_items:
        items.append(item)
    return {"success": True, "items": items}


@mod.route("/api/scrape")
def get_from_scrape():
    #items = []
    #for item in scr:
        #items.append(item)
    return {"success": True, "items": str(scr)}
