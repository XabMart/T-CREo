# -*- coding: utf-8 -*-
from datetime import datetime, date
from spam_filter import SimpleSpamFilter
from bad_words_checker import badWordsProportion
from spell_checker import SpellCheckerWrapper
from general_utils import process_language
import json



def followersImpact(followers_count,friends_count):
    max_followers = 2000000
    result = (min(followers_count, max_followers) / max_followers) * 50
    return result

    
def followerProportion(followers_count,friends_count):
    if followers_count + friends_count == 0:
        result = 0
    else:
        result = (followers_count / (followers_count + friends_count)) * 50
    return result
    
def socialCredibility(followers_count,friends_count):
    socialCredibility = followersImpact(followers_count,friends_count) + followerProportion(followers_count,friends_count)
    return socialCredibility

def verification(verified):
    if verified:
        result = 50
    else:
        result = 0
    return result

def creation_weight(account_creation):
    try:
        # Intenta analizar la fecha con el formato '%Y-%m-%dT%H:%M:%S.%fZ'
        creation = datetime.strptime(account_creation, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        try:
            # Intenta analizar la fecha con el formato '%Y-%m-%d %H:%M:%S%z'
            creation = datetime.strptime(account_creation, '%Y-%m-%d %H:%M:%S%z')
        except ValueError:
            # Si no se puede analizar la fecha en ninguno de los formatos, devuelve un valor predeterminado
            return 0

    current_year = date.today().year
    result = ((current_year - creation.date().year) / (current_year - 2006)) * 50
    return result

def userCredibility(verified, account_creation):
    verification_result = verification(verified)
    creation_weight_result = creation_weight(account_creation)
    return verification_result + creation_weight_result

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




def credibility(text_credibility,social_credibility,user_credibility):
    with open("credibility-config.json") as f:
        config = json.load(f)
    textWeight = config.get('text_credibility_weight')
    userWeight = config.get('user_credibility_weight')
    socialWeight = config.get('social_credibility_weight')
    credibility = social_credibility*socialWeight + user_credibility*userWeight + text_credibility*textWeight
    return credibility