import pickle
from operator import itemgetter
from typing import Dict, List, Tuple


def usage():
    print("usage:")
    print(sys.argv[0], "crawl <base_url> <index_file> <out_dict_file>")
    print(sys.argv[0], "page_rank <iterations> <dict_file> <out_rank_filename>")
    print(sys.argv[0], "words_dict <base_url> <index_file> <out_word_file>")
    print(sys.argv[0], "search <query> <rank_filename> <word_file> <max_results>")
    exit(-1)


def save_object(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def load_object(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


def search_pages(_query_list, _rank_filename, _words_filename, _max_results) -> List[Tuple[str, float]]:
    page_ranks: Dict[str, int] = load_object(_rank_filename)
    words_count: Dict[str, Dict[str, int]] = load_object(_words_filename)

    # 1. Filter pages that all the words exist there and take the minimum count between the words
    first_word = True
    page_word_count = {}  # to store the count of words per page
    for query in _query_list:
        if query not in words_count:
            continue  # if word does not exist, ignore it
        page_list = words_count[query] # pages this word appears in
        if first_word:  # first word sets the page list, rest is take the minimum and intersection
            page_word_count = page_list
            first_word = False
            continue

        # take only the pages that are in the page_list of this word and prev words and the minimum count
        page_word_count = {p: min(page_word_count[p], page_list[p]) for p in page_list.keys() if p in page_word_count}

    if len(page_word_count)==0:
        return [] # no page contains all words
    # 2. take the pages in the word list and their rank
    page_ranks = dict((p, page_ranks[p]) for p in page_word_count.keys())

    # 3. sort in reverse, take maximum max-results
    selected_pages = sorted(page_ranks, key=page_ranks.get, reverse=True)[:_max_results]
    results = []
    for _page in selected_pages:
        results.append((_page, page_ranks[_page] * page_word_count[_page]))

    return sorted(results, key=itemgetter(1), reverse=True)


if __name__ == "__main__":
    import sys
    from crawl import Crawler, WordCounter
    from page_rank import rank_pages

    if len(sys.argv) <= 4:
        usage()
    cmd = sys.argv[1]
    if cmd == 'crawl':
        base_url = sys.argv[2]
        index_file = sys.argv[3]
        out_file = sys.argv[4]
        crawler = Crawler(base_url, index_file)
        crawler.start_crawling()
        save_object(crawler.traffic_dict, out_file)
        print(crawler.traffic_dict)
        exit(0)
    if cmd == 'page_rank':
        iterations = int(sys.argv[2])
        word_dict_filename = sys.argv[3]
        out_file = sys.argv[4]

        word_dict = load_object(word_dict_filename)
        ranks = rank_pages(word_dict, iterations)
        save_object(ranks, out_file)
        exit(0)
    if cmd == 'words_dict':
        base_url = sys.argv[2]
        index_file = sys.argv[3]
        out_file = sys.argv[4]
        counter = WordCounter(base_url, index_file)
        word_counts = counter.start_counting()
        save_object(word_counts, out_file)
        exit(0)

    if cmd == 'search':
        if len(sys.argv) <= 5:
            usage()
        query_list = sys.argv[2].split()
        rank_filename = sys.argv[3]
        words_filename = sys.argv[4]
        max_results = int(sys.argv[5])

        results = search_pages(query_list, rank_filename, words_filename, max_results)
        for page, score in results:
            print(page, score)
        print("*"*10)
        exit(0)

    usage()
