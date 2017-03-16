import urllib.request
from bs4 import BeautifulSoup


# https://twitter.com/DocteurePATATE/status/842360779454189568



def parse_html(url):
    # url= 'https://twitter.com/doclamarre/status/840287127527141378'
    htmlfile = urllib.request.urlopen (url)
    htmltext = htmlfile.read ()
    soup = BeautifulSoup (htmltext, "html.parser")

    res = [i.p.get_text() for i in soup.find_all('div', class_= "js-tweet-text-container")]
    return res


