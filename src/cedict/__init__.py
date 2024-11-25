import logging as log
import re
import tempfile
from pathlib import Path

from ..utils import download_to, extract
from ..word import Word


def contains_chinese(text):
    """
    判断字符串内是否包含中文
    """
    # 使用正则表达式匹配汉字
    pattern = re.compile(r"[\u4e00-\u9fff]")
    match = pattern.search(text)
    return bool(match)


def all_are_chinese(text: str) -> bool:
    """
    判断字符串是否完全由中文组成
    """
    for char in text:
        if not "\u4e00" <= char <= "\u9fff":
            return False
    return True


def extract_line(text: str) -> tuple[str | None, str | None]:
    """
    提取出一行内的汉字与拼音
    """
    pattern = re.compile(r"\s(\S+)\s\[([^]]+)\]")
    match = pattern.search(text)

    if match:
        return match.group(1), match.group(2)
    else:
        log.error(f"无法提取出汉字与拼音：{text}")
        return None, None


def process_pinyin(text: str):
    """
    处理拼音，将形如 wu3 bu4 she2 转为 wu bu she
    """

    # 将拼音分割为单个字符串
    pinyin = text.split(" ")
    for i in range(len(pinyin)):
        if pinyin[i][-1].isdigit():
            pinyin[i] = pinyin[i][:-1]

        if pinyin[i].endswith("u:"):
            pinyin[i] = f"{pinyin[i][:-2]}v"

        pinyin[i] = pinyin[i].lower()

    return " ".join(pinyin)


def parse_cedict(text: str):
    """
    处理整个文件
    """
    comment: list[str] = []
    words: list[Word] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            comment.append(line)
            continue
        word, spell = extract_line(line)
        assert (
            word is not None and spell is not None
        ), "无法提取出汉字与拼音：{}".format(line)
        if not all_are_chinese(word):
            log.warning(f"单词不完全由汉字组成，跳过：{word}")
            continue

        words.append(Word(word, process_pinyin(spell)))
    return comment, words


def main():
    cedict_zip_path = download_to(
        "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip",
        Path(tempfile.gettempdir()) / "cedict.zip",
    )
    cedict_path = extract(cedict_zip_path)
    cedict_content = (cedict_path / "cedict_ts.u8").read_text(encoding="utf-8")
    comment, words = parse_cedict(cedict_content)
    log.info(f"已处理 {len(comment)} 条注释， {len(words)} 个单词")

    output = []
    output.extend(comment)
    output.append("")
    output.extend(map(str, words))
    output_text = "\n".join(output)
    Path("CEDICT.dict.yaml").write_text(output_text, encoding="utf-8")
    log.info("已在当前目录生成 CEDICT.dict.yaml")
