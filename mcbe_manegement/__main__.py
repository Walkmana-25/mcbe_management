import fire
import server_power
<<<<<<< HEAD
import exceptions
def start(option="normal"):
    """Start Server(To force activation, use the --force)"""
    try:
        ans = server_power.start(option)
    except exceptions.Required_file_does_not_exist as ans:
        pass 
    
=======
def start(option="normal"):
    """Start Server(To force activation, use the --force)"""
    ans = server_power.start(option)
>>>>>>> 1254f7d6785c29eb062884bc70da3196b045d218
    return ans

if __name__ == '__main__':
    fire.Fire()