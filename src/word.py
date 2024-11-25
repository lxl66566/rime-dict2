from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    word: str
    spell: str

    def __repr__(self):
        return f"{self.word}\t{self.spell}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, value: object) -> bool:
        assert isinstance(value, Word), "只能比较两个 Word 对象，不能比较其他类型的对象"
        return (self.word, self.spell) == (value.word, value.spell)
