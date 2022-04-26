import fire
import server_power
def start(option="normal"):
    """Start Server(To force activation, use the --force)"""
    ans = server_power.start(option)
    return ans

if __name__ == '__main__':
    fire.Fire()