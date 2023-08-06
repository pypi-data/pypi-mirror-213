from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='MultiScraper',
  version='1.0.0',
  author='Alexander554',
  author_email='gaa.280811@gmail.com',
  description='Multi Scraper is a set of tools for fast and easy parsing',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests', 'lxml', 'bs4', 'aiohttp', 'cloudscraper', 'selenium', 'urllib3'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='MultiScraper',
  python_requires='>=3.7'
)