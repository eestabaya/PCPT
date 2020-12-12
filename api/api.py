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


@mod.route("/api/ABCDEHGFIOUEGUIEBUIABUIUA")
def log_scrape():

    print("Processing GPUs")
    gpu = get_gpu_prices()

    print("Processing CPUs")
    cpu = get_cpu_prices()

    for site in gpu:
        for product in site:
            arr = site.get(product)
            price = arr[0]
            link = arr[1]
            update_product(product, price, site, link)

    for site in cpu:
        for product in site:
            arr = site.get(product)
            price = arr[0]
            link = arr[1]
            update_product(product, price, site, link)


def update_product(part_id, price, site, link):
    finder = db["product"].find_one({"_id": part_id})

    if finder is None:
        db["product"].insert(
            {
                "_id": part_id,
                "stores": {
                    site: {
                        "price": price,
                        "link": link
                    }
                }
            }
        )
    else:
        db["product"].update(
            {"_id": part_id},
            {
                '$set': {
                    'stores.' + site + "price": price,
                    'stores.' + site + "link": link
                }
            }
        )


def add_scraped_product(_id="", product_name="some product", product_type="computer thing", product_rating=0.0,
                        product_brand="brand"):
    # TODO pass in product's ID, name, type, rating, and brand
    _id = 0
    """
    product_name = "test product"
    product_type = "computer thing"
    product_rating = 0.0
    product_brand = "brand"
    """

    # TODO pass in store data
    store_id = 0
    product_price = 0.0
    store_url = "https://store.com/product"

    # TODO pass in date
    date = "placeholder"

    # product exists, update its Store field
    if db.product.find({"_id": _id}).count > 0:

        db.product.update(
            {"_id": _id},
            {
                "$push": {
                    "stores":
                        {
                            "store_id": store_id,
                            "product_price": product_price,
                            "store_url": store_url
                        },

                    "hist_price_data":
                        {
                            "product_price": product_price,
                            "date": date
                        }
                }
            }
        )

    # product does not exist, add it to the database
    else:
        db.product.insert(
            {
                "_id": _id,
                "product_name": product_name,
                "product_type": product_type,
                "product_rating": product_rating,
                "product_brand": product_brand,
                "stores":
                    [
                        {
                            "store_id": store_id,
                            "product_price": product_price,
                            "store_url": store_url
                        }
                    ],
                "hist_price_data":
                    [
                        {
                            "product_price": product_price,
                            "date": date
                        }
                    ]
            }
        )
    return {"success": "true"}


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
