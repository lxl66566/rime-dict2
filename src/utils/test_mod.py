from . import keep_ascii


def test_keep_ascii():
    assert keep_ascii("中文") == ""
    assert keep_ascii("你好，Hello World! 🌍") == ",Hello World! "
