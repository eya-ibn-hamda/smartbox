import subprocess
from tabulate import tabulate

def is_ip_active(ip):
    """
    Check if an IP address is active by sending a ping request.
    Args:
        ip (str): The IP address to check.
    Returns:
        bool: True if the IP is active, False otherwise.
    """
    try:
        subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def parse_device_info(line):
    """
    Parse a line of ARP table output and extract IP and MAC address.
    Args:
        line (str): A line from the 'arp -a' command output.
    Returns:
        dict: A dictionary containing 'IP' and 'mac_addr' keys.
    """
    words = line.split()
    ip = words[1].strip("()")  # Remove parentheses from IP address
    mac = words[3].upper()  # Convert MAC address to uppercase
    return {"IP": ip, "mac_addr": mac}

def get_arp_table():
    """
    Execute the 'arp -a' command and return a list of active devices.
    Returns:
        list: A list of dictionaries, each containing IP and MAC address.
    """
    try:
        result = subprocess.run(["arp", "-a"], stdout=subprocess.PIPE, check=True)
        output = result.stdout.decode().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while retrieving the ARP table: {str(e)}")
        return []

    devices = [
        parse_device_info(line)
        for line in output
        if line.strip() and "at" in line and is_ip_active(parse_device_info(line)["IP"])
    ]
    return devices

def display_devices(devices):
    """
    Display the list of devices in a formatted table.
    Args:
        devices (list): List of dictionaries containing IP and MAC address.
    """
    print(tabulate(devices, headers="keys", tablefmt="pipe"))

def main():
    """Main function to execute the script."""
    devices = get_arp_table()
    display_devices(devices)

if __name__ == "__main__":
    main()

