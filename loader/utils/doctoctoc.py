import urllib.request
from bs4 import BeautifulSoup
import json
import tweepy
from tweepy import OAuthHandler
import xlrd
import time
import random
from django.conf import settings
from hello.models import Question, Answer
from hello.utils.clean import clean_tweet

# https://twitter.com/DocteurePATATE/status/842360779454189568


class TwitterSearcher():
    def __init__(self, credentials):
        self.credentials = credentials
        self.auth = None
        self.api = None

    def authenticate(self):
        self.auth = OAuthHandler(self.credentials['ckey'], self.credentials['csecret'])
        self.auth.set_access_token(self.credentials['atoken'], self.credentials['asecret'])
        self.api = tweepy.API(self.auth)

    def search(self, query="#doctoctoc"):
        if self.api is None:
            self.authenticate()
        cur = tweepy.Cursor(self.api.search, q=query)
        i = 0
        for t in cur.items(200):
            i += 1
            print(i)
            print(t.text)


class TwitterScrapper():
    def __init__(self):
        self.num_url = 0
        self.num_url_succeed = 0
        self.num_url_failed = 0

    def parse_html(self, url):
        # Get all tweet-text(questions and replies) from a url of a tweet
        try:
            htmlfile = urllib.request.urlopen (url)
            htmltext = htmlfile.read()
            soup = BeautifulSoup (htmltext, "html.parser")
            #store id of tweet and user
            res = [i.p.get_text() for i in soup.find_all('div', class_= "js-tweet-text-container")]
        except Exception as e:
            print('Error with url, ', url)
            print(e)
            res = None
        if len(res) == 0:
            res = None
            print('Error with url, ', url)
        return res

    def question_answer_from_url(self, url):
        self.num_url += 1
        res = self.parse_html(url)
        if res is None:
            self.num_url_failed += 1
            print()
        else:
            q = Question(txt=res[0], src='twiiter_scrap')
            q.txt_clean, q.is_clean = clean_tweet(q.txt, remove_hashtags=True)
            q.save()
            if len(res)>1:
                for r in res[1:]:
                    a = Answer(txt=r, src='twiiter_scrap', question_id=q.pk)
                    a.txt_clean, a.is_clean = clean_tweet(a.txt, remove_hashtags=True)
                    a.save()
            self.num_url_succeed += 1
        return True

    def load_xls(self,path):
        max_num_questions = 1000 #Pour ne pas avoir trop de reponses a enlever si upgrade postgre heroku
        wb = xlrd.open_workbook(path)
        sh = wb.sheet_by_name(u'url')
        urls = sh.col_values(0)
        urls_use = urls[1:max_num_questions]
        liste_url = set(urls_use)
        liste_url = ['https://twitter.com' + i for i in liste_url if '/' in i]
        return liste_url

    def populate_from_xls(self, path):
        urls = TwitterScrapper.load_xls(self,path)
        for u in urls:
            res = self.question_answer_from_url(u)
            time.sleep(random.randint(0,2)) #sleep 2 sec pour pas se faire prendre par twitter
        return self.num_url_succeed, self.num_url_failed


def scrap_doctoctoc():
    path = 'loader/data/Excel_URL_Twitter_DocTocToc.xlsx'
    t = TwitterScrapper()
    res = t.populate_from_xls(path)
    print("Number urls succeed {}, Number urls failed {}".format(t.num_url_succeed, t.num_url_failed))


def start_listening(keywords):
    s = TwitterSearcher(settings.TWITTER_CREDENTIALS)
    s.authentificate()
    s.start_stream(keywords)


