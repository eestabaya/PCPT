#
# Code by Colin Lemarchand
#

import bs4
import time
from random import choice
import requests

from selenium import webdriver

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

store_urls = {
    'adorama':
        {'gpu': "https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards",
         'cpu': "https://www.adorama.com/l/Computers/Computer-Components/CPU-Processors"},
    'bhphotovideo':
        {'gpu': "https://www.bhphotovideo.com/c/buy/Graphic-Cards/ci/6567/N/3668461602",
         'cpu': "https://www.bhphotovideo.com/c/buy/CPUs/ci/19865/N/3835434461"},
    'newegg':
        {'gpu': "https://www.newegg.com/p/pl?N=100007709%208000&PageSize=96&Order=1",
         'cpu': "https://www.newegg.com/p/pl?N=100007671%208000&PageSize=96&Order=1"}
}


def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def extract_source_requests(url):
    source = requests.get(url, headers=random_headers()).text
    time.sleep(10)
    return source


def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1400,1500")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


def extract_source(url, driver):
    """given a page's url, returns the html source"""
    driver.get(url)
    time.sleep(5)
    source = driver.page_source

    return source


def extract_bh_num_results(source):
    """given the html source of a page on B&H, returns the number of products in the page's category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    num_products = int(
        soup.find_all(lambda tag: tag.name == 'span' and tag.get('data-selenium') == 'titleNumberingPagination')[
            0].contents[0].split()[2])
    return num_products


def extract_adorama_num_results(source):
    """given the html source of a page on Adorama, returns the number of products in the page's category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    if str(soup.find_all("title")[0].contents[0]).strip() == "Access to this page has been denied.":
        print("Captcha block detected! Scrape failed.")
        time.sleep(100)
        return 0
    num_products = int(soup.find_all(class_="index-count-total")[0].contents[0])
    return num_products


def extract_newegg_num_pages(source):
    """given the html source of a page on Adorama, returns the number of pages in the product category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    num_pages = int(soup.find_all(class_="list-tool-pagination-text")[0].contents[3].contents[4])
    return num_pages


def extract_bh_page(source):
    """given a B&H page's html source, returns dictionary with format {part #: [price, link]} of all products on page"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    part_num_to_data = {}
    products = soup.find_all(lambda tag: tag.name == 'div' and tag.get('data-selenium') == 'miniProductPageProduct')
    for product in products:
        product_soup = bs4.BeautifulSoup(str(product), 'lxml')

        product_name = product_soup.find(
            lambda tag: tag.name == 'div' and tag.get('data-selenium') == 'miniProductPageProductSkuInfo').contents[
            0].split("#")
        product_name = product_name[len(product_name) - 1]

        product_price_section = product_soup.find(
            lambda tag: tag.name == 'span' and tag.get('data-selenium') == 'uppedDecimalPrice')
        if product_price_section is None:
            print("Price unavailable: " + product_name)
            continue
        product_price = product_price_section.contents[0].contents[0] + "." + \
                        product_price_section.contents[1].contents[0]

        product_link = 'www.bhphotovideo.com' + product_soup.find(
            lambda tag: tag.name == 'a' and tag.get('data-selenium') == 'miniProductPageProductNameLink').get('href')

        part_num_to_data[product_name] = [product_price, product_link]

    return part_num_to_data


def extract_adorama_page(source):
    """given an Adorama page's html source, returns dictionary with format { part # : price } of all products on page"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    if str(soup.find_all("title")[0].contents[0]).strip() == "Access to this page has been denied.":
        print("Captcha block detected! Scrape failed.")
        time.sleep(100)
        return {}
    products_tab = soup.find_all(class_="item-list")[0].contents
    part_num_to_data = {}
    for item in products_tab:
        if type(item) == bs4.element.Tag and item.get('class') == ['item']:
            part_num = None
            part_price = None
            for elem in item.contents:
                if type(elem) == bs4.element.Tag and elem.get('class') == ['item-details']:
                    part_num = elem.contents[len(elem.contents) - 2].contents[3].contents[1].contents[0]

                elif type(elem) == bs4.element.Tag and elem.get('class') == ['item-actions']:
                    for x in elem.contents:
                        if type(x) == bs4.element.Tag and x.get('class') == ['prices']:
                            for y in x.contents:
                                if type(y) == bs4.element.Tag and y.get('id') == 'FinalPrice':
                                    part_price = y.get('value')

            part_num_to_data[part_num] = part_price

    return part_num_to_data


def extract_newegg_page(source):
    """given a Newegg page's html source, returns dictionary with format { part # : price } of all products on page"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    part_num_to_data = {}
    item_containers = soup.find_all(class_="item-container")
    for item in item_containers:
        try:
            product_soup = bs4.BeautifulSoup(str(item), 'lxml')

            part_num_section = product_soup.find(lambda tag: tag.name == 'strong' and tag.text == 'Model #: ')
            if part_num_section is None:
                continue
            part_num = part_num_section.parent.contents[1]

            part_price_section = product_soup.find(class_='price-current').contents
            part_price = float((part_price_section[2].text + part_price_section[3].text).replace(",", ""))

            shipping_price = product_soup.find(class_='price-ship').text.split()[0].replace("$", "")
            try:
                part_price += float(shipping_price)
            except ValueError:
                pass
            rounded_part_price = f"${part_price:.2f}"

            if part_num is not None and rounded_part_price is not None:
                part_num_to_data[part_num] = rounded_part_price

        except Exception as e:
            print(e)
            continue
    return part_num_to_data


def scrape_bh_category(category_url):
    """given a B&H category's url, scrapes all pages and returns a dictionary with format { part # : price } of all
    products in category"""
    # driver = get_webdriver()
    # num_products = extract_bh_num_results(extract_source(category_url, driver))
    num_products = extract_bh_num_results(extract_source_requests(category_url))
    part_num_to_data = {}
    for i in range(1, (num_products - 1) // 30 + 2):
        # page_data = extract_bh_page(extract_source(category_url + "/pn/" + str(i), driver))
        page_data = extract_bh_page(extract_source_requests(category_url + "/pn/" + str(i)))
        part_num_to_data.update(page_data)
    # driver.close()
    return part_num_to_data


def scrape_adorama_category(category_url):
    """given an Adorama category's url, scrapes all pages and returns a dictionary with format { part # : price } of
    all products in category"""
    driver = get_webdriver()
    num_products = extract_adorama_num_results(extract_source(category_url, driver))
    part_num_to_data = {}
    for i in range(1, num_products, 15):
        page_data = extract_adorama_page(extract_source(category_url + "?startAt=" + str(i), driver))
        part_num_to_data.update(page_data)
    driver.close()
    return part_num_to_data


def scrape_newegg_category(category_url):
    """given a Newegg category's URL, scrapes all pages and returns a dictionary with format { part # : price } of
    all products in a category"""
    # driver = get_webdriver()
    # num_pages = extract_newegg_num_pages(extract_source(category_url, driver))
    num_pages = extract_newegg_num_pages(extract_source_requests(category_url))
    part_num_to_data = {}
    for i in range(1, num_pages):
        # page_data = extract_newegg_page(extract_source(category_url + "&page=" + str(i), driver))
        page_data = extract_newegg_page(extract_source_requests(category_url + "&page=" + str(i)))
        part_num_to_data.update(page_data)
    # driver.close()
    return part_num_to_data


def get_gpu_prices():
    gpu_prices = {}
    # gpu_prices['adorama'] = scrape_adorama_category(store_urls['adorama']['gpu'])
    gpu_prices['bhphotovideo'] = scrape_bh_category(store_urls['bhphotovideo']['gpu'])
    gpu_prices['newegg'] = scrape_newegg_category(store_urls['newegg']['gpu'])
    return gpu_prices


def get_cpu_prices():
    cpu_prices = {}
    # cpu_prices['adorama'] = scrape_adorama_category(store_urls['adorama']['cpu'])
    cpu_prices['bhphotovideo'] = scrape_bh_category(store_urls['bhphotovideo']['cpu'])
    cpu_prices['newegg'] = scrape_newegg_category(store_urls['newegg']['cpu'])
    return cpu_prices
