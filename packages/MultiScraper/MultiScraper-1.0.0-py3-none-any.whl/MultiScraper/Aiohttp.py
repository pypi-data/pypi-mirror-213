import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def parse_soup(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'lxml')
    return soup


async def parse_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    return html