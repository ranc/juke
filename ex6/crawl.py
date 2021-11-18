from typing import Dict
import requests
import urllib.parse


class Crawler:
    word_dict: Dict[str, Dict[str, int]]

    def __init__(self, base_url: str, index_file: str):
        self.base_url = base_url
        with open(index_file) as f:
            self.word_dict = dict((line.strip(), {}) for line in f.readlines())
            self.word_set = set(self.word_dict.keys())

    def start_crawling(self):
        for page in self.word_set:
            self.crawl_page(page)

    def crawl_page(self, page: str):
        full_url = urllib.parse.urljoin(self.base_url, page)
        doc = requests.get(full_url).text
        entry = self.word_dict[page]
        self.count_links(doc, entry)

    def count_links(self, doc: str, page_entry: Dict[str, int]):
        from bs4 import BeautifulSoup
        parsed_doc = BeautifulSoup(doc, 'html.parser')
        for a in parsed_doc.find_all('a'):
            link: str = a.get('href')
            if link is None:
                continue
            link = link.strip()
            if len(link) == 0:
                continue
            # if absolute link
            if link.startswith(self.base_url):
                link = link[len(self.base_url):]
            if link not in self.word_set:
                continue
            if link not in page_entry:
                page_entry[link] = 1
            else:
                page_entry[link] += 1


class WordCounter:
    word_dict: Dict[str, Dict[str, int]]

    def __init__(self, base_url: str, index_file: str):
        self.base_url = base_url
        self.word_dict = {}
        with open(index_file) as f:
            self.page_set = set(f.readlines())

    def start_counting(self) -> Dict[str, Dict[str, int]]:
        for page in self.page_set:
            self.count_words(page)
        return self.word_dict

    def count_words(self, page):
        full_url = urllib.parse.urljoin(self.base_url, page)
        doc = requests.get(full_url).text
        from bs4 import BeautifulSoup
        parsed_doc = BeautifulSoup(doc, 'html.parser')
        for p in parsed_doc.find_all("p"):
            for word in p.text.split():
                if word not in self.word_dict:
                    self.word_dict[word] = {page: 1}
                elif page not in self.word_dict[word]:
                    self.word_dict[word][page] = 1
                else:
                    self.word_dict[word][page] += 1


