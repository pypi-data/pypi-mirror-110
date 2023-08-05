from essentials.network_ops import Get_GW, Get_IP, IP_to_MAC, Get_IP_with_MAC, Get_All_IP_Stat
from essentials import GetPublicIP
import platform    # For getting the operating system name
import subprocess  # For executing a shell command


Get_Device_IPS = Get_IP
Get_All_Net_Ifaces = Get_All_IP_Stat
Device_IP_to_MAC = IP_to_MAC
Get_Gateway = Get_GW


def shell_command(command):
    return subprocess.check_output(command)


class __ping_stats__(object):
    def __init__(self):
        self.sent = None
        self.received = None
        self.lost = None

    def parse_str_win(self, data_str):
        sent, recv, lost = data_str.split(", ")

        self.sent = sent.split("= ")[1]
        self.received = recv.split("= ")[1]
        self.lost = lost.split("= ")[1][0]

    def __str__(self):
        return f"< PING STATS (sent: {self.sent}, received: {self.received}, lost: {self.lost}) >"

    def __p_print__(self):
        return f"PING STATS \r\n\t\tsent: {self.sent},\r\n\t\treceived: {self.received},\r\n\t\tlost: {self.lost}"

class __ping_trip_time__(object):
    def __init__(self):
        self.minimum = None
        self.maxium = None
        self.average = None

    def parse_str_win(self, data_str):
        min, max, avg = data_str.split(", ")

        self.minimum = min.split("= ")[1]
        self.maxium = max.split("= ")[1]
        self.average = avg.split("= ")[1]

    def __str__(self):
        return f"< PING TRIP TIME (minimum: {self.minimum}, maxium: {self.maxium}, average: {self.average}) >"

    def __p_print__(self):
        return f"PING TRIP TIME \r\n\t\tminimum: {self.minimum}, \r\n\t\tmaxium: {self.maxium}, \r\n\t\taverage: {self.average}"

class __ping__(object):
    def __init__(self, success, host, pings):
        self.success = success
        self.host = host
        self.pings = pings
        self.statistics = __ping_stats__()
        self.trip_time = __ping_trip_time__()

    def __str__(self) -> str:
        return f"PING (host: {self.host}, pings: {self.pings}, success: {self.success}) \r\n\t{self.statistics.__p_print__()}\r\n\t{self.trip_time.__p_print__()}"
        

def ping(host, pings=1):
    param = '-n' if platform.system().lower()=='windows' else '-c'

    try:
        command = shell_command(f"ping {param} {str(pings)} {host}")
        success = True
    except:
        success = False
        command = b""

    if "Destination host unreachable" in command.decode():
        success = False
    

    if platform.system().lower() == 'windows':
        ping_resp = __ping__(success, host, pings)
        if success:
            packet_data, _, times, _ = command.decode().split("Packets: ")[1].split("\r\n")
            print(packet_data, times)
            ping_resp.statistics.parse_str_win(packet_data)
            ping_resp.trip_time.parse_str_win(times)
        


    return ping_resp
        
def ignore(*args):
    pass