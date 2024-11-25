import logging as log
import re
import unicodedata
from copy import copy
from pathlib import Path

import pandas as pd
from pypinyin import lazy_pinyin
from rustiter import rter

from ..utils import contains_chinese
from ..utils.var import OUTPUT, frontmatter

NAME = "Galgame"


def remove_elements_after_non_letter(lst):
    # 遍历列表中的每个元素
    for i, item in enumerate(lst):
        # 检查元素是否包含非字母字符
        if re.search(r"[^a-zA-Z]", item):
            # 如果找到非字母字符，返回该元素之前的所有元素
            return lst[:i]
    # 如果没有找到非字母字符，返回原始列表
    return lst


# 每个 galgame 同时放中文译名和原名，原名排在译名后面。
class Game:
    def __init__(self, name: str, translation: str, rating_count: str):
        self.name = name
        self.translation = translation
        self.rating_count = max(int(rating_count), 1)
        self.pinyin = " ".join(
            remove_elements_after_non_letter(
                rter(lazy_pinyin(translation))
                .map(lambda x: unicodedata.normalize("NFKD", x))
                .filter(None)
                .collect()
            )
        )
        if self.pinyin.strip() == "":
            raise ValueError(f"无法提取出拼音：{translation}")

    def __str__(self):
        return f"{self.translation}\t{self.pinyin}\t{self.rating_count}\n{self.name}\t{self.pinyin}\t{self.rating_count - 1}"


def main():
    # 读取CSV文件
    # data from: https://zhuanlan.zhihu.com/p/186288692
    df = pd.read_csv(Path(__file__).parent / "src.csv", encoding="utf-8")

    # 提取需要的字段
    extracted_data = df[["游戏名称", "游戏译名", "评分人数"]]

    def preprocess(text: str):
        return text.replace("\t", " ")

    games: list[Game] = []

    # 使用iterrows()方法遍历DataFrame的每一行
    for index, row in extracted_data.iterrows():
        game_name = preprocess(row["游戏名称"])
        game_translation = preprocess(row["游戏译名"])
        rating_count = row["评分人数"]

        # 第一位不是中文就不要了，对输入法没有帮助
        if "暂无译名" in game_translation or not contains_chinese(game_translation[0]):
            continue
        try:
            games.append(Game(game_name, game_translation, rating_count))
        except ValueError as e:
            log.error(e)
            continue

    log.info(f"已处理 {len(games)} 个游戏，条目数：{len(games)*2}。")

    output = copy(OUTPUT)
    output.append(frontmatter(NAME))
    output.extend(map(str, games))
    output_text = "\n".join(output)
    Path(f"{NAME}.dict.yaml").write_text(output_text, encoding="utf-8")


if __name__ == "__main__":
    main()
