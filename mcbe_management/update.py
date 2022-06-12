from mcbe_management import lib, exceptions, backup, get_update
import json
import os
import shutil

def server_update(manual=True, force=False):
    if manual == True:
        print("Update Minecraft Server")
    #Serverが起動しているか確認
    if lib.check_server_started() == True:
        raise exceptions.server_is_started()
    #Serverがインストールされているか確認
    if lib.check_installed() == False:
        raise exceptions.server_is_not_installed()
    #serverのversionを読み込む
    url = get_update.get_update_url()
    version = lib.url_to_version(url)
    #jsonから現在のversionを読み込む
    with open("/var/games/mcbe/script.json") as f:
        settings = json.load(f)
    #json.loadがstrを返したら、dicrionaryに変換する
    if type(settings) is str:
        setting = eval(setting)
    
    current_version = settings["mc_version"]

    #versionを比較する
    if  version != current_version or force == True:
        print("Starting Update")
        #先にバックアップをする
        print("backupping...")
        backup.backup()

        #worlds,server.properties,allowlist.json,permissions.jsonを一時フォルダーに移動する
        #/tmp/mcbe_manegement/dataを作る
        os.makedirs("/tmp/mcbe_manegement/data", exist_ok=True)
        #コピーを実行する
        print("copying server data")
        copy_list = [
            ["/var/games/mcbe/server/server.properties", "/tmp/mcbe_manegement/data/server.properties"],
            ["/var/games/mcbe/server/allowlist.json", "/tmp/mcbe_manegement/data/allowlist.json"],
            ["/var/games/mcbe/server/permissions.json", "/tmp/mcbe_manegement/data/permissions.json"]
        ]
        copy_folder = ["/var/games/mcbe/server/worlds/", "/tmp/mcbe_manegement/data/worlds"]
        for i in copy_list:
            shutil.copy2(i[0], i[1])

        shutil.copytree(copy_folder[0], copy_folder[1],dirs_exist_ok=True)

        #現在のサーバーを削除する
        shutil.rmtree("/var/games/mcbe/server")

        #updateを実行する
        lib.server_download(url)

        #serverのコピーを実行する
        print("Updating")
        shutil.copytree("/tmp/mcbe_manegement/server","/var/games/mcbe/server")

        #パーミッションを変更する
        os.chmod("/var/games/mcbe/server/bedrock_server", 755)

        #デフォルトのserver.properties,allowlist.json,permissions.jsonを削除する
        for i in copy_list:
            os.remove(i[0])

        #データをもとに戻す
        for i in copy_list:
            shutil.copy2(i[1], i[0])
        
        shutil.copytree(copy_folder[1], copy_folder[0])

        #Jsonに書き込む
        settings["mc_version"] = version
        with open("/var/games/mcbe/script.json", "w") as f:
            json.dump(settings, f, indent=4)   



        #不具合防止のoutput.txtを作る
        f = open("/var/games/mcbe/server/output.txt", "w")
        f.write("")
        f.close()
        
        return "Update Completed"

    else:
        return "Update is not needed."

print(server_update(force=True))