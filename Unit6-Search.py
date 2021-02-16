# Search Engine - Unit 6

import urllib

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def add_page_to_index(index,url,content):
    page = content.split()
    for keyword in page:
        add_to_index(index, keyword, url)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None

def lucky_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page

def compute_ranks(graph):
    d = 0.8 #damping factor
    numloops = 10 #number of timesteps
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for url in graph:
                if page in graph[url]:
                    newrank = newrank + d * (ranks[url] / len(graph[url]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def ordered_search(index, rank, keyword):
    pages = lookup(index, keyword)
    return quicksort_pages(pages, ranks)

def quicksort_pages(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]] #find pivot
        worse = []
        better = []
        for page in pages[1:]:
            if ranks[page] <= pivot:
                worse.append(page)
            else:
                better.append(page)
        return quicksort_pages(better, ranks) + [pages[0]] + quicksort_pages(worse, ranks)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {} #create empty graph
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content) #store all outlinks
            graph[page] = outlinks #add all outlinks to graph
            union(tocrawl, outlinks) #add all outlinks to tocrawl
            crawled.append(page)
    return index, graph
