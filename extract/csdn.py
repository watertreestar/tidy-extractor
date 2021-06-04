import codecs
import os
import re

import html2text
import requests
from bs4 import BeautifulSoup


class Analyzer(object):
    """docstring for Analyzer"""

    def __init__(self):
        super(Analyzer, self).__init__()

    # get the page of the blog by url
    def get(self, url):
        headers = {

            'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
            'Cookie': 'uuid_tt_dd=10_36633268600-1616984717880-679008; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_36633268600-1616984717880-679008; _ga=GA1.2.2044190035.1616984719; c_segment=0; dc_sid=b6eb5b87c939d448ca7072ae53c14cc8; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1618722210,1618723329; Hm_lpvt_e5ef47b9f471504959267fd614d579cd=1618799461; __gads=ID=67c46669364474e0-22193ad184c7009b:T=1619165033:RT=1619165033:S=ALNI_MZEUUV7mk5X5qVszybwXTz5szdPYg; _gid=GA1.2.49058454.1621821512; aliyun_webUmidToken=T2gAVNdoJOKnipaqHKvBkD7eMkVCLga_XxvBmZM-7tfrjbcWlYRIulzezYimm5bVvPU=; is_advert=1; c_first_ref=www.google.com; unlogin_scroll_step=1622683265850; SESSION=347d36e7-0aa2-46fc-9f51-c509ba118590; ssxmod_itna=iqRx2DcDRD0Q0=QGHqwnDjrE0DCDu0PZ=Y6Cx0H+eiODUoxnRiyWw44Tyq8/yp5Kf7mqaPhqW0q5foFDneG0DQKGmCxGtFD7Tb5oHcUPD3Dm4i3DDE3DgDmKGgKqGfvfxDcFDcxN=Gw7d3DGqDnCkf/DBoxs2ND73=D3RPDtu=H7xp0B8=HI4DHmBqhKa4k/SqWW0GYWGGtfgLaMDh8AExrEhepBBddCRnMiBydeD===; ssxmod_itna2=iqRx2DcDRD0Q0=QGHqwnDjrE0DCDu0PZ=Y6Dn9g9vxDss7eDLnOYXS4n+ZGjh/5OuQlEatP/iI0ARhe82BK4sYGzLvhtFub6PFp8q8ioIF9Qec0qL7l6zHbspuhPMkzU=8d1gn/n4H8O=isReaanoTt6rmzY6uWfOatslGQNAiduDOH9mwpOgp+oYydw9rzztFz5E7mXZ7mP/OEr67z9fn8939U3b9mSKQU3+cjKkILVcbjp9TtrfcWgQWOxpqfOmCLhSo0N3jyc/kfPHfvZRjgf14Dw2idDjKD+2GDD; firstDie=1; dc_session_id=10_1622695564189.170802; c_first_page=https%3A//blog.csdn.net/yjk13703623757/article/details/79490476; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1622644623,1622644628,1622685842,1622695565; log_Id_click=99; c_pref=https%3A//blog.csdn.net/f641385712/category_7941357.html%3Fspm%3D1001.2014.3001.5482; c_ref=https%3A//fangshixiang.blog.csdn.net/category_7941357_2.html; announcement-new=%7B%22isLogin%22%3Afalse%2C%22announcementUrl%22%3A%22https%3A%2F%2Fblog.csdn.net%2Fblogdevteam%2Farticle%2Fdetails%2F112280974%3Futm_source%3Dgonggao_0107%22%2C%22announcementCount%22%3A0%7D; c_page_id=default; dc_tos=qu417g; log_Id_pv=684; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1622697244; log_Id_view=1976'
        }
        # req = urllib.Request(url, headers=headers)
        # html_doc = urllib.urlopen(req).read()
        response = requests.get(url, headers=headers)
        html_doc = response.text
        return html_doc


'''
Exports file with different format 
'''


class Exporter(Analyzer):
    """docstring for Exporter"""

    def __init__(self):
        super(Exporter, self).__init__()

    # get the title of the article
    def getTitle(self, detail):
        return detail.find(class_='article-title-box').h1

    # get the content of the article
    def getArticleContent(self, detail):
        return detail.find(class_='article_content')

    # export as markdown
    def export2markdown(self, f, detail):
        f.write(html2text.html2text(self.getTitle(detail).prettify()))
        f.write(html2text.html2text(self.getArticleContent(detail).prettify()))

    # export as html
    def export2html(self, f, detail):
        f.write(self.getTitle(detail).prettify())
        f.write(self.getArticleContent(detail).prettify())

    # export
    def export(self, link, cate_name, form):
        cate_name = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", cate_name)
        html_doc = self.get(link)
        soup = BeautifulSoup(html_doc, "html.parser")
        detail = soup.find(class_='blog-content-box')
        filename = self.getTitle(detail).getText()
        filename = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", filename)
        path = './csdn/'
        print('Exporting [{}]'.format(filename))
        if form == 'markdown':
            path += 'markdown' + '/' + cate_name
            if not os.path.exists(path):
                os.makedirs(path)
            f = codecs.open(path + '/' + filename + '.md', 'w', encoding='utf-8')
            self.export2markdown(f, detail)
            f.flush()
            f.close()
            return
        elif form == 'html':
            path += 'html' + '/' + cate_name
            if not os.path.exists(path):
                os.makedirs(path)
            f = codecs.open(path + '/' + filename + '.html', 'w', encoding='utf-8')
            self.export2html(f, detail)
            f.close()
            return

    def run(self, link, cate_name, form):
        self.export(link, cate_name, form)


class Parser(Analyzer):
    """docstring for parser"""

    def __init__(self):
        super(Parser, self).__init__()
        self.article_list = []
        self.cate = {}
        self.cate_link = {}

    '''
    获取分类
    '''

    def get_categories(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        cates = soup.select(".user-special-column .aside-common-box-content")[0].select('a')
        for cate_href in cates:
            # print(cate_href)
            cate_name = cate_href.span.getText()
            cate_link = cate_href['href']
            if len(cate_href.select('.pay-tag')) == 0:
                print('Find Free cate [{}] with link [{}]'.format(cate_name,cate_link))
                self.cate[cate_name] = cate_link
            else:
                print('Find Chargeable cate [{}] with link [{}].Discard it'.format( cate_name,cate_link))

    '''
        deal all categories
    '''
    def parse_per_categories(self):

        for c_name in self.cate.keys():
            c_link = self.cate[c_name]
            article_link = self.get_cate_all_article(c_name,c_link)
            self.cate_link[c_name] = article_link

    '''
        Gets all article link for one cate
    '''
    def get_cate_all_article(self,cate_name, cate_link):
        page,article_list = self.get_page_article(cate_link)
        print('Cate [{}] find [{}] 页. Article [{}]条'.format(cate_name,page,len(article_list)))
        return article_list

    def get_page_article(self, cate_link):
        page = 1
        article_link = []
        while True:
            link = cate_link[:-5] + '_' + str(page) + cate_link[-5:]
            html_doc = self.get(link)
            soup = BeautifulSoup(html_doc, features="html.parser")
            article_list = soup.select('.column_article_list')[0].select('li')
            if len(article_list) > 0:
                page = page + 1
                article_link.extend([l.a['href'] for l in article_list])
            else:
                break

        return page-1,article_link

    '''
        Export a pdf
    '''
    def export(self, export_format):

        for cate_name in self.cate_link.keys():
            exporter = Exporter()
            cate_links = self.cate_link[cate_name]
            for link in cate_links:
                exporter.run(link, cate_name, export_format)

    '''
        Main method to start parse
    '''
    def run(self, url, export_format='markdown'):
        html_doc = self.get(url)
        self.get_categories(html_doc)
        self.parse_per_categories()
        self.export(export_format)

