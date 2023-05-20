# -*- coding: utf-8 -*-
from spam_filter import SimpleSpamFilter
from bad_words_checker import badWordsProportion
from spell_checker import SpellCheckerWrapper
from general_utils import process_language
import json


with open("spam-config.json") as f:
    config = json.load(f)

spamFilter = SimpleSpamFilter()
spamFilter.load_config("spam-config.json")

with open("text-credibility-config.json") as f:
    config = json.load(f)

badWordsWeight = config.get('bad_words_weight')
spamWeight = config.get('spam_weight')
spellWeight = config.get('spell_errors_weight')


def textCredibility(text, lang):
    lang = process_language(lang)
    spamResult = spamFilter.is_spam(text, lang)
    badWordResult = badWordsProportion(text, lang)
    checker = SpellCheckerWrapper(language=lang)
    spellResult = checker.spellErrorProportion(text)
    textCredibility = spamResult * spamWeight + badWordResult * badWordsWeight + spellResult * spellWeight
    return textCredibility
