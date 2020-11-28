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

def add_scraped_product():
    # TODO pass in product's ID, name, type, rating, and brand
    product_id = 0
    product_name = "test product"
    product_type = "computer thing"
    product_rating = 0.0
    product_brand = "brand"

    # TODO pass in store data
    store_id = 0
    product_price = 0.0
    store_url = "https://store.com/product"

    # product exists, update its Store field
    if(db.product.find({"product_id":product_id}).count > 0):
        db.product.update(
            {"product_id":product_id},
            {
                "$push": {
                    "stores": {
                        "store_id": store_id,
                        "product_price": product_price,
                        "store_url": store_url
                    }
                }
            }
        )
    # product does not exist, add it to the database
    else:
        db.product.insert(
            {
                "product_id": product_id,
                "product_name": product_name,
                "product_type": product_type,
                "product_rating": product_rating,
                "product_brand": product_brand,
                "stores": [
                    {
                        "store_id": store_id,
                        "product_price": product_price,
                        "store_url": store_url
                    }
                ]
            }
        )
    return {"success": True};


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
