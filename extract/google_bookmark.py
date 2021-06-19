#!/bin/python3
#coding:utf-8

import os

import requests
from bs4 import BeautifulSoup

from tools.util import de_html


class GoogleBookMark:
    """
    Extract for google book marks to search better
    """

    def __init__(self, file, prefix = None):
        """
        Init file path and site prefix
        :param file:    bookmark file location
        :param prefix:  url prefix to filter site
        """
        self.file = file
        self.prefix = prefix

    def parse(self):
        """
        Parse file to bookmark url list
        :return: list
        """
        if not os.path.exists(self.file):
            raise Exception("File not found")
        f = open(self.file)

        content = f.read()
        soup = BeautifulSoup(content, "html.parser")
        if self.prefix:
            css_selector = "a[href^='"+self.prefix+"']"
        else:
            css_selector = 'a'
        links = soup.select(css_selector)
        return [item['href'] for item in links]




if __name__ == '__main__':

    # gbm = GoogleBookMark("/Users/young/Desktop/bookmarks_2021_6_18.html", "https://github.com")
    # github_links = gbm.parse()
    text = requests.get("https://github.com/watertreestar/tidy-extractor").text
    text = de_html(text)
    print(text)
