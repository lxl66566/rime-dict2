class Word:
    def __init__(self, word: str, spell: str):
        self.word = word
        self.spell = spell

    def __repr__(self):
        return f"{self.word}\t{self.spell}"

    def __str__(self):
        return self.__repr__()
