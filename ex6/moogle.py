import pickle


def usage():
    print("usage:")
    print(sys.argv[0], "crawl <base_url> <index_file> <out_dict_file>")
    print(sys.argv[0], "page_rank <iterations> <dict_file> <out_file>")
    exit(-1)


def save_object(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)


def load_object(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


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
        word_count = counter.start_counting()
        save_object(word_count, out_file)
        exit(0)

    usage()
