# Create a ping command
import platform
import subprocess

class PingPong:
    def __init__(self, host: str):
        self.host = host

    def ping(self, timeout: int = 1) -> bool:
        """
        Ping a host and return True if the host is reachable
        """
        # -c 1: Send only one packet
        # -W 1: Timeout after 1 second
        # -q: Quiet output
        # -n: Numeric output only
        command = f"ping -c 1 -W {timeout} -q -n {self.host}"
        # Run the command
        process = subprocess.run(command, shell=True, capture_output=True)
        # Check the return code
        if process.returncode == 0:
            return True
        else:
            return False
        

if __name__ == "__main__":
    host = "192.168.110.1"
    ping = PingPong(host)
    print(f"Pinging {host}...")
    if ping.ping(timeout=5):
        print(f"{host} is reachable")
    else:
        print(f"{host} is not reachable")