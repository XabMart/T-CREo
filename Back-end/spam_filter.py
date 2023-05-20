from enum import Enum
import re
from better_profanity import profanity
import better_profanity
import json


class SimpleSpamFilter:
    def __init__(self, min_words=None, max_percent_caps=None, max_num_swear_words=None):
        self.min_words = min_words
        self.max_percent_caps = max_percent_caps
        self.max_num_swear_words = max_num_swear_words

    def is_spam(self, tweet, lang):
        if self.min_words is not None and len(tweet.split(' ')) < self.min_words:
            return 0

        if self.max_percent_caps is not None and percent_caps(tweet) > self.max_percent_caps:
            return 0

        if self.max_num_swear_words is not None and num_swear_words(tweet, lang) > self.max_num_swear_words:
            return 0

        return 100

    def load_config(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        self.min_words = config.get("min_words", None)
        self.max_percent_caps = config.get("max_percent_caps", None)
        self.max_num_swear_words = config.get("max_num_swear_words", None)

def percent_caps(tweet):
    cap_count = 0
    chars = list(tweet)

    for char in chars:
        if char == char.upper():
            cap_count += 1

    return (cap_count / len(tweet)) * 100

def num_swear_words(tweet, lang):
    profanity.load_censor_words(lang)
    def get_cleaned_words(text):
        return re.sub(r"[.|,|\n]", ' ', text).split(' ')

    cleaned_tweet_words = get_cleaned_words(tweet)
    swear_words_count = 0

    for word in cleaned_tweet_words:
        if profanity.contains_profanity(word):
            swear_words_count += 1

    return swear_words_count
