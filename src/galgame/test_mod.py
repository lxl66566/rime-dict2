from . import remove_elements_after_non_letter


def test_remove_elements_after_non_letter():
    lst = ["apple", "banana", "123", "cherry", "date"]
    assert remove_elements_after_non_letter(lst) == ["apple", "banana"]
