import questionary

from .cedict import NAME as cedict_NAME
from .cedict import main as cedict_main
from .galgame import NAME as galgame_NAME
from .galgame import main as galgame_main
from .zhwiki import NAME as zhwiki_NAME
from .zhwiki import main as zhwiki_main

ret = questionary.select(
    "Select the dict you want to make",
    choices=[cedict_NAME, galgame_NAME, zhwiki_NAME],
).ask()

if ret == cedict_NAME:
    cedict_main()
elif ret == galgame_NAME:
    galgame_main()
elif ret == zhwiki_NAME:
    zhwiki_main()
