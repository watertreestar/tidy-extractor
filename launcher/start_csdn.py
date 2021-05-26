from extract.csdn import Parser


def start(user_id, export_format):
    url = 'http://blog.csdn.net/' + user_id
    parser = Parser()
    parser.run(url, export_format)
