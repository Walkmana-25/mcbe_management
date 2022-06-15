class mcbe_exception(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class Required_file_does_not_exist(mcbe_exception):
    """必要なファイルが存在していないときに発生させる例外クラス"""
    pass

class screen_already_exists(mcbe_exception):
    """screenがすでに存在しているときに発生させる例外クラス"""
    pass

class server_timeout(mcbe_exception):
    """サーバーが規定時間以内に起動しないときに発生する例外クラス"""
    pass
class Required_package_does_not_installed(mcbe_exception):
    """必要なパッケージがインストールされていないときに発生する例外クラス"""
    pass
class Server_already_installed(mcbe_exception):
    """サーバーを二回インストールしようとしたときに発生する例外クラス"""
    pass
class Server_is_not_running(mcbe_exception):
    """サーバーが起動していないときに発生する例外クラス"""

class  variable_class_mcbe_exception(mcbe_exception):
    """違う変数のクラスのときに発生する例外クラス"""

class config_is_wrong(mcbe_exception):
    """configのフォーマットが間違っているときに発生する例外クラス"""

class server_is_started(mcbe_exception):
    """サーバーが停止していることが必要な処理で、サーバーが停止していなかったときに発生する例外クラス"""

class get_update_url_failed(mcbe_exception):
    """URLを取得に失敗したときに発生する例外クラス"""
class server_is_not_installed(mcbe_exception):
    """Serverがインストールされていないときに発生する例外クラス"""