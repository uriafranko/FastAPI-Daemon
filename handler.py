import sys
import uvicorn
from Daemon import Daemon


def is_ip_valid(ip_string: str, port: int) -> bool:
    """Receive ip address and port and return if valid.
    Args:
        ip_string (str): ip address to check.
        port (int): port to check.
    Returns:
        bool: is the string a valid ip address.
    """
    if not isinstance(port, int):
        print('Invalid port type. Must be an integer.')
        return False
    if not isinstance(ip_string, str):
        print('Invalid ip type. Must be an string.')
        return False
    ip_parts = ip_string.split(".")
    if len(ip_parts) < 4 or len(ip_parts) > 4:
        print("IP address should be structured from 4 parts.")
        return False
    if not(bool(ip_parts) and all(map(lambda n: 0 <= int(n) <= 255, ip_parts))):
        print("invalid IP address")
        return False
    return True


class FastAPI_Daemon(Daemon):
    """Daemon Wrapper for FastAPI

    Args:
        app_command (str): The command to run the FastAPI server
        host (str): The host to bind the server to
        port (int): The port to bind the server to
        pidfile (str): The path to create the pidfile
    """

    def __init__(self, app_command: str = 'app:app',
                 port: int = 8080, host: str = '0.0.0.0',
                 pidfile: str = '/var/run/fastapi_daemon.pid',
                 stdin: str = '/dev/null', stdout: str = '/dev/null',
                 stderr: str = '/dev/null', overwrite_output: bool = False):

        super().__init__(pidfile, stdin, stdout, stderr, overwrite_output)
        self.app_command = app_command
        self.host = host
        self.port = port

    def run(self):
        uvicorn.run(self.app_command,
                    host=self.host, port=self.port, reload=True)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    if not is_ip_valid(host, port):  # checks if the host + port is a valid ip address
        exit()
    fastAPI_app = "app:app"  # Command to start fastAPI server, default is main:app
    daemon = FastAPI_Daemon(app_command=fastAPI_app, host=host, port=port,
                            pidfile='/var/run/fastapi_daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting fastAPI daemon...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print("Attempting to stop the daemon...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print("Attempting to restart the daemon...")
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
