import subprocess
import os 
from mcbe_management import lib, get_update
import sys


def install():
    #サーバーがインストール済みか判別
    if lib.check_installed() == True:
        return "MCBE Server Installed"
        

    #Google Chromeがインストール済みか判別
    try:
        subprocess.check_output(["google-chrome", "--version"])
    except subprocess.CalledProcessError:
        print("Google Chrome is not installed. Please install Google Chrome", file=sys.stderr)
        exit()
        
    #screenがインストール済みか判別
    try:
        subprocess.check_output(["screen", "--version"])
    except subprocess.CalledProcessError:
        print("screen is not installed. Please install Screen", file=sys.stderr)
        exit()

    
    #/var/games/mcbe/を作成
    os.makedirs("/var/games/mcbe/")
