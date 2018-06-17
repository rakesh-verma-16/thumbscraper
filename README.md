# thumbscraper

Thumbscraper is a extendable, scalable and generic web scraper model which not only can scrape the websites for useful content but can also verify the landing pages by making XPATH queries.

### Dependencies
- Python3
- lxml

### Usage
> Thumb Scraper requires Python3 to run.
> Clone the project locally and install the dependencies

```sh
$ git clone https://github.com/rakesh-verma-16/thumbscraper.git
$ cd thumbscraper
$ python tomthumbscraper.py `url_to_json_file` `entry_point_for_scraper` `username` `password`
$ python test_tomthumbscraper.py
```

### JSON <Structure/Format>
```
{
    "0": {
        "next_page_expected": "12345",
        "xpath_button_to_click": "/html/body/div[1]/nav/div/div/ul/li[1]/div/div/div[3]/ul[2]/li[4]/a",
        "xpath_test_query": "//*[@id=\"body\"]/div/div/section[1]/div/h2//text()",
        "xpath_test_result": [
            "Some result here"
        ]
    },
    "12345": {
        "next_page_expected": "67890",
        "xpath_button_to_click": "/html/body/div[1]/nav/div/div/ul/li[4]/div/div/div[2]/ul/li[1]/a",
        "xpath_test_query": "//*[@id=\"content\"]/div[1]/div/a[2]//text()",
        "xpath_test_result": [
            "Some result here as well"
        ]
    },
    "67890": {
        "next_page_expected": "452528",
        "xpath_button_to_click": "/html/body/div[1]/nav/div/div/ul/li[1]/div/div/div[1]/ul/li[6]/a",
        "xpath_test_query": "//*[@id=\"body\"]/div[@class=\"page\"]/div[1]/div/h1//text()",
        "xpath_test_result": [
            "Some result here again."
        ]
    },
}
```
 
### Expected Output
```
Move to page 1

Move to page 2

...

ALERT - Can’t move to page 4: page 3 link has been malevolently tampered with!!
```

### TODOs
 - [x] Add comments
 - [ ] Write MORE tests
 - [ ] Make it more extendible
