import cloudscraper
from bs4 import BeautifulSoup

def parse_soup(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    return soup

def parse_html(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    return response.content
