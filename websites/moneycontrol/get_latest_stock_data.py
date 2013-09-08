#! /usr/bin/env python

"""
Script to freshly download all the moneycontrol stock quote pages
"""

import add_bsecodes_to_stock_quote_page_urls
import download_alphabet_pages
import get_stock_quote_page_urls_from_alphabet_pages
import download_stock_quote_pages
import parse_stock_quote_pages

download_alphabet_pages.download_alphabet_pages(download_if_dst_exists=False)
get_stock_quote_page_urls_from_alphabet_pages.run()
download_stock_quote_pages.run()
add_bsecodes_to_stock_quote_page_urls.run()
parse_stock_quote_pages.run()
