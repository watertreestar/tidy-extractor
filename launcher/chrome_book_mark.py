import re

import requests

from export.mysql_exporter import MySQLExporter
from google_bookmark import GoogleBookMark
from tools.util import de_html
from tools.logger import logger

PROXIES = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087'
}


def start(path):
    mysql_exporter = MySQLExporter('localhost', 62723, 'root', 'root', '123456')

    gbm = GoogleBookMark(path, "https://github.com")
    github_links = gbm.parse()
    logger.info("Find %s link", str(len(github_links)))
    failed_links = []
    for link in github_links:
        if mysql_exporter.exist('chrome_book_mark', ('url', link)):
            logger.info("Exist this, skip......")
            continue
        try:
            logger.info("Extract url [%s]", link)
            html_text = requests.get(link, proxies=PROXIES).text
            title = re.findall(r"<title.*?>(.+?)</title>", html_text)[0]
            if len(title) > 200:
                title = title[0:200]
            text = de_html(html_text)
            normal_link = re.sub(r"#.*", "", title)
            data = [('url', link), ('title', normal_link), ('content', text)]
            logger.info("Insert to MySQL db")
            mysql_exporter.export('chrome_book_mark', data)
            logger.info("Insert finished.............................")
        except Exception as e:
            logger.exception("Errors occur:%s", e)
            failed_links.append(link)

    if len(failed_links) > 0:
        logger.error("Exist failed link,%s", failed_links)
    logger.info("All links has deal,haha > > >>>>>>>>>>>>>>>")
