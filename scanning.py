import requests
import re
import urlparse
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = []
        self.ignore_links = ignore_links

    def extract_links(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links and link not in self.ignore_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)

    def forms_extraction(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content)
        return parsed_html.find_all("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urlparse.urljoin(url, action)
        print post_url
        method = form.get("method")

        input_lists = form.findAll("input")
        post_data = {}
        for input in input_lists:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_value

        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.forms_extraction(link)
            for form in forms:
                print "[+] Testing in Form " + link
                vuln_xss = self.xss_forms(form, link)
                if vuln_xss:
                    print "\n\n[***] Discovered XSS in form : " + str(link)
                    print "........." + str(form) + "........."

            if "=" in link:
                print "\n\n[+] Testing .....  " + str(link)
                vuln_xss = self.xss_link(link)
                if vuln_xss:
                    print "[***] Discovered XSS in link : " + str(link)


    def xss_forms(self, form, url):
        xss_script = "<ScriPt>alert('xss')</ScrIPt>"
        response = self.submit_form(form, xss_script, url)
        return xss_script in response.content

    def xss_link(self, url):
        xss_script = "<ScriPt>alert('xss')</ScrIPt>"
        url = url.replace("=", "=" + xss_script)
        response = self.session.get(url)
        return xss_script in response.content



