import unicodedata
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
from rustiter import rter

from ..utils.var import frontmatter

NAME = "arknights"
output = [frontmatter(NAME)]


def p(text: str):
    pinyin = (
        rter(lazy_pinyin(text))
        .map(lambda x: unicodedata.normalize("NFKD", x))
        .filter(None)
    )
    return pinyin


def main():
    url = "https://prts.wiki/w/%E6%B3%B0%E6%8B%89%E8%AF%8D%E5%BA%93"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # 使用CSS选择器选取所有tr下的第一个td
        first_tds = soup.select("tr > td:first-of-type")

        for td in first_tds:
            nounce = td.get_text(strip=True)
            if "/" in nounce:
                nounce = nounce.split("/")
            else:
                nounce = [nounce]
            for n in rter(nounce).take_while(lambda x: x != "("):
                pinyin = " ".join(
                    p(n)
                    .filter(lambda x: x not in ["·", "-"])
                    .map(lambda x: x.replace("·", ""))
                    .collect()
                )
                output.append(f"{n}\t{pinyin}")

        output_text = "\n".join(output)
        Path(f"{NAME}.dict.yaml").write_text(output_text, encoding="utf-8")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
