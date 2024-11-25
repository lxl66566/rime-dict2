from PyConsoleMenu2 import BaseMenu

from .cedict import NAME as cedict_NAME
from .cedict import main as cedict_main
from .galgame import NAME as galgame_NAME
from .galgame import main as galgame_main

ret = (
    BaseMenu("Select the dict you want to make")
    .add_options([cedict_NAME, galgame_NAME])
    .run()
)

match ret:
    case 0:
        cedict_main()
    case 1:
        galgame_main()
