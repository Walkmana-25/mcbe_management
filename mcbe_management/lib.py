import os
#from mcbe_management import get_update
import get_update, exceptions
import urllib.request
import zipfile
import subprocess

def check_installed():#インストール済みか判別
    """サーバーがインストール済みか判別"""
    return os.path.isfile("/var/games/mcbe/lock/installed")

def server_download():#MCBE ServerをDLして解凍する
    """MCBE ServerをDLして解凍するよ"""
        
    os.makedirs("/tmp/mcbe_manegement", exist_ok=True)
    print("Downloading...")
    mc_url = get_update.get_update_url()
        #zipファイルの準備
    f = open("/tmp/mcbe_manegement/server.zip", "w")
    f.write("")
    f.close
    urllib.request.urlretrieve(mc_url,"/tmp/mcbe_manegement/server.zip")#サーバーをDLしてzipを保存
    print("Extracting")
    with zipfile.ZipFile("/tmp/mcbe_manegement/server.zip", "r") as f:
        f.extractall("/tmp/mcbe_manegement/server")


def check_server_started():
    """サーバーが起動しているか判別するよ"""
    return os.path.isfile("/var/games/mcbe/lock/started")

def excute_inside_server(input):
    """Minecraft Server内でコマンドを実行して、その実行結果を取得する"""
    #サーバーが起動しているか確認
    if check_server_started() == False:
        raise exceptions.Server_is_not_running
    
