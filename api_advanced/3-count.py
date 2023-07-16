#!/usr/bin/python3
"""Module for the count_words function"""

import requests


def count_words(subreddit, word_list, after='', hot_list=None):
    """
    Recursive function that queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    if hot_list is None:
        hot_list = [0] * len(word_list)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return

    data = response.json()

    for topic in data['data']['children']:
        for word in topic['data']['title'].split():
            for i in range(len(word_list)):
                if word_list[i].lower() == word.lower():
                    hot_list[i] += 1

    after = data['data']['after']

    if after is not None:
        count_words(subreddit, word_list, after, hot_list)
    else:
        sorted_counts = sorted(zip(word_list, hot_list), key=lambda x: (-x[1], x[0]))

        for word, count in sorted_counts:
            if count > 0:
                print(f"{word.lower()}: {count}")


if __name__ == '__main__':
    subreddit = "unpopular"
    word_list = ['you', 'unpopular', 'vote', 'down', 'downvote', 'her', 'politics']
    count_words(subreddit, word_list)
