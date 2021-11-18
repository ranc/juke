import pickle
from operator import itemgetter
from typing import Dict


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


def search_pages(_query_list, _rank_filename, _words_filename, _max_results):
    page_ranks: Dict[str, int] = load_object(_rank_filename)
    words_count: Dict[str, Dict[str, int]] = load_object(_words_filename)
    sorted_page_ranks = set(sorted(page_ranks, key=page_ranks.get, reverse=True)[:_max_results])
    results = {}
    for query in _query_list:
        results[query] = []
        if query not in words_count:
            continue
        page_list = words_count[query]
        query_results = []
        for page, word_count in page_list.items():
            if page not in sorted_page_ranks:
                continue
            query_results.append((page, page_ranks[page] * word_count))
        if len(query_results) == 0:
            continue
        sorted_results = sorted(query_results, key=itemgetter(1), reverse=True)
        results[query] = sorted_results
    return results


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
        save_object(crawler.word_dict, out_file)
        print(crawler.word_dict)
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
        for q, res in results.items():
            if len(res) == 0:
                print("no results for", q)
            else:
                for page, score in res:
                    print(page, score)
            print("*"*10)
        exit(0)

    usage()
