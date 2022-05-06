import lib, exceptions
import time



def backup():
    #サーバーが起動しているか判別する
    server_started = lib.check_server_started

    #サーバーが起動している時の処理
    if server_started == True:
        lib.excute_inside_server("save hold")#bedrock serverで、worldsフォルダーをlockする
        #server側から、保存が終わったことを通知されるまで待つ(timeoutは5回)
        for i in range(6):
            if i == 5:
                raise exceptions.server_timeout
            save_result = lib.excute_inside_server("save resume")
            if "saved" in save_result:
                break
            time.sleep(1)