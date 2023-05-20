from spellchecker import SpellChecker

class SpellCheckerWrapper:
    def __init__(self, language):
        self.spell = SpellChecker(language=language)

    def spellErrorProportion(self, text):
        words = text.split()
        word_amount = len(words)
        spell_error_words = self.spell.unknown(words)
        spell_error_amount = len(spell_error_words)
        spell_error_proportion = 100-(spell_error_amount / word_amount)*100
        return spell_error_proportion
