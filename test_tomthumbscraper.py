#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import json
import requests
from lxml import html
import tomthumbscraper


class TestTomThumbScraper(unittest.TestCase):

    def setUp(self):
        self.json_data_url = \
            'https://s3-eu-west-1.amazonaws.com/legalstart/thumbscraper_input_tampered.hiring-env.json'
        self.url = 'https://yolaw-tokeep-hiring-env.herokuapp.com'
        self.username = 'Thumb'
        self.password = 'Scraper'
        self.scraper = \
            tomthumbscraper.TomThumbScraper(self.json_data_url,
                                            self.url, self.username, self.password)

    def test_run(self):
        self.scraper.run()

    def test_request_invalid_parameters(self):
        with self.assertRaises(Exception):
            scraper = \
                tomthumbscraper.TomThumbScraper(self.json_data_url)
            scraper.run()

    def test_request_invalid_credentials(self):
        self.scraper.load_current_page()
        self.scraper.password = 'some random password'
        with self.assertRaises(Exception):
            scraper.load_current_page()

    def test_is_on_correct_page(self):
        page = requests.get(self.url, auth=(self.username,
                                            self.password))
        self.scraper.current_page_data = \
            html.document_fromstring(page.text)
        self.assertTrue(self.scraper.is_on_correct_page())
        self.scraper.current_page_data = html.document_fromstring('<a>')
        self.assertFalse(self.scraper.is_on_correct_page())

    def test_move_to_next_page(self):
        page = requests.get(self.url, auth=(self.username,
                                            self.password))
        self.scraper.current_page_data = \
            html.document_fromstring(page.text)
        self.scraper.move_to_next_page()
        self.assertEqual(self.scraper.index, self.scraper.data['0'
            ]['next_page_expected'])


if __name__ == '__main__':
    unittest.main()
