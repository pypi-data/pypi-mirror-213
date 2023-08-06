from bs4 import BeautifulSoup
import http.client

def parse_soup(url):
    sp = url.split('/')
    conn = http.client.HTTPSConnection(sp[2])

    if len(sp) > 3: conn.request("GET", f"/{sp[3]}/")
    else: conn.request("GET", "/")

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    soup = BeautifulSoup(data, 'lxml')
    return soup

def parse_html(url):
    sp = url.split('/')
    conn = http.client.HTTPSConnection(sp[2])

    if len(sp) > 3: conn.request("GET", f"/{sp[3]}/")
    else: conn.request("GET", "/")

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    return data
