import threading
from queue import Queue
import requests
import json
import time
import pdfkit
import re



class LaGou_spider():
    def __init__(self):
        self.url = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId=69'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie': 'KcOdIMg4LhYL9JmL8XLb0NUZuPo%2Cundefined%22%7D%5D; user-finger=335537b1b99aeedd303fa800cea99f37; LG_LOGIN_USER_ID=1da92f61302e61a84b0d557d29bfaf043c2fc86771214e7c; _putrc=05734D2650E27F4B; login=true; unick=%E9%99%88%E4%BA%9A%E5%B9%B3; gate_login_token=0f7f3e6cd430ae298be1782de0b0f555bdcc9d6173ba572c; X_HTTP_TOKEN=fa14cbf36322463a338655116160ebe3a4f4ba1ee8; JSESSIONID=AA2CDC15AE8CD4685AC5241E47728F60; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%228846294%22%2C%22%24device_id%22%3A%2217198128d17709-05c5221ccb5a9c-6701434-1327104-17198128d1944e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_campaign%22%3A%22distribution%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.141%22%7D%2C%22first_id%22%3A%221773845286bb8f-0914ab3b68e22c-31346d-1327104-1773845286cbe3%22%7D',
            'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=492',
            'Origin': 'https://kaiwu.lagou.com',
            'Sec-fetch-dest': 'empty',
            'Sec-fetch-mode': 'cors',
            'Sec-fetch-site': 'same-site',
            'x-l-req-header': '{deviceType:1}'}
        self.textUrl='https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId='  #发现课程文章html的请求url前面都是一样的最后的id不同而已
        self.queue = Queue()  # 初始化一个队列
        self.error_queue = Queue()

    def parse_one(self):
        """

        :return:获取文章html的url
        """
        # id_list=[]
        html = requests.get(url=self.url, headers=self.headers).text
        dit_message = json.loads(html)
        message_list = dit_message['content']['courseSectionList']
        # print(message_list)
        for message in message_list:
            for i in message['courseLessons']:
                true_url=self.textUrl+str(i['id'])
                self.queue.put(true_url)#文章的请求url


        return self.queue

    def get_html(self,true_url):
        """

        :return:返回一个Str 类型的html
        """
        html=requests.get(url=true_url,timeout=10,headers=self.headers).text
        dit_message = json.loads(html)
        str_html=str(dit_message['content']['textContent'])
        article_name=dit_message['content']['theme']
        article_name = re.sub(r'[\\\/\:\*\?\"\<\>\|\.]', "", article_name)
        self.htmltopdf(str_html,article_name)

    def htmltopdf(self,str_html,article_name):
        path_wk = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'custom-header': [('Accept-Encoding', 'gzip')]
        }
        pdfkit.from_string(str_html,"{}.pdf".format(article_name),configuration=config,options=options)



    def thread_method(self, method, value):  # 创建线程方法
        thread = threading.Thread(target=method, args=value)
        return thread

    def main(self):

        thread_list = []
        true_url= self.parse_one()
        while not  true_url.empty():
            m3u8 = true_url.get()
            print(m3u8)
            self.get_html(m3u8)
            time.sleep(2)
            # for i in range(10):  # 创建线程并启动
            #     if not true_url.empty():
            #         m3u8 = true_url.get()
            #         print(m3u8)
            #         thread = self.thread_method(self.get_html, (m3u8,))
            #         thread.start()
            #         print(thread.getName() + '启动成功,{}'.format(m3u8))
            #         thread_list.append(thread)
            #     else:
            #         break
            # while len(thread_list)!=0:
            #     for k in thread_list:
            #         k.join()  # 回收线程
            #         print('{}线程回收完毕'.format(k))
            #         thread_list.remove(k)



run = LaGou_spider()
run.main()