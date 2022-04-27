import sys
import fire
import server_power


import exceptions
class server_io(object):

    def start(option="normal"):
        """Start Server(To force activation, use the --force)"""
        try:
            ans = server_power.start(option)
        except exceptions.Required_file_does_not_exist:
            print("Error:Required File does not exist.", file=sys.stderr)
        except exceptions.screen_already_exists:
            print("Error: Server has already started.", file=sys.stderr)

        return ans



    def stop():
        """Stop Server"""
        out = server_power.stop()
        return out

def main():
    fire.Fire(server_io)


if __name__ == '__main__':
    main()