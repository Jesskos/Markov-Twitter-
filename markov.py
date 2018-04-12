"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    init_words = choice(chains.keys()) 
    words = list(init_words)
    while True:
        try:
            key = tuple(words[-2:])
            value = choice(chains[key])
            words.append(value)
            joined_words = " ".join(words)
            if len(joined_words) >= 120:
                break
        except KeyError:
            break
    return joined_words

def tweet(chains):
    """Create a tweet and send it to the Internet."""

    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    status = api.PostUpdate(chains)
    print status.text
    

def get_users_tweets(words):

    while True: 
        users_string = raw_input("Enter a Tweet, or q to quit")
        if users_string == "q":
            break 
        else: 
            new = make_text(words)
            tweet(new)



# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(['green-eggs.txt'])

# Get a Markov chain
chains = make_chains(text)
tweet_word = make_text(chains)
# # Your task is to write a new function tweet, that will take chains as input
tweet(tweet_word)
get_users_tweets(chains)