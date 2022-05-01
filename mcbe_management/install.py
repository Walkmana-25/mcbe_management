import os 
from mcbe_management import lib


def install():
    #サーバーがインストール済みか判別
    if lib.check_installed() == True:
        print("MCBE Server Installed")
        exit()

    #Google Chromeがインストール済みか判別
           

    
    #/var/games/mcbe/を作成
    os.makedirs("/var/games/mcbe/")
