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
            'referrer': 'https://google.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def extract_source(url):
    """given a page's url, returns the html source"""
    source = requests.get(url, headers=random_headers()).text
    return source


def extract_bh_num_results(source):
    """given the html source of a page on B&H, returns the number of products in the page's category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    num_products = int(soup.find_all(lambda tag: tag.name == 'span' and tag.get('data-selenium') == 'titleNumberingPagination')[0].contents[0].split()[2])
    return num_products


def extract_adorama_num_results(source):
    """given the html source of a page on Adorama, returns the number of products in the page's category"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    if str(soup.find_all("title")[0].contents[0]).strip() == "Access to this page has been denied.":
        print("Captcha block detected! Scrape failed.")
        f = open("test.txt", 'w')
        f.write(soup.text)
        return 0
    num_products = int(soup.find_all(class_="index-count-total")[0].contents[0])
    return num_products


def extract_bh_page(source):
    """given a B&H page's html source, returns dictionary with format { part # : price } of all products on page"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    part_num_to_data = {}
    products = soup.find_all(lambda tag: tag.name == 'div' and tag.get('data-selenium') == 'miniProductPageProduct')
    for product in products:
        product_soup = bs4.BeautifulSoup(str(product), 'lxml')

        product_name = product_soup.find(lambda tag: tag.name == 'div' and tag.get('data-selenium') == 'miniProductPageProductSkuInfo').contents[0].split()
        product_name = product_name[len(product_name) - 1]

        product_price_section = product_soup.find(lambda tag: tag.name == 'span' and tag.get('data-selenium') == 'uppedDecimalPrice')
        if product_price_section is None:
            print("Price unavailable: " + product_name)
            continue
        product_price = product_price_section.contents[0].contents[0] + "." + product_price_section.contents[1].contents[0]

        part_num_to_data[product_name] = product_price

    return part_num_to_data


def extract_adorama_page(source):
    """given an Adorama page's html source, returns dictionary with format { part # : price } of all products on page"""
    soup = bs4.BeautifulSoup(source, 'lxml')
    if str(soup.find_all("title")[0].contents[0]).strip() == "Access to this page has been denied.":
        print("Captcha block detected! Scrape failed.")
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


def scrape_bh_category(category_url):
    """given a B&H category's url, scrapes all pages and returns a dictionary with format { part # : price } of all
    products in category"""
    num_products = extract_bh_num_results(extract_source(category_url))
    part_num_to_data = {}
    for i in range((num_products - 1) // 30 + 2):
        page_data = extract_bh_page(extract_source(category_url + "/pn/" + str(i)))
        part_num_to_data.update(page_data)
    return part_num_to_data


def scrape_adorama_category(category_url):
    """given an Adorama category's url, scrapes all pages and returns a dictionary with format { part # : price } of
    all products in category"""
    num_products = extract_adorama_num_results(extract_source(category_url))
    part_num_to_data = {}
    for i in range(0, num_products, 15):
        page_data = extract_adorama_page(extract_source(category_url + "?startAt=" + str(i)))
        part_num_to_data.update(page_data)
    return part_num_to_data


# bh_gpu = scrape_bh_category("https://www.bhphotovideo.com/c/buy/Graphic-Cards/ci/6567/N/3668461602")
# for pair in bh_gpu.items():
#    print(str(pair) + "\n")
# print(len(bh_gpu))


# adorama_gpu = scrape_adorama_category(
#     "https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards")
# print(adorama_gpu)
# adorama_ram = scrape_adorama_category(
#     "https://www.adorama.com/l/Computers/Computer-Components/Computer-Memory-lrbr-RAM-rrbr")
# print(adorama_ram)
# adorama_ssd = scrape_adorama_category(
#     "https://www.adorama.com/l/Computers/Drives-comma-SSD-and-Storage/Internal-SSD-Drives")
# print(adorama_ssd)
# adorama_hdd = scrape_adorama_category(
#     "https://www.adorama.com/l/Computers/Drives-comma-SSD-and-Storage/Hard-Disk-Drives")
# print(adorama_hdd)
# adorama_mobo = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Motherboard-Interfaces")
# print(adorama_mobo)
# adorama_psu = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Desktop-Power-Supplies")
# print(adorama_psu)
# adorama_cpu = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/CPU-Processors")
# print(adorama_cpu)
# adorama_case = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Tower-Cases")
# print(adorama_case)
