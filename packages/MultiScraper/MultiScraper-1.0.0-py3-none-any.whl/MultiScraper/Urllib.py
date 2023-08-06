from bs4 import BeautifulSoup
import urllib.request

def parse_soup(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup

def parse_html(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    return html


