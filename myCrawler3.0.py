# th3xer0's  Web Crawler - 5.0
# Usage:
# index || crawled = crawl_web('seed_url', max_pages, max_depth, 'i' || 'c')
# index || crawled = crawl_web('http://www.dtctechnology.com', 100, 5, 'i')
# lookup = lookup(index, keyword)


import urllib #import urllib (for get_page)

def get_page(url): #procedure to read in a webpage at specified url
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page): #procedure to find find next link in page
    start_link = page.find('<a href=')  #find the first hyperlink
    if start_link == -1: #catch no link found
        return None, 0 #returns for no link found
    start_quote = page.find('"', start_link) #find the opening quote of link
    end_quote = page.find('"', start_quote+1) #find the closing quote of link
    url = page[start_quote+1:end_quote] # store the url (between quotes)
    return url, end_quote #return url and end_quote (to find next part of page)


def get_all_links(page): #procedure to loop get_next_target, while links exist
    links = [] #initialize links list to Null
    while True: #starts loop, sets to repeat until break
        url, endpos = get_next_target(page) #calls get_next_target, assigns output
        if url: #checks for a valid url
            links.append(url) #adds url to linkList
            page = page[endpos:] #advances page (input)
        else: #catches None (null) url
            break #breaks loop
    return links


def union(p,q): #procedure to union append lists
    for e in q: #loop through all elements in list
        if e not in p: #check for element in q that is already in p
            p.append(e) #append all unique elements in q to p


def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword,[url]])


def add_page_to_index(index,url,content):
    page = content.split()
    for keyword in page:
        add_to_index(index, keyword, url)


def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword
            return entry[1]
    return []

def crawl_web(seed, max_pages, max_depth, iorc):
    tocrawl = [[seed, 0]] #populate tocrawl list with seed url
    crawled = []
    index = [] #initialize index - blank
    while tocrawl and len(crawled) < max_pages:
        page, depth = tocrawl.pop() #set page to last url in tocrawl list, remove from list
        if page not in crawled and depth <= max_depth:
            content = get_page(page)
            add_page_to_index(index, page, content)
            #union(tocrawl, get_all_links(content)) #call procedure to union lists
            for link in get_all_links(content):
                tocrawl.append([link, depth + 1])
            crawled.append(page) #update crawled list with url just crawled
    if iorc == 'i' or iorc == 'I':
        return index #return index of crawled pages
    if iorc == 'c' or iorc == 'C':
        return crawled #return list of crawled pages
    else:
        return index #return index of crawled pages

# Usage:
# index = crawl_web('seed_url', max_pages, max_depth, 'i' || 'c')
# index = crawl_web('http://www.dtctechnology.com', 100, 5, 'i')

