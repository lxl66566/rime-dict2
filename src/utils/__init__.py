import logging as log
import re
import tempfile
import unicodedata
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm


def download_to(url: str, to: Path):
    """
    下载并缓存，如果读取到则跳过下载
    """
    if to.exists():
        log.info(f"文件已存在：{to}，跳过下载。")
        return to

    # 下载文件
    log.info("开始下载 CEDICT 文件...")
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        with (
            open(to, "wb") as file,
            tqdm(
                desc="下载进度",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar,
        ):
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                bar.update(len(chunk))
    log.info(f"文件下载完成，保存到 {to}。")
    return to


def extract(zip_path: Path):
    assert zip_path.exists(), "文件不存在：{}".format(zip_path)

    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    log.info(f"创建临时目录：{temp_dir}")
    # 解压文件
    log.info("开始解压文件...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)
    files = list(Path(temp_dir).glob("*"))
    if len(files) == 1 and files[0].is_dir():
        to = files[0]
    else:
        to = Path(temp_dir)
    log.info(f"文件解压完成，解压后主路径：{to}")

    return to


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


def keep_ascii(s):
    """
    去除字符串中的非 ASCII 字符
    """
    return "".join(c for c in unicodedata.normalize("NFKD", s) if ord(c) < 128)
