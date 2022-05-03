import subprocess
import sys
import fire
import exceptions, server_power, install


class server_io(object):

    def start(option="normal"):
        ans = ""
        """Start Server(To force activation, use the start_force)"""
        try:
            ans = server_power.start(option)
        except exceptions.Required_file_does_not_exist:
            print("Error:Required File does not exist.", file=sys.stderr)
        except exceptions.screen_already_exists:
            print("Error: Server has already started.", file=sys.stderr)
        except exceptions.server_timeout:
            print("Server could not start.", file=sys.stderr)

        return ans

    def start_force(option="force"):
        ans = ""
        """Start Server(Force)"""
        try:
            ans = server_power.start("force")
        except exceptions.Required_file_does_not_exist:
            print("Error:Required File does not exist.", file=sys.stderr)
        except exceptions.screen_already_exists:
            print("Error: Server has already started.", file=sys.stderr)

        return ans


    def stop(self):
        """Stop Server"""
        out = server_power.stop()
        return out

    def install(self):
        """Install Server"""
        try:
            out = install.install()
        except exceptions.Server_already_installed:
            print("Server has already installed.")
        except exceptions.Required_package_does_not_installed:
            print("Google Chrome or Screen is not installed. Please install them.", file=sys.stderr)
def main():
    fire.Fire(server_io)


if __name__ == '__main__':
    main()