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
    soup = bs4.BeautifulSoup(source, 'lxml')
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
            # print(str(part_num) + ":" + str(part_price)) # debug

    return part_num_to_data

def scrape_adorama_category(category_url):
    """given an adorama category's url and name, writes the price data for each product in the category to a file
    named <category_name>.txt """
    num_products = extract_adorama_num_results(extract_source(category_url))
    part_num_to_data = {}
    for i in range(0, num_products, 15):
        page_data = extract_adorama_page(extract_source(category_url + "?startAt=" + str(i)))
        part_num_to_data.update(page_data)
    return part_num_to_data


# adorama_gpu = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Video-and-Graphics-Cards")
# adorama_ram = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Computer-Memory-lrbr-RAM-rrbr")
# adorama_ssd = scrape_adorama_category("https://www.adorama.com/l/Computers/Drives-comma-SSD-and-Storage/Internal-SSD-Drives")
# adorama_hdd = scrape_adorama_category("https://www.adorama.com/l/Computers/Drives-comma-SSD-and-Storage/Hard-Disk-Drives")
# adorama_mobo = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Motherboard-Interfaces")
# adorama_psu = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/Desktop-Power-Supplies")
# adorama_cpu = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Components/CPU-Processors")
# adorama_case = scrape_adorama_category("https://www.adorama.com/l/Computers/Computer-Tower-Cases")


# print(adorama_gpu)
# print(adorama_ram)
# print(adorama_ssd)
# print(adorama_hdd)
# print(adorama_mobo)
# print(adorama_psu)
# print(adorama_cpu)
# print(adorama_case)
