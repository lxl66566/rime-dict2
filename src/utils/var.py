from datetime import datetime

OUTPUT = ["# made by lxl66566. https://github.com/lxl66566/rime-dict2", "#"]


def frontmatter(name: str):
    return f"""
---
name: {name}
version: "{datetime.now().strftime('%Y-%m-%d')}"
sort: by_weight
...

"""
