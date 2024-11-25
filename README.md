# rime-dict2

我自己整理的简体中文 rime dict，作为其他词库的补充。你可以在 [Release](https://github.com/lxl66566/rime-dict2/releases) 中直接下载制作完毕的 dict。当前内容：

<!-- prettier-ignore -->
| 字典名 | 条目数 | 是否包含词频 | 备注 |
| :---: | :---: | :---: | :---: |
| [CEDICT](https://www.mdbg.net/chinese/dictionary?page=cc-cedict) | 121543 | x |

## 运行程序

使用 [uv](https://github.com/astral-sh/uv) 作为 python 包管理器。安装 uv 后，clone 本仓库，运行 `uv run python -m src` 即可。程序会自动下载源词典文件，处理并输出。
