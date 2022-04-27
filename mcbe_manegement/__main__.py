import sys
import fire
import server_power


import exceptions
def start(option="normal"):
    """Start Server(To force activation, use the --force)"""
    try:
        ans = server_power.start(option)
    except exceptions.Required_file_does_not_exist:
        print("Error:Required File does not exist.", file=sys.stderr)
    return 
    


if __name__ == '__main__':
    fire.Fire()