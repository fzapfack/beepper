import re


def clean_tweet(txt, remove_hashtags=False):
    # remove pic links
    clean = re.sub(r'pic.twitter\S+', '', txt)
    # clean1=txt.split('pic.twitter')[0]
    # Remove @
    clean = re.sub('@\w+', '', clean)
    # Remove #
    if remove_hashtags:
        clean = re.sub('#\w+', '', clean)
        good = True
    else:
        clean = re.sub('#[dD][oO][cC][tT][oO][cC]\w+', '', clean)
        a = re.findall('#\w+', txt)
        good = len(a) > 0
    return clean, good

    return True