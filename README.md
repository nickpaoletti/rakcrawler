Rakuten crawler (SUPER ALPHA): I love browsing through Rakuten global market for great deals on clothes.

Unfortunately, clicking through pages of pages of items for only a few to be my size can be a very time consuming endeavour.

I created this crawler to help ease the process - returning a list of links of items that match a given size given a certain query.

Of course, the results are never guaranteed perfect - machine translation can make some odd items show up given a query. However,
it's still a great starting point.

For this base implementation, it crawls two of my favorite global market stores - kanful and kind-u. I will only have this crawler
browse known stores, as each have very different formatting for where the size is marked, something in which I code in manually.

USAGE:

py rakcrawler.py -brand -size

Be sure to put multi word brands in quotes. ex:

py rakcrawler.py "engineered garments" m