# rime-dict2

我自己整理的简体中文 rime dict，作为其他词库的补充。**你可以在 [Release](https://github.com/lxl66566/rime-dict2/releases) 中直接下载制作完毕的 dict**。当前内容：

<!-- prettier-ignore -->
| 字典名与来源 | 条目数 | 是否包含词频 | 备注 |
| :---: | :---: | :---: | :---: |
| [CEDICT](https://www.mdbg.net/chinese/dictionary?page=cc-cedict) | 118631 | ✖ |
| [Galgame](https://zhuanlan.zhihu.com/p/186288692) | 1844 | ✔ | 每个 galgame 同时放中文译名和原名，原名排在译名后 |
| [zhwiki-](https://github.com/felixonmars/fcitx5-pinyin-zhwiki) | 891551 | ✖ | zhwiki 原数据集的精简版，去除了一些人名地名，仍然很大；去除算法可能会误删到其他常用词语，因此需要配合其他词典使用 |

## 运行程序

使用 [uv](https://github.com/astral-sh/uv) 作为 python 包管理器。安装 uv 后，clone 本仓库，运行 `uv run python -m src` 即可。程序会自动下载源词典文件，处理并输出。

生成词典后，还需要进行格式化，重新对其排序。这里使用 vscode 插件 [Rime formatter](https://github.com/lxl66566/rime-formatter) 进行格式化。
