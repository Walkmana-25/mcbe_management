import os
from mcbe_management import get_update
import urllib.request
import zipfile
import subprocess

def check_installed():#インストール済みか判別
    """サーバーがインストール済みか判別"""
    return os.path.isfile("/var/games/mcbe/lock/installed")

def server_download():#MCBE ServerをDLして解凍する
    """MCBE ServerをDLして解凍するよ"""
        
    os.makedirs("/tmp/mcbe_manegement")
    print("Downloading...")
    mc_url = get_update.get_update_url()
    urllib.request.urlretrieve(mc_url,"/tmp/mc_manegement/server.zip")#サーバーをDLしてzipを保存
    print("Extracting")
    with zipfile.ZipFile("/tmp/mc_manegement/server.zip", "r") as f:
        f.extractall("/tmp/mc_manegement/server")


def check_server_started():
    """サーバーが起動しているか判別するよ"""
    screen_test = subprocess.run(["screen","-ls"], encoding="utf-8", stdout=subprocess.PIPE)
    screen_exist = "mcbe" in screen_test.stdout
    if screen_exist == True:
        return True
    else:
        return False
            