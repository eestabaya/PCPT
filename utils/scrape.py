#
# Code by Colin Lemarchand
#

from random import choice

import bs4
import requests

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def extract_source(url):
    """given a page's url, returns the html source"""
    source = requests.get(url, headers=random_headers()).text
    return source


def extract_adorama_num_results(source):
    """given a page's html source, returns the number of products in the page's category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    num_products = int(soup.find_all(class_="index-count-total")[0].contents[0])
    return num_products


def extract_adorama_page(source):
    """ given a page's html source, adds all products in the page's category to externally defined dictionary,
    with format { part # : price } """

    part_num_to_data = {}

    soup = bs4.BeautifulSoup(source, 'lxml')
    products_tab = soup.find_all(class_="item-list")[0].contents
    for item in products_tab:
        if type(item) == bs4.element.Tag and item.get('class') == ['item']:
            part_num = None
            for elem in item.contents:
                if type(elem) == bs4.element.Tag and elem.get('class') == ['item-details']:
                    part_num = elem.contents[len(elem.contents) - 2].contents[3].contents[1].contents[0]

                elif type(elem) == bs4.element.Tag and elem.get('class') == ['item-actions']:
                    part_price = elem.contents[1].contents[5].get('value')

                    if part_price is None:
                        part_price = elem.contents[1].contents[7].get('value')

                    part_num_to_data[part_num] = part_price
                    # print(str(part_num) + ":" + str(part_price))

    return part_num_to_data


def scrape_adorama_category(category_url, category_name):
    """given an adorama category's url and name, writes the price data for each product in the category to a file
    named <category_name>.txt """

    num_products = extract_adorama_num_results(extract_source(category_url))
    part_num_to_data = {}

    for i in range(0, num_products, 15):
        part_num_to_data[i] = extract_adorama_page(extract_source(category_url + "?startAt=" + str(i)))
    # file = open(f"../scrapes/{category_name}.txt", 'w')
    # file.write(str(pair) + "\n") for pair in part_num_to_data.items()]
    return part_num_to_data


scr = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards",
                        "adorama_gpu")
# scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Computer-Memory-lrbr-RAM-rrbr", "adorama_ram")

