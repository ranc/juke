import unittest

from ex6.crawl import Crawler, WordCounter
from ex6.moogle import search_pages
from ex6.page_rank import rank_pages

BASE_URL = "https://www.cs.huji.ac.il/~intro2cs1/ex6/wiki/"

class TestEx6(unittest.TestCase):
    def test_part1(self):
        crawler = Crawler(BASE_URL, "small_index.txt")
        crawler.start_crawling()
        print(crawler.traffic_dict)

    def test_part2(self):
        word_dict = {
            "Hogwarts": {"Harry": 1, "Hogwarts":10},
            "Harry": {"Harry": 10, "Herminone": 1, "Draco": 1},
            "Draco": {"Harry": 1},
            "Herminone": {"Herminone": 5}
        }
        print(rank_pages(word_dict, 100))

        page_rank = rank_pages(word_dict, 1)
        print(page_rank)
        #self.assertEqual(page_rank, {'Hogwarts': 0, 'Harry': 2.0, 'Draco': 0.5, 'Herminone': 0.5})

    def test_part3_1(self):
        counter = WordCounter(BASE_URL, "small_index.txt")
        counter.count_words("Harry_Potter.html")
        counter.count_words("Hermione_Granger.html")
        print(counter.word_dict)

    def test_part3_full(self):
        counter = WordCounter(BASE_URL, "small_index.txt")
        counter.start_counting()
        print(counter.word_dict["Harry"])

    def test_part4_1(self):
        for p,s in search_pages(["scar", "crookshanks"], "rank.pickle", "words.pickle",  5):
            print(p,s)

    def test_part4_2(self):
        for p,s in search_pages(["broom", "wand", "cape"], "rank.pickle", "words.pickle",  5):
            print(p,s)


if __name__ == "__main__":
    unittest.main()
