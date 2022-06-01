import subprocess
import os 
#from mcbe_management import lib, exceptions
from mcbe_management import lib, exceptions#for dev
import sys
import shutil
import pkgutil
import json





def install():
    #サーバーがインストール済みか判別
    if lib.check_installed() == True:
        raise exceptions.Server_already_installed
        

    #Google Chromeがインストール済みか判別
    try:
        subprocess.check_output(["google-chrome", "--version"])
    except subprocess.CalledProcessError:
        raise exceptions.Required_package_does_not_installed

        
    #screenがインストール済みか判別
    try:
        subprocess.check_output(["screen", "--version"])
    except subprocess.CalledProcessError:
        raise exceptions.Required_package_does_not_installed

    
    #/var/games/mcbe/を作成
    os.makedirs("/var/games/mcbe/lock", exist_ok=True)

    #configとdemonをコピーする
    with open("/etc/mcbe_management.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/mcbe_management.json").decode("utf-8"))
    with open("/var/games/mcbe/script.json", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/script.json").decode("utf-8"))
    with open("/var/games/mcbe/demon.py", "x") as f:
        f.write(pkgutil.get_data("mcbe_management", "templete/demon.py").decode("utf-8"))

    #jsonファイルを読み込む
    with open("/var/games/mcbe/script.json", "r") as f:
        settings = json.loads(f)

    #bedrock serverのインストール
    #/tmp/mcbe_manegementにzipをdlして、そのあと展開して中身を/var/games/mcbe/serverにコピーする
    url = lib.server_download()#DLしたサーバーを/tmp/mcbe_manegement/serverに展開
    if url == None:
        print("Coldn't get minecraft server download link.", file=sys.stderr)
        os._exit(1)
    print("Installing")
    shutil.copytree("/tmp/mcbe_manegement/server","/var/games/mcbe/server")
    #パーミッションの変更

    os.chmod("/var/games/mcbe/server/bedrock_server", 755)

    print("Install Completed!")

    #インストールした印を作る
    f = open("/var/games/mcbe/lock/installed", "w")
    f.write("")
    f.close

    #不具合防止のoutput.txtを作る
    f = open("/var/games/mcbe/server/output.txt", "w")
    f.write("")
    f.close()

    #jsonファイルにVersion情報を書き込む
    settings["mc_version"] = lib.url_to_version(url)
    write_json = json.dumps(settings)
    with open("/var/games/mcbe/script.py", "w") as f:
        json.dump(write_json, f, indent=4)


    print("Please edit /var/games/mcbe/server/server.properties")
    print("After, You can start server with mcbe start")









