from PyConsoleMenu2 import BaseMenu

from .cedict import main as cedict_main

ret = BaseMenu("Select the dict you want to make").add_options(["CEDICT"]).run()

match ret:
    case 0:
        cedict_main()
