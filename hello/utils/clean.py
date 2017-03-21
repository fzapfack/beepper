import re


def clean_tweet(txt, remove_hashtags=False):
    # Remove @ and pics
    clean1 = re.sub('@\w+', '', txt)
    clean = re.sub('pic.twitter.com[^\s]*', '', clean1)
    if remove_hashtags:
        clean = re.sub('#\w+', '', clean)
        good = True
    else:
        clean = re.sub('#[dD][oO][cC][tT][oO][cC]\w+', '', clean)
        a = re.findall('#\w+', txt)
        good = len(a)>0
    return clean, good