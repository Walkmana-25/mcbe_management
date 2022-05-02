import os
from mcbe_management import get_update
import urllib.request
import zipfile

def check_installed():#インストール済みか判別
    return os.path.isfile("/var/games/mcbe/lock/installed")

def server_download():#MCBE ServerをDLして解凍する
        
    os.makedirs("/tmp/mcbe_manegement")
    print("Downloading...")
    mc_url = get_update.get_update_url()
    urllib.request.urlretrieve(mc_url,"/tmp/mc_manegement/server.zip")#サーバーをDLしてzipを保存
    print("Extracting")
    with zipfile.ZipFile("/tmp/mc_manegement/server.zip", "r") as f:
        f.extractall("/tmp/mc_manegement/server")


