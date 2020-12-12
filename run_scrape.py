from utils.db_config import db
from utils.scrape import get_cpu_prices, get_gpu_prices


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


log_scrape()
