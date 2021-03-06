import unittest

from export.mysql_exporter import MySQLExporter


class MySQLExporterTest(unittest.TestCase):
    def setUp(self):
        self.exporter = MySQLExporter('localhost', 62723, 'root', 'root', '123456')

    def test_export(self):
        self.exporter.export("chrome_book_mark",[('url','https://github.com'),('title','github'),('content','fafafafafafafafa')])

    def test_exist(self):
        exist = self.exporter.exist("chrome_book_mark", ("url","https://github.com/genli9/abstract-component"))
        print(exist)
