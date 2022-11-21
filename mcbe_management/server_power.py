import subprocess
import os
import time
from mcbe_management import exceptions, lib, log, update
from logging import getLogger
from glob import glob
#TODO screen がすでに存在していた時の処理
#TODO2 標準エラー出力についての設定
#minecraft serverが正常に起動したか確かめる(output.txtからserver startedが出力されて、3秒いないにcrashが表示されないかどうか)
logger = getLogger("mcbe").getChild("server_power")

def start(option=None, auto=False):
    logger.info("Starting Minecraft Bedrock Server")
    #最低限必要なファイルが存在しているか確認
    #bedrock_server,server.properties,worldsフォルダ
    bedrock = os.path.isfile("/var/games/mcbe/server/bedrock_server")
    properties_file = os.path.isfile("/var/games/mcbe/server/server.properties")
    logger.debug(f"bedrock server exists:{bedrock}, properties_file exsits:{properties_file}")
    if not option == "force":
        if bedrock == False or properties_file == False:
            if bedrock == False:
                exception = "bedrock_server"
            #elif properties_file == False:
            #    exception = f"{exception},server.properties"
            raise exceptions.Required_file_does_not_exist(exception)#存在しなかったらエラー
    
    #サーバーがすでに起動しているか確かめる
    
    if os.path.isfile("/var/games/mcbe/lock/started") == True:
        screen_list = []
        screen_list += glob("/tmp/screen/S-root/*.mcbe_server")
        screen_list += glob("/run/screen/S-root/*.mcbe_server")
        screen_list += glob("/root/.screen/*.mcbe_server")
        if(screen_list != []):
            raise exceptions.screen_already_exists()


    #screen の準備
    server_dir = "/var/games/mcbe/server/"
    args = ["screen", "-dmS", "mcbe_server"]
    logger.debug(f"ran {args}")
    subprocess.check_output(args, cwd=server_dir)#サーバー実行用のscreenを立ち上げる
    
    #screen上でサーバーを起動させる
    
    args = (r"screen -S mcbe_server -X stuff 'LD_LIBRARY_PATH=. ./bedrock_server > output.txt \n'")
    logger.debug(f"ran {args}")
    result = subprocess.run(args, cwd=server_dir, shell=True)

    logger.info("server start signal sent.")
    


    #bedrock serverのコンソール上でServer startedが表示されているか確認
    f = open("/var/games/mcbe/server/output.txt", "r")
    for i in range(11):
        console = f.read()
        console_out = "start" in console
        logger.debug(f"Start in mcbe console:{console_out}")
        logger.debug(f"Cycle count:{i}")
        if console_out == True:
            break
        elif i == 10:
            f.close
            raise exceptions.server_timeout()
        time.sleep(1)

    f.close
    #server startしていることを示すlockファイルを生成する
    f = open("/var/games/mcbe/lock/started", "w")
    f.write("")
    f.close()
    logger.debug("Created lock file")



    logger.info("Server Started.")
    return "Server Started!"

def stop(stop_demon=True):
    logger.info("Stopping Minecraft Server")
    logger.debug(f"Stop Demon:{stop_demon}")
    #サーバーが起動しているか確かめる
    logger.debug(f"Server Started:{lib.check_server_started()}")
    if lib.check_server_started() == False:
        raise exceptions.Server_is_not_running
    if stop_demon == True:   
        #demonに終了信号を送る
        with open("/var/games/mcbe/lock/demon_stop","w") as f:
            f.write("")
        logger.info("daemon stop signal sent.")

    #サーバー停止信号を送る
    args = (r"screen -S mcbe_server -X stuff 'stop \n'")
    result = subprocess.run(args, shell=True)

    #bedrock serverのコンソール上でQuit correctlyが表示されているか確認
    f = open("/var/games/mcbe/server/output.txt", "r")
    for i in range(30):
        console = f.read()
        console_out = "Quit correctly" in console
        logger.debug(f"Quit Correctly in console:{console_out}")
        if console_out == True:
            break
        print(f"Waiting:{i}/30s")
        if(i == 29):
            print("Timeout. Stop force.")
        time.sleep(1)
    f.close
    

    #screenのセッションを終了する
    args = (r"screen -S mcbe_server -X stuff 'exit \n'")
    result = subprocess.run(args, shell=True)
    logger.debug("Screen Deleted")

    #MCBE ServerのScreenが残っていたら全部消す
    
    screen_list = []
    screen_list += glob("/tmp/screen/S-root/*.mcbe_server")
    screen_list += glob("/run/screen/S-root/*.mcbe_server")
    screen_list += glob("/root/.screen/*.mcbe_server")
    for i in screen_list:
        os.remove(i)

    #lockファイルの削除
    os.remove("/var/games/mcbe/lock/started")
    logger.debug("/var/games/mcbe/lock/started deleted.")
    if stop_demon == True:
        #demonが終了しているか確認する
        while True:
            started = os.path.exists("/var/games/mcbe/lock/demon_started")
            logger.debug(f"daemon started:{started}")
            if started == False:
                break
            print("Waiting for stopping demon....")
            time.sleep(1)
        os.remove("/var/games/mcbe/lock/demon_stop")
        logger.info("daemon Stopped.")
     
    logger.info("Server Stopped")
    return "Server Stopped"

if __name__ == "__main__":
    start()
    stop()

def auto_fix(num):
    #0回の時はサーバーを再起動する
    if num == 0:
        #サーバーを停止させる
        stop(stop_demon=False)
        #サーバーを起動させる
        start()

    #1回のときはサーバーを再インストールする
    if num == 1:
        #サーバーを停止させる
        stop(stop_demon=False)
        #サーバーを強制アップデートする
        update.server_update(manual=False, force=True)
        #サーバーを起動させる
        start()

    #2回以上の時はサーバーを停止させる
    if num >= 2:
        #サーバを停止させる
        stop(stop_demon=False)
        #エラーを発生させる
        logger.error("Failed to fix")
        raise exceptions.server_crash()