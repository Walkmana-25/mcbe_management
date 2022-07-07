from mcbe_management import lib, exceptions, backup, get_update, log
import json
import os
import shutil
from logging import getLogger
logger = getLogger("mcbe").getChild("update")

def server_update(manual=True, force=False):
    logger.info("Starting Update")
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
    setting = ""
    with open("/var/games/mcbe/script.json") as f:
        setting = json.load(f)
    #json.loadがstrを返したら、dicrionaryに変換する
    if type(setting) is str:
        setting = eval(setting)
    logger.debug(f"setting:{setting}")    

    current_version = setting["mc_version"]
    logger.info(f"Current MC Version:{current_version}") 
    logger.info(f"Remote version:{version}")

    #versionを比較する
    if  version != current_version or force == True:
        logger.info(f"Update Server to {version}")
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
        logger.debug(f"copy list:{copy_list}")
        logger.debug(f"copy_colder:{copy_folder}")
        for i in copy_list:
            shutil.copy2(i[0], i[1])

        shutil.copytree(copy_folder[0], copy_folder[1],dirs_exist_ok=True)

        #現在のサーバーを削除する
        shutil.rmtree("/var/games/mcbe/server")
        logger.debug("Delete Server")

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
        setting["mc_version"] = version
        with open("/var/games/mcbe/script.json", "w") as f:
            json.dump(setting, f, indent=4)   



        #不具合防止のoutput.txtを作る
        f = open("/var/games/mcbe/server/output.txt", "w")
        f.write("")
        f.close()
        logger.info("Update Completed")
        
        return "Update Completed"

    else:
        logger.info("Server do not need update")
        return "Update is not needed."

if __name__ == "__main__":
    server_update(force=True)