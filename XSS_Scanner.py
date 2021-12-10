import scanning

'''Complete the configuration as required for target website'''

target_url = "http://testphp.vulnweb.com/"                                      # Change this
login_url = target_url + "login.php"                                            # Change this
ignore_links = target_url + "logout.php"                                        # Change this
data_dict = {"uname": "test", "pass": "test", "login": "submit"}                # Change this



vuln_scanner = scanning.Scanner(target_url, ignore_links)
vuln_scanner.session.post(login_url, data=data_dict)

vuln_scanner.crawl()
vuln_scanner.run_scanner()

