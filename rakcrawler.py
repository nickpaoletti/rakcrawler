from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

from bs4 import BeautifulSoup
import requests
import re
import argparse

#Thank you to https://docs.python.org/3.3/howto/argparse.html#id1

parser = argparse.ArgumentParser()
#brand and size are mandatory arguments
parser.add_argument("brand", help="Brand name you want to search")
parser.add_argument("size", help="Your size")
#note - many sizes are marked 0-5, others US sizing, others, IT sizing. for this reason, I do not have this strictly as xs/s/m/l, etc.
args = parser.parse_args()

matches = []

def getItems(store):
    
    page = 1
    success = True

    #Keep grabbing the next page results until no more results are left
    while(success):
        print("Parsing page # " + str(page) + " of results of store " + store + "...")

        #following URL is the search function, viewing 60 items (max) at once - grab data from that
        url = 'http://global.rakuten.com/en/search/?sm=3&p=' + str(page) + '&h=3&k=' + args.brand.replace(" ", "+") + '&l-id=gs_product_search&sid=' + store
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        #The following is the class of the div that holds the "No results" message.
        if soup.find(class_="b-mod-panel b-color-def b-text-def") == None:

            #specialized methods for each store.
            #TO DO - implement ragtag, another major store. 
            if store == 'kind-u':
                findKind(soup)
            elif store == 'kanful':
                findKanful(soup)

            #since this page exists, onto the next
            page = page + 1

        else:
            #If the 'no results' message comes up, we stop parsing that store.
            success = False

#to do - finditems with only one argument - polymorphism :) Just checks titles for kind ones.

def findKind(soup):

    #kind-u actually encodes the size in the title of the link to the item. This way we don't have to visit the item, just check the link.
    for match in soup.find_all(is_link, href=re.compile("^/en/store/kind-u/item/")):
        if match.string.find('size: ' + args.size.lower()) != -1: #size is always marked as lowercase
            matches.append({match.get('href') : match.string}) 

# For kanful
def findKanful(soup):

    #kanful is more difficult and n complexity times slower - n being # of items.
    #Visit each link to check the page for the size.
    for match in soup.find_all(is_link, href=re.compile("^/en/store/kanful/item/")):
        #Each link to an item must be visited.
        response = requests.get("http://global.rakuten.com" + match['href'])
        soup = BeautifulSoup(response.text, "html.parser")
        
        try:
            #If size is not marked blank
            if len(soup.find("td", id="item_size").contents) > 1:

                size = soup.find("td", id="item_size").contents[1]
                title = soup.find(class_="b-ttl-main").string

                #Check against size given in argument. kanful sizing is marked as CAPS.
                if size == args.size.lower().upper():
                    matches.append({match['href'] : title})

        except AttributeError: #If there is no size field at all, we need to gloss over this.
            pass

def is_link(tag):
    return tag.parent.get('class') == ['b-content', 'b-fix-2lines']

getItems('kind-u') #Parse through results from kind-u
getItems('kanful') #Parse through results from kanful
print(matches)