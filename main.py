from scraper import scrape_studentweb
from mailer import mail_self

def run():
    results = scrape_studentweb()
    res_list = results.split("\n")
    res_list = [i for i in res_list if len(i) > 0]
    if (len(res_list) > 1):
        body = ""
        for res in res_list:
            body += res + "\n"
        mail_self("mail","password","Flere nye karakterer!", body)
    elif (len(res_list) == 1):
        mail_self("mail","password",results)

run()
