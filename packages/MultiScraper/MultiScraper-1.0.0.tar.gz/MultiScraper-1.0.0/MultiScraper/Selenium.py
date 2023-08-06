from bs4 import BeautifulSoup
from selenium import webdriver

def parse_soup(url, browser="edge"):
    if browser == "edge":
        driver = webdriver.Edge(url)
    elif browser == "chrome":
        driver = webdriver.Chrome(url)
    elif browser == "firefox":
        driver = webdriver.Firefox(url)
    else:
        return "Браузер не поддерживается!"

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup

def parse_html(url, browser="edge"):
    if browser == "edge":
        driver = webdriver.Edge(url)
    elif browser == "chrome":
        driver = webdriver.Chrome(url)
    elif browser == "firefox":
        driver = webdriver.Firefox(url)
    else:
        return "Браузер не поддерживается!"

    driver.get(url)
    html = driver.page_source
    return html