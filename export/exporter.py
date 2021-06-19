"""
Different Exporter
"""
# !/usr/bin/python
# -*- coding:utf-8 -*-
import os.path

import pdfkit
import html2text


class BaseExporter:
    """
    Base Export for all exporter
    """

    def __init__(self):
        pass

    def write_file(self, file_path, encoding='UTF-8'):
        """
        Write data to file
        :param file_path:
        :param encoding:
        :return:
        """
        pass

    def write_mysql(self, conn, db, table, data_list=[]):
        """
        Write data to mysql database
        :param table:
        :param db:
        :param conn:
        :param data_list:
        :return:
        """
        pass

    def write_mongo(self, conn, doc, rows=[]):
        """
        Write data to  mongodb
        :param doc:
        :param conn:
        :param rows:
        :return:
        """
        pass

    def write_mq(self, conn, topic, messages=[]):
        """
        Write data to message mq
        :param conn:
        :param topic:
        :param messages:
        :return:
        """
        pass

    def export(self, export_path, file_name, content):
        """
        Export file
        :return:
        """
        self.do_export(export_path, file_name, content)

    def do_export(self,export_path, file_name, content):
        """
        Internal export method
        :return:
        """
        pass


class PDFExporter(BaseExporter):
    """
    Export content as a PDF file
    """

    def __init__(self, pdfkit_path):
        self.pdfkit_path = pdfkit_path

    def do_export(self,export_path, file_name, content):
        config = pdfkit.configuration(wkhtmltopdf=self.pdfkit_path)
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'custom-header': [('Accept-Encoding', 'gzip')]
        }
        pdfkit.from_string(content, "{}.pdf".format(file_name), configuration=config, options=options)


class MarkdownExporter(BaseExporter):
    """
    Export content as Markdown file
    """

    def __init__(self):
        pass

    def do_export(self, export_path, file_name, content):
        md_text = ""
        md_text += html2text.html2text(content)
        file_path = os.path.join(export_path,file_name)
        self.write_file(file_path)


class HTMLExporter(BaseExporter):
    """
    Export content as html file
    """

    def __init__(self, auto_complete):
        self.auto_complete = auto_complete

    def do_export(self,export_path, file_name, content):
        html_text = ""
        html_text += content
        file_path = os.path.join(export_path, file_name)
        self.write_file(file_path, html_text)


class MySQLHTMLExporter(BaseExporter):
    """
    Export html content to MySQL database
    """
    def do_export(self,export_path, file_name, content):
        pass
