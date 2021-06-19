"""
    main script
"""
import logging
from launcher import chrome_book_mark

from tools.logger import get_logger

logger = get_logger('app',log_path='/Users/young/PycharmProjects/tidy-extractor/logs/app.log',log_level=logging.INFO)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('tidy-extract')
    chrome_book_mark.start("/Users/young/Desktop/bookmarks_2021_6_18.html")



