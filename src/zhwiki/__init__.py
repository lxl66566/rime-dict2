import re
import tempfile
from pathlib import Path

from ..utils import download_to

NAME = "zhwiki-"

START = {
    # 姓
    "赵",
    "钱",
    "孙",
    "李",
    "周",
    "吴",
    "郑",
    "王",
    "冯",
    "陈",
    "褚",
    "卫",
    "蒋",
    "沈",
    "韩",
    "杨",
    "朱",
    "秦",
    "尤",
    "许",
    "何",
    "吕",
    "施",
    "张",
    "孔",
    "曹",
    "严",
    "华",
    "金",
    "魏",
    "陶",
    "姜",
    "戚",
    "谢",
    "邹",
    "喻",
    "柏",
    "水",
    "窦",
    "章",
    "云",
    "苏",
    "潘",
    "葛",
    "奚",
    "范",
    "彭",
    "郎",
    "鲁",
    "韦",
    "昌",
    "马",
    "苗",
    "凤",
    "花",
    "方",
    "俞",
    "任",
    "袁",
    "柳",
    "酆",
    "鲍",
    "史",
    "唐",
    "费",
    "廉",
    "岑",
    "薛",
    "雷",
    "贺",
    "倪",
    "汤",
    "滕",
    "殷",
    "罗",
    "毕",
    "郝",
    "邬",
    "安",
    "常",
    "乐",
    "于",
    "时",
    "傅",
    "皮",
    "卞",
    "齐",
    "康",
    "伍",
    "余",
    "卜",
    "顾",
    "孟",
    "平",
    "黄",
    "穆",
    "萧",
    "尹",
    "高",
    "程",
    "盛",
    "崔",
    "蔡",
    "贾",
    "胡",
    "洪",
    "董",
    "丁",
    "池",
}

start_max_len = max(len(x) for x in START)

END = {
    # 地区
    "市",
    "县",
    "区",
    "村",
    "山",
    "路",
    "桥",
    "站",
    "路",
    "道",
    "镇",
    "乡",
    "公司",
    "厅",
    "局",
    "集团",
    "俱乐部",
    "开发区",
    "所",
    "处",
    "场",
    "中学",
    "高中",
    "校",
    "院",
    "小学",
    "公园",
    "湾",
    "河",
    "湖",
    "氏",
    "店",
    # 生物
    "界",
    "门",
    "纲",
    "目",
    "科",
    "属",
    "种",
    "蛇",
    "鼠",
    "虫",
    "树",
    "鸟",
    "鱼",
    "雀",
    "人",
}
end_max_len = max(len(x) for x in END)


def match_end(word: str):
    for x in set([word[-i:] for i in range(1, end_max_len + 1)]):
        if x in END:
            return True
    return False


def match_start(word: str):
    for x in set([word[:i] for i in range(1, start_max_len + 1)]):
        if x in START:
            return True
    return False


def take_line(line: str):
    """
    returns whether to take this line
    """
    if len(line) == 0:
        return True
    if line.startswith("#"):
        return True

    x = line.split("\t")
    if match_start(x[0]) or match_end(x[0]):
        return False

    return True


def main():
    tempdir = Path(tempfile.gettempdir())
    download_to(
        "https://github.com/felixonmars/fcitx5-pinyin-zhwiki/releases/download/0.2.5/zhwiki-20241218.dict.yaml",
        tempdir / "zhwiki.dict.yaml",
    )
    s = (tempdir / "zhwiki.dict.yaml").read_text(encoding="utf-8").splitlines()
    s = list(filter(lambda x: take_line(x), s))
    s.append("")  # 末尾空行
    (tempdir / "zhwiki-.dict.yaml").write_text("\n".join(s), encoding="utf-8")
