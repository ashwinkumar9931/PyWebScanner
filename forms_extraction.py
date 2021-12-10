import urlparse
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
forms_list = parsed_html.find_all("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    print post_url
    method = form.get("method")

    input_lists = form.findAll("input")
    post_data = {}
    for input in input_lists:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "payload"
        post_data[input_name] = input_value

    result = requests.post(post_url, data=post_data)
    print result.content


