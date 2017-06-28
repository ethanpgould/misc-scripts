"""
Ethan P. Gould
https://github.com/ethanpgould
ethanpgould@gmail.columbia

A simple script to download all .pdf files from a given url.

Usage: must specify url to base html page and *complete* path to
the directory you would like to save them to, otherwise this version will not work. 

Ex: python fetchpdfs.py http://www.exampleurl.com/ /Users/yourname/directory
"""

import requests
from bs4 import BeautifulSoup
import urllib
import sys
import os

def fetch_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    raise Exception("{} Error".format(r.status_code))

def scrape_links(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.find_all('a') # return all link elements

def get_pdfs(url, base_dir):
    html = fetch_page(url)
    links = scrape_links(html)

    if len(links) == 0:
        raise Exception("No Links On Page")
    pdf_count = 0

    for link in links:
        if link['href'][-4:] == ".pdf":
            pdf_count += 1
            pdf = requests.get(urllib.parse.urljoin(url, link['href']))
            print(pdf.status_code)
            if pdf.status_code == 200:
               with open(os.path.join(base_dir, link['href']), 'wb') as f:
                   f.write(pdf.content)

    if pdf_count == 0:
        raise Exception("No PDFs on Page")
    print("{} PDF files saved in {}".format(pdf_count, base_dir))

def main(): # specify page to scrape for pdf and place to put them
    url = sys.argv[1]
    base_dir = sys.argv[2]
    print("Downloading PDFs from "+sys.argv[1]+" to "+sys.argv[2])
    print("...")
    if os.path.isdir(base_dir):
        try:
            get_pdfs(url, base_dir)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
