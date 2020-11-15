import json
import scholarly
import sys


def show_matching_papers(title: str) -> list:
    search_query = scholarly.scholarly.search_pubs(title)
    matched_papers: list = []
    continue_iteration: bool = True
    ctr: int = 0
    while continue_iteration:
        try:
            matched_papers.append(next(search_query))
            ctr += 1
            if ctr > 10:
                continue_iteration = False
        except StopIteration:
            continue_iteration = False

    return matched_papers


if __name__ == '__main__':
    query: str = " ".join(sys.argv[1:])
    papers_info: list = show_matching_papers(query)
    paper_titles = dict(items=[])
    paper_titles["items"] = [{"title": pi.bib["title"],
                              "subtitle": ", ".join(pi.bib["author"]),
                              "arg": pi.bibtex} for i, pi in enumerate(papers_info)]
    paper_titles = json.dumps(paper_titles)
    print(paper_titles)
