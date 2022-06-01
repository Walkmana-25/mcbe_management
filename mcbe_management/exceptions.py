class Required_file_does_not_exist(Exception):
    """必要なファイルが存在していないときに発生させる例外クラス"""
    pass

class screen_already_exists(Exception):
    """screenがすでに存在しているときに発生させる例外クラス"""
    pass

class server_timeout(Exception):
    """サーバーが規定時間以内に起動しないときに発生する例外クラス"""
    pass
class Required_package_does_not_installed(Exception):
    """必要なパッケージがインストールされていないときに発生する例外クラス"""
    pass
class Server_already_installed(Exception):
    """サーバーを二回インストールしようとしたときに発生する例外クラス"""
    pass
class Server_is_not_running(Exception):
    """サーバーが起動していないときに発生する例外クラス"""

class  variable_class_exception(Exception):
    """違う変数のクラスのときに発生する例外クラス"""

class config_is_wrong(Exception):
    """configのフォーマットが間違っているときに発生する例外クラス"""

class server_is_started(Exception):
    """サーバーが停止していることが必要な処理で、サーバーが停止していなかったときに発生する例外クラス"""