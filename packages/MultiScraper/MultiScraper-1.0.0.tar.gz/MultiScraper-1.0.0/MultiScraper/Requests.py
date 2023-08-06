from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import requests

def parse_get_soup(url, headers={}, cookies={}, json={}, data={}, parser='lxml'):
    response = requests.get(url, headers=headers, cookies=cookies, json=json, data=data)
    soup = BeautifulSoup(response.text, parser)
    return soup

def parse_get_html(url, headers={}, cookies={}, json={}, data={}):
    response = requests.get(url, headers=headers, cookies=cookies, json=json, data=data)
    return response.text

def parse_post_soup(url, json={}, data={}, parser='lxml'):
    response = requests.post(url, json=json, data=data)
    soup = BeautifulSoup(response.text, parser)
    return soup

def parse_post_html(url, json={}, data={}):
    response = requests.post(url, json=json, data=data)
    return response.text


def parse_auth(url, user, password):
    basic = HTTPBasicAuth(user, password)
    response = requests.get(url, auth=basic)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

