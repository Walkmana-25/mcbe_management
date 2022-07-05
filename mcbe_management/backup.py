import subprocess
from mcbe_management import lib, exceptions, server_power, log
import datetime
import time
import time
import os
import shutil
import sys
from logging import getLogger


def backup():
    logger = getLogger("mcbe").getChild("backup")
    logger.info("Starting Backup")
    
    #worldsフォルダーが存在しているか確認する
    if os.path.exists("/var/games/mcbe/server/worlds") == False:
        raise exceptions.Required_file_does_not_exist("/var/games/mcbe/server/worlds")
    #サーバーが起動しているか判別する
    #サーバーが起動している時の処理
    if os.path.isfile("/var/games/mcbe/lock/started") == True:
        logger.debug("Server is running")
        save_hold = lib.excute_inside_server("save hold")#bedrock serverで、worldsフォルダーをlockする
        logger.debug(f"save hold:{save_hold}")
        #server側から、保存が終わったことを通知されるまで待つ(timeoutは5回)
        for i in range(6):
            logger.debug(f"loop:{i}")
            if i == 5:
                raise exceptions.server_timeout
            save_result = lib.excute_inside_server("save query")
            logger.debug(f"save query:{save_result}")
            if "saved" in save_result:
                break
            time.sleep(1)
    else:
        logger.debug("Server is not running.")

def restore():
    logger = getLogger("mcbe").getChild("backup")



if __name__ == "__main__":
    command = input("Enter Function")
    if command == "backup":
        backup()
    elif command == "restore":
        restore()
    else:
        print("error")
        sys.exit(1)