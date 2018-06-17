#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Tom Thumb Scraper
~~~~~~~~~~~~~~~~~

Tom Thumb Scraper is a web scraper which takes an entry point and moves
to other links using XPATH Queries.

    >>> import tomthumbscraper
    >>> scraper = tomthumbScraper.TomThumbScraper('http://www.example.com/jsonFile.json', 'https://entrypoint.com')
    >>> scraper.run()
        Move to page 1
        Move to page 2
        ...
        ALERT - Can’t move to page 4: page 3 link has been malevolently tampered with!!
"""

import sys
import json
import requests
from lxml import html


def fetch_json_data(data_link):
    """Loads the JSON data from a given URL

    :param:
        data_link: Link to the JSON data file

    :raises:
         Exception: if doesn't receive success response

    :return:
         Python Object deserialized from a JSON document
    """

    data_element = requests.get(data_link)

    if not data_element.status_code \
        == TomThumbScraper.HTTP_SUCCESS_RESPONSE:
        raise Exception('Unable to get JSON data from the given link')

    return json.loads(data_element.text)


class TomThumbScraper:

    """TomThumbScraper is a web scraper which moves through multiple pages after successful validation.

    The programme can be run through the terminal with the following command:

    (Rakesh-MacBook)$ python /*path to tomthumbscraper.py*/ url_to_json_file entry_point_for_scraper username password

    The scraper downloads and stores the json data from the given link and stores it into a python object which is later
    used for validation and access purpose. The JSON data format is show below in INPUT section.

    Input:
        Scraper consumes a JSON object as input in the following format:

            "0": {
                "next_page_expected": "b8e06d3f",
                "xpath_button_to_click": "/html/body/div[1]/nav/div/div/ul/li[1]/div/div/div[3]/ul[2]/li[4]/a",
                "xpath_test_query": "//*[@id=\"body\"]/div/div/section[1]/div/h2//text()",
                "xpath_test_result": [
                    "\n    \n      Legalstart, le partenaire juridique de plus de 50 000 entrepreneurs\n    "
                ]
            }

    Output:

        Move to page 1
        Move to page 2
        Move to page 3
        ...
        ALERT - Can’t move to page 12: page 11 link has been malevolently tampered with!!

    """

    HTTP_SUCCESS_RESPONSE = 200

    def __init__(
        self,
        data_link,
        initial_url,
        username='Thumb',
        password='Scraper',
        index='0',
        ):
        """ Initializes the data

        :arg:
        :param data_link: Link to the JSON data file
        :param initial_url: The entry point for scraper
        :param username: Username for authenticating the scraper
        :param password: Password for authenticating the scraper
        :param index: Index from JSON file to start reading from. Default is "0"

        :raises:
            Exception: if starting index is not found in JSON file (default="0").

        """

        self.base_url = initial_url
        self.url = initial_url
        self.index = index
        self.username = username
        self.password = password
        self.current_page_data = None
        self.data = fetch_json_data(data_link)

        if self.index not in self.data:
            raise Exception('No starting index found in JSON file')

    def run(self):
        """This is a class method which loads the current page
        and verifies if the current page is expected or not by
        making XPATH query to an HTML fragment in page content.

        If the current page is successfully validated, scraper
        moves to the next desired page and page count is incremented.

        If the current page is not the desired page, it stops the flow
        and prints into the console the tampered page number.
        """

        page_counter = 0

        while True:
            self.load_current_page()
            if self.is_on_correct_page():
                page_counter += 1
                print ('Move to page', page_counter)
                self.move_to_next_page()
                continue
            else:
                print ('ALERT - Can\'t move to page', page_counter + 1,
                       ': page', page_counter,
                       'link has been malevolently tampered with!!')
            break

    def load_current_page(self):
        """Loads a page from a url and creates a HTML tree from the content.

        :raises:
            Exception if doesn't recieve a success response.
        """

        page = requests.get(self.url, auth=(self.username,
                            self.password))
        if not page.status_code \
            == TomThumbScraper.HTTP_SUCCESS_RESPONSE:
            raise Exception('Invalid page url or credentials supplied for '
                             + self.url)

        self.current_page_data = html.document_fromstring(page.text)
        self.current_page_data.make_links_absolute(self.base_url)

    def is_on_correct_page(self):
        """Validates that the current page is indeed the correct page as well

        :return:
            BOOL: True if on the right page, false otherwise.
        """

        actual_xpath_query_result = \
            self.current_page_data.xpath(self.data[self.index]['xpath_test_query'
                ])
        expected_xpath_query_result = \
            self.data[self.index]['xpath_test_result']

        return actual_xpath_query_result == expected_xpath_query_result

    def move_to_next_page(self):
        """Sets the next link to go to and updates the index to next expected index.
        """

        next_link_element = \
            self.current_page_data.xpath(self.data[self.index]['xpath_button_to_click'
                ])
        self.url = next_link_element[0].attrib['href']
        self.index = self.data[self.index]['next_page_expected']


if __name__ == '__main__':


    def main():
        """Creats a Scraper instance using the values supplies via Command-Line as parameteres
        """

        if len(sys.argv) < 3:
            print 'Atleast 2 arguments expected - Link to data file and base url'
            exit(1)

        if len(sys.argv) == 3:
            scraper = TomThumbScraper(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 5:
            scraper = TomThumbScraper(sys.argv[1], sys.argv[2],
                    sys.argv[3], sys.argv[4])
        else:
            print 'Invalid number arguments supplied.'
            print 'Expected Format: \npython tomthumbscraper.py url_to_json_file entry_point username password'
            exit(1)

        scraper.run()


    main()
