from logging import getLogger, StreamHandler, FileHandler, Formatter, ERROR, INFO, DEBUG
from datetime import datetime
import os
import json
import re
#configを読み込んで、debug modeか判別する
debug_mode = False
if os.path.exists("/etc/mcbe_management.json") == True:
    with open("/etc/mcbe_management.json", "r") as load_config_json:
        text = load_config_json.read()
        re_text = re.sub(r'/\*[\s\S]*?\*/|//.*', '', text)
        config = json.loads(re_text)
        debug_mode = config["debug_mode"]

#log用のディレクトリの生成
os.makedirs("/var/log/mcbe_management", exist_ok=True)
#loggerの生成
logger = getLogger("mcbe")
logger.setLevel(DEBUG)

#Logのフォーマットの設定
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#StreamHandlerの設定
stream_handler = StreamHandler()
#StreamHandlerはError以上を出力する
if debug_mode == True:
    stream_handler.setLevel(DEBUG)
else:
    stream_handler.setLevel(ERROR)
#Formatを登録する
stream_handler.setFormatter(handler_format)

#FileHandlerの設定
file_handler = FileHandler('/var/log/mcbe_management/{:%Y-%m-%d}.log'.format(datetime.now()))
#Info以上を出力する
file_handler.setLevel(INFO)
#Formatを登録する
file_handler.setFormatter(handler_format)

#handlerをセット
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

#loggerのテスト
if __name__ == "__main__":
    logger.critical("critical test")
    logger.error("error_test")
    logger.info("info_test")
    logger.debug("debug_error")
