from . import extract_line, process_pinyin


def test_extract_line():
    a, b = extract_line(
        "五步蛇 五步蛇 [wu3 bu4 she2] /Deinagkistrodon acutus, a species of "
    )
    assert a == "五步蛇"
    assert b == "wu3 bu4 she2"


def test_process_pinyin():
    pinyins = ["zhi1", "wo2 lu:4"]
    answers = ["zhi", "wo lv"]
    for i in range(len(pinyins)):
        assert process_pinyin(pinyins[i]) == answers[i]
