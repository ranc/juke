from typing import Dict


# Calculate total number of links going out of a document
def calc_links_from(word_dict: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    res = {}
    for from_doc, links in word_dict.items():
        res[from_doc]=0
        for to_doc, count in links.items():
            res[from_doc] += count
    return res


def rank_pages(word_dict: Dict[str, Dict[str, int]], iterations) -> Dict[str, int]:
    total_links_from = calc_links_from(word_dict)
    page_ranks = dict((page, 1) for page in total_links_from.keys())
    for _ in range(iterations):
        new_page_ranks = {}
        for page_j in word_dict.keys():
            new_page_ranks[page_j] = 0
            for page_i, link_i_to_all in word_dict.items():
                if page_j not in link_i_to_all:
                    continue
                num_links_i_to_j = link_i_to_all[page_j]
                new_page_ranks[page_j] += page_ranks[page_i]*num_links_i_to_j/total_links_from[page_i]

        page_ranks = new_page_ranks
    print(page_ranks)
    return page_ranks
