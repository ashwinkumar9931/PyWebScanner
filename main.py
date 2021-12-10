#!/home/akm/PycharmProjects/PyWebScanner2 python

import requests
from bs4 import BeautifulSoup

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "http://testphp.vulnweb.com/"

response = request(target_url)


parsed_html = BeautifulSoup(response.content)
print parsed_html