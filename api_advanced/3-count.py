#!/usr/bin/python3
"""
Recursive function to count keywords from hot articles on Reddit.
"""

import requests


def count_words(subreddit, word_list, after='', counts=None):
    if counts is None:
        counts = {}
        word_list = [word.lower() for word in word_list]

    if after is None:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            if count > 0:
                print(f"{word}: {count}")
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        children = data['data']['children']
        for child in children:
            title = child['data']['title'].lower().split()
            for word in word_list:
                if word in title:
                    counts[word] = counts.get(word, 0) + 1
        after = data['data']['after']
        count_words(subreddit, word_list, after, counts)
    else:
        print("Invalid subreddit or no posts match.")


if __name__ == '__main__':
    subreddit = "unpopular"
    word_list = ['you', 'unpopular', 'vote', 'down', 'downvote', 'her', 'politics']
    count_words(subreddit, word_list)
