#   Program: xer0Find
#   File: xer0Find-Main
#   Version: 1.0-beta
#   Written by: th3xer0 - th3xer0@gmail.com *aka* Ben Feld - benwfeld@gmail.com
#
#   This progrm is a web crawler and search engine written by th3xer0
#   This insparation and base code for this program came from Udacity"s CS101 Course (1st hexamester / ? 2012)
#   I would encourage anyone reading this to check out Udacity @ www.udacity.com
#   I would also like to give a special thanks to Dave Evans at Udacity, for his awesomeness.
#
#   Cool Features in this program:
#   -Ability to resume / continue previous crawls
#   -Functional logging (to a file)
#   -File I/O
#
#   Features to Add / Improve:
#   -Incorporate Robots.txt functionality
#   -Refine the content split (of web page content)
#
#   Things that could be improved:
#   -Better OOP, use of objectes
#   -Better use of functions to reduce code reuse
#
#   *COPYRIGHT (C) 2012 th3xer0, under the GUN General Public License:*
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Imports
# I am trying not to use any third party libraries, as this was a CS101 class and I am learning as I go.
# I want to completely understand HOW and WHY my code works.  This is a learning experience.
# However, some built in Python libraries are necessary.
import os
import sys
import time
import shelve
import cPickle
import urllib

# Set version
version = "1.0-beta"

# Determine OS
platform = os.name

# Set Arguments:
args = []
if len(sys.argv[1:]) == 2:
    for arg in sys.argv[1:]:
        args.append(arg)

# Initialize Screen, per OS
# Called from Main Entry into the program
def initialize():
    if platform == "posix":
        os.system("clear")
        uos = "Linux"
    elif platform == "nt":
        os.system("cls")
        uos = "Windows"
    elif platform == "os2":
        uos = "Mac"
        print "Sorry this program does not yet support Mac!, but you should not have made it here."
        sys.exit()
    start(uos)

# Begin Program (where no command line args are passed in)
# Called from initalize
def start(uos):
    print "Welcome to xer0Find"
    print "Version:" + " " + version
    print "Your OS Platform is:" + " " + uos + "\n"
    if not args:
        usage()
        sys.exit()
    if args[0] == "crawl":
        crawl(uos)
    if args[0] == "query":
        query(uos)
    if args[0] == "dump":
        dump(uos)
    if args[0] != "crawl" and args[0] != "query" and args[0] != "dump":
        usage()

# Display Usage Instructions
# Called from start and query (as I/O exception)
def usage():
    print """Usage:

python xer0Find_""" + version + ".py" + """ [crawl | query] [crawlDirectory | queryDirectory]

crawl  -- begin a crawl
query  -- run a query
crawlDirectory  -- absolute path of a directory to store a crawl
queryDirectory  -- absolute path of a directory that holds a crawl

crawl e.g:  python xer0Find_""" + version + ".py" + """ crawl /home/user/crawls/
query e.g:  python xer0Find_""" + version + ".py" + """ query /home/user/crawls/""" + "\n"

# Crawl Mode Entry
# Called from start
def crawl(uos):
    print "Option: Cralw\n"
    if uos == "Linux":
        slash = "/"
    if uos == "Windows":
        slash = "\\"
    if os.path.isdir(args[1]):
        print args[1] + " is a valid directory!\n"
        if args[1][-1] != slash:
            crawlPath = args[1] + slash
        else:
            crawlPath = args[1]
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write("\n\n" + runtime + " - xer0Find called from the command line. " + str(args) + "\n")
            log.write(runtime + " User OS: " + uos + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + crawlPath + " is a valid directory.\n")
            log.close()
        except:
            print "Error: Log file write exception. (crawl, set crawlPath)"
    else:
        print "Not a valid directory."
        sys.exit()
    # Check for existing crawl in the valid directory
    existingCrawl = True
    if not os.path.isfile(crawlPath + "crawl.xfd"):
        existingCrawl = False
    if not os.path.isfile(crawlPath + "config.xfd"):
        existingCrawl = False
    if existingCrawl:
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "A previous crawl exists within this directory.\n")
            log.close()
        except:
            print "Error: Log file write exception. (crawl, existingCrawl)"
        print "A previous crawl exists within this directory.\n"
        print "You may choose to continue with the existing crawl, or begin a new crawl within this directory.\n"
        print "If you choose to begin a new crawl within this directory, your existing crawl will be lost.\n"
        print "Alternatively, you may begin a new crawl within a new directory and still maintain the crawl within this directory.\n"
        userInput = False
        while not userInput:
            continueYN = raw_input("Would you like to continue with your exitsing crawl? (y/n) ")
            if continueYN == 'y':
                print "\n\nContinuing Previous Crawl\n"
                userInput = True
                try:
                    log = open(crawlPath + "log.xfd.txt", "a")
                    log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "User elects to continue previous crawl.\n")
                    log.close()
                except:
                    print "Error: Log file write exception. (crawl, userContinueCrawl)"
                continueCrawl(crawlPath)
            if continueYN == 'n':
                print "\n\nBeginning New Crawl\n"
                userInput = True
                try:
                    log = open(crawlPath + "log.xfd.txt", "a")
                    log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "User elects to begin new crawl.\n")
                    log.close()
                except:
                    print "Error: Log file write exception. (crawl, userContinueCrawl)"
                newCrawl(crawlPath)
    else:
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "There is no existing crawl within this directory.\n")
            log.close()
        except:
            print "Error: Log file write exception. (crawl, no existingCrawl)"
        print "There is no existing crawl within this directory.\n"
        newCrawl(crawlPath)

# Continue Saved Crawl
# Called from crawl
def continueCrawl(crawlPath):
    print "Importing previous crawl config...\n"
    # NO ERROR DETECTION / INPUT VALIDATION HERE - SHOULD ADD LATER
    # Any errors in saved config file here can cause catastrophic program failure later
    try:
        log = open(crawlPath + "log.xfd.txt", "a")
        configFile = open(crawlPath + "config.xfd", "r")
        config = cPickle.load(configFile)
        crawlFile = shelve.open(crawlPath + "crawl.xfd")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Config imported from file.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Seed: " + config["seed"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Pages: " + config["maxPages"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Depth: " + config["maxDepth"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Time: " + config["maxTime"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl imported.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Pages Crawled Count: " + str(len(crawlFile["crawled"])) + "\n")
        log.close()
        configFile.close()
    except:
        print "Error: Log file write exception. (newCrawl, setConfig)"
    print "Imported config:"
    # Print Config
    configFile = open(crawlPath + "config.xfd", "r")
    config = cPickle.load(configFile)
    print "Seed: " + config["seed"]
    print "Max Pages: " + config["maxPages"]
    print "Max Depth: " + config["maxDepth"]
    print "Max Time: " + config["maxTime"]
    print "Pages Crawled: " + str(len(crawlFile["crawled"]))
    print "Pages to Crawl: " + str(len(crawlFile["tocrawl"]))
    configFile.close()
    crawlFile.close()
    userInput = False
    while not userInput:
        changeYN = raw_input("\nWould you like to change any of these config settings? (y/n) ")
        if changeYN == 'y':
            userInput = True
            # Change configs here
            config["seed"] = raw_input("Seed: ")
            config["maxPages"] = raw_input("Max Pages: ")
            config["maxDepth"] = raw_input("Max Depth: ")
            config["maxTime"] = raw_input("Max Time (minutes): ")
            # configFile = open(crawlPath + "config.xfd", "w")
            # cPickle.dump(config, configFile)
            # configFile.close()
            # configFile = open(crawlPath + "config.xfd", "r")
            # config = cPickle.load(configFile)
            # configFile.close()
            configFile = open(crawlPath + "config.xfd", "w")
            cPickle.dump(config, configFile)
            configFile.close()
            try:
                log = open(crawlPath + "log.xfd.txt", "a")
                configFile = open(crawlPath + "config.xfd", "r")
                config = cPickle.load(configFile)
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "User elects to change previous config settings.\n")
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Seed: " + config["seed"] + "\n")
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Pages: " + config["maxPages"] + "\n")
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Depth: " + config["maxDepth"] + "\n")
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Time: " + config["maxTime"] + "\n")
                log.close()
                configFile.close()
            except:
                print "Error: Log file write exception. (continueCrawl, userSettingsChanged)"
        if changeYN == 'n':
            userInput = True
            #continue on unchanged
            seedChangeForced = False
            seedChanged = False
            crawlFile = shelve.open(crawlPath + "crawl.xfd")
            while not crawlFile["tocrawl"] and not seedChanged:
                seedChangeForced = True
                seedChanged = True
                print "There are no pages left to crawl in the imported crawl.\n"
                print "Please specify a new seed."
                config["seed"] = raw_input("Seed: ")
                configFile = open(crawlPath + "config.xfd", "w")
                cPickle.dump(config, configFile)
                configFile.close()
            try:
                log = open(crawlPath + "log.xfd.txt", "a")
                log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "User elects to continue with previous config settings.\n")
                if seedChangeForced:
                    log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "There are no pages left to crawl in the imported crawl.  Seed changed forced.\n")
                    log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Seed: " + config["seed"] + "\n")
                log.close()
            except:
                print "Error: Log file write exception. (continueCrawl, userSettingsUnchanged)"
    configFile.close()
    crawlFile.close()
    crawl_web(crawlPath)

# Begin New Crawl
# Called from crawl
def newCrawl(crawlPath):
    print "To begin a new crawl, please enter the following information:"
    # NO ERROR DETECTION / INPUT VALIDATION HERE - SHOULD ADD LATER
    # Any errors in user input here can cause catastrophic program failure later 
    seed = raw_input("Seed: ")
    maxPages = raw_input("Max Pages: ")
    maxDepth = raw_input("Max Depth: ")
    maxTime = raw_input("Max Time (minutes): ")
    newConfig = {"seed": seed, "maxPages": maxPages, "maxDepth": maxDepth, "maxTime": maxTime}
    try:
        # Save config file
        configFile = open(crawlPath + "config.xfd", "w")
        cPickle.dump(newConfig, configFile)
        configFile.close()
        # Save crawl (to a shelf)
        crawlFile = shelve.open(crawlPath + "crawl.xfd")
        crawlFile["tocrawl"] = []
        crawlFile["crawled"] = []
        crawlFile["index"] = {}
        crawlFile["graph"] = {}
        crawlFile.sync()
        crawlFile.close()
    except:
        print "Error: Config, crawl write exception. (newCrawl, storeConfig)"
    try:
        log = open(crawlPath + "log.xfd.txt", "a")
        configFile = open(crawlPath + "config.xfd", "r")
        config = cPickle.load(configFile)
        crawlFile = shelve.open(crawlPath + "crawl.xfd")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Config set by user.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Seed: " + config["seed"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Pages: " + config["maxPages"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Depth: " + config["maxDepth"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Time: " + config["maxTime"] + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl created.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawled: " + str(crawlFile["crawled"]) + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Index: " + str(crawlFile["index"]) + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Graph: " + str(crawlFile["graph"]) + "\n")
        log.close()
        configFile.close()
        crawlFile.close()
    except:
        print "Error: Log file write exception. (newCrawl, setConfig)"
    crawl_web(crawlPath)

# Actual Crawl Function
# This should look familiar from Udacity CS101
# Called from continueCrawl and newCrawl
def crawl_web(crawlPath): #instead of just seed
    print "\nBeginning crawl."
    configFile = open(crawlPath + "config.xfd", "r")
    config = cPickle.load(configFile)
    crawlFile = shelve.open(crawlPath + "crawl.xfd")
    # Load variables from crawlFile, so we do not need to keep reading / writing file
    if not crawlFile["tocrawl"]:
        tocrawl = crawlFile["tocrawl"]
        tocrawl.append([config["seed"], 0])
    else:
        tocrawl = crawlFile["tocrawl"]
        tocrawl.append([config["seed"], 0])
    crawled = crawlFile["crawled"]
    index = crawlFile["index"]
    graph = crawlFile["graph"]
    secondsToCrawl = int(config["maxTime"]) * 60
    crawlStartTime = time.time()
    crawlEndTime = crawlStartTime + secondsToCrawl
    crawlStartTimeLog = time.strftime("%Y-%m-%d_%H:%M:%S")
    keepCrawling = int(config["maxPages"])
    crawlCount = 0
    oldCrawlCount = len(crawled)
    try:
        log = open(crawlPath + "log.xfd.txt", "a")
        log.write(crawlStartTimeLog + " - " + "Crawl begins.\n")
        log.close()
    except:
        print "Error: Log file write exception. (crawl_web, crawlBegins)"
    while keepCrawling and tocrawl and time.time() < crawlEndTime:
        page, depth = tocrawl.pop()
        # Allow LinkedIn:
        if page not in crawled and depth <= config["maxDepth"]:
        # LinkedIn Killer (in a test run, LinkedIn URLs accounted for 4112/10000 pages crawled):
        #if page not in crawled and depth <= config["maxDepth"] and page.find("linkedin") == -1:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            for link in outlinks:
                tocrawl.append([link, depth + 1])
            crawled.append(page)
            crawlCount += 1
            keepCrawling -= 1
    crawlEndTime = time.time()
    crawlEndTimeLog = time.strftime("%Y-%m-%d_%H:%M:%S")
    # Save Crawl
    crawlFile["tocrawl"] = tocrawl
    crawlFile["crawled"] = crawled
    crawlFile["index"] = index
    crawlFile["graph"] = graph
    crawlFile.sync()
    try:
        log = open(crawlPath + "log.xfd.txt", "a")
        log.write(crawlEndTimeLog + " - " + "Crawl ends.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl Time Max (minutes): " + config["maxTime"] + "\n")
        if crawlEndTime - crawlStartTime < 60:
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl Time Elapsed (seconds): " + str(crawlEndTime - crawlStartTime) + "\n")
        else:
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl Time Elapsed (minutes): " + str((crawlEndTime - crawlStartTime) / 60) + "\n")
        if crawlCount != len(crawled) - oldCrawlCount:
            print "Crawled count error!"
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawled count error: crawlCount (" + str(crawlCount) + ")" + " != len(crawled) (" + str(len(crawled)) + ")" + "\n")
        else:
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Pages Crawled Count: " + str(crawlCount) + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawled Pages (Total): " + str(len(crawled)) + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Not Crawled: " + str(len(tocrawl)) + "\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Config saved to disk.\n")
        log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl saved to disk.\n")
        log.close()
        configFile.close()
        crawlFile.close()
    except:
        print "Error: Log file write exception. (crawl_web, crawlCompleted)"
    configFile.close()
    crawlFile.close()

# Reads in the webpage
# Called from / returns to crawl_web
def get_page(url): #procedure to read in a webpage at specified url
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

# Splits page content and calls add_to_index for each keyword
# Called from / returns to crawl_web
def add_page_to_index(index,url,content):
    # Want to update split to function better
    page = content.split()
    for keyword in page:
        add_to_index(index, keyword, url)

# Creates/appends a URL entry in index for each keyword
# Called from / returns to add_page_to_index
def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

# Finds all links within a given page (within oage content), uses get_next_target to find each successive link
# Called from / returns to crawl_web
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

# Finds one link at a time and passes it back to get_all_links
# Called from / returns to get_all_links
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1:end_quote]
    return url, end_quote

# Query Mode Entry
# Called from start
def query(uos):
    print "Option: Query\n"
    try:
        if os.path.isfile(args[1]):
            print args[1] + " is a valid file!\n"
        else:
            print "Not a valid file."
    except:
        print "Exception!"
        print usage()

# Data Dump Mode
# Called from start
def dump(uos):
    print "Option: Dump\n"
    if uos == "Linux":
        slash = "/"
    if uos == "Windows":
        slash = "\\"
    if os.path.isdir(args[1]):
        print args[1] + " is a valid directory!\n"
        if args[1][-1] != slash:
            crawlPath = args[1] + slash
        else:
            crawlPath = args[1]
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write("\n\n" + runtime + " - xer0Find called from the command line. " + str(args) + "\n")
            log.write(runtime + " User OS: " + uos + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + crawlPath + " is a valid directory.\n")
            log.close()
        except:
            print "Error: Log file write exception. (dump, set crawlPath)"
    else:
        print "Not a valid directory."
        sys.exit()
    # Check for existing crawl in the valid directory
    existingCrawl = True
    if not os.path.isfile(crawlPath + "crawl.xfd"):
        existingCrawl = False
    if not os.path.isfile(crawlPath + "config.xfd"):
        existingCrawl = False
    if existingCrawl:
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "A previous crawl exists within this directory.  Dump possible.\n")
            log.close()
        except:
            print "Error: Log file write exception. (dump, existingCrawl)"
        print "A previous crawl exists within this directory.  Dump possible.\n"
        print "Importing previous crawl config...\n"
        # NO ERROR DETECTION / INPUT VALIDATION HERE - SHOULD ADD LATER
        # Any errors in saved config file here can cause catastrophic program failure later
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            configFile = open(crawlPath + "config.xfd", "r")
            config = cPickle.load(configFile)
            crawlFile = shelve.open(crawlPath + "crawl.xfd")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Config imported from file.\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Seed: " + config["seed"] + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Pages: " + config["maxPages"] + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Depth: " + config["maxDepth"] + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Max Time: " + config["maxTime"] + "\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Crawl imported.\n")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "Pages Crawled Count: " + str(len(crawlFile["crawled"])) + "\n")
            log.close()
            configFile.close()
        except:
            print "Error: Log file write exception. (newCrawl, setConfig)"
        print "Imported config:"
        # Print Config
        configFile = open(crawlPath + "config.xfd", "r")
        config = cPickle.load(configFile)
        print "Seed: " + config["seed"]
        print "Max Pages: " + config["maxPages"]
        print "Max Depth: " + config["maxDepth"]
        print "Max Time: " + config["maxTime"]
        print "Pages Crawled: " + str(len(crawlFile["crawled"]))
        print "Pages to Crawl: " + str(len(crawlFile["tocrawl"]))
        print "\nConfig: " + str(config) + "\n"
        ##HERE##
        userInput = False
        while not userInput:
            toDump = raw_input("What would you like to dump? (tocrawl, crawled, index, graph): ")
            if toDump == "tocrawl":
                userInput == True
                print str(crawlFile["tocrawl"])
            if toDump == "crawled":
                userInput == True
                #print str(crawlFile["crawled"])
                for item in crawlFile["crawled"]:
                    print item
            if toDump == "index":
                userInput == True
                print str(crawlFile["index"])
            if toDump == "graph":
                userInput == True
                print str(crawlFile["graph"])
            else:
                userInput = False
        configFile.close()
        crawlFile.close()
    else:
        try:
            log = open(crawlPath + "log.xfd.txt", "a")
            log.write(time.strftime("%Y-%m-%d_%H:%M:%S") + " - " + "There is no existing crawl within this directory.  Nothing to dump.\n")
            log.close()
        except:
            print "Error: Log file write exception. (dump, no existingCrawl)"
        print "There is no existing crawl within this directory.  Nothing to dump.\n"

# Main Entry into the program
# When program is called from the command line, this will run first
if __name__ == "__main__":
    runtime = time.strftime("%Y-%m-%d_%H:%M:%S")
    try:
        if platform == "posix" or platform == "nt":
            initialize()
        elif platform == "os2":
            # OSX should work (possibly requiring minor tweaking), but I do not have a Mac to test on
            # Once this program is completed (or functioning), I will attempt to get it working on Mac
            print "Sorry this program does not yet support Mac!"
            sys.exit()
        else:
            print "Unknown OS:" + " " + platform
    # May remove this as I do not this it will catch anything properly
    except KeyboardInterrupt:
        print "User stopped xer0Find"
