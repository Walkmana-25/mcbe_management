import subprocess
import os 
from mcbe_management import lib
import sys
import shutil



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


    #bedrock serverのインストール
    #/tmp/mcbe_manegementにzipをdlして、そのあと展開して中身を/var/games/mcbe/serverにコピーする
    lib.server_download()#DLしたサーバーを/tmp/mcbe_manegement/serverに展開
    print("Installing")
    shutil.copytree("/tmp/mcbe_manegement/server","/var/games/mcbe/server")
    print("Install Completed!")

    #インストールした印を作る
    f = open("/var/games/mcbe/lock/installed", "w")
    f.write("")
    f.close

    #不具合防止のoutput.txtを作る
    f = open("/var/games/mcbe/server/output.txt", "w")
    f.write("")
    f.close()


    print("Please edit /var/games/mcbe/server/server.properties")
    print("After, You can start server with mcbe start")






