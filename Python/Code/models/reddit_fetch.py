#! /usr/bin/env python

import praw
from time import sleep

limit = 100
filename = 'stories.txt'

def get_content(name, agent):
    texts = list()
    reddit = praw.Reddit(user_agent = agent)
    subreddit = reddit.get_subreddit(name)
    submissions = subreddit.get_hot(limit = limit)
    for x in submissions:
        texts.append(x.title)
    print "Fetched " + str(len(texts)) + " submissions for " + name + "..."
    return list(set(texts))

def get_depressed():
    return get_content('depression', 'Depressed User Agent')

def get_happy():
    return get_content('happy', 'Happy User Agent')

def get_suicide_watch():
    return get_content('suicidewatch', 'Suicide Watch User Agent')

def main():
    stories = get_depressed() + get_happy() + get_suicide_watch()
    print "Writing to " + filename + "..."
    f = open(filename, 'w')
    for story in stories:
        f.write(story.encode('utf-8'))
        f.write("\n")
    f.close()
    print "Done!"

if __name__ == "__main__":
    main()

