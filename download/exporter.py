"""
Different Exporter
"""


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


class PDFExporter(BaseExporter):
    """
    Export content as a PDF file
    """

    def __init__(self):
        pass


class MarkdownExporter(BaseExporter):
    """
    Export content as Markdown file
    """

    def __init__(self):
        pass


class HTMLExporter(BaseExporter):
    """
    Export content as html file
    """

    def __init__(self):
        pass
