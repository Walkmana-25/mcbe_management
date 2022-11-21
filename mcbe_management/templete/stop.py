from http import server
from mcbe_management import server_power
from systemd import daemon

if __name__ == '__main__':
    daemon.notify("STATUS=Server Stopping")
    daemon.notify("STOPPING=1")
    server_power.stop()
