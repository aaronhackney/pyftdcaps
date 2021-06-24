from pyftd import FTDClient
from netmiko import ConnectHandler
from getpass import getpass
from os import environ, path
import logging
import argparse

log = logging.getLogger(__name__)


def main(ftd_client, ftd_ssh, cap_file):
    copy_capture(ftd_ssh, cap_file)
    download_capture(ftd_client, cap_file)


def download_capture(ftd_client, cap_file):
    file = ftd_client.download_disk_file(cap_file)
    with open(f"{path.expanduser('~')}/{cap_file}", "wb") as download_file:
        download_file.write(file)
    if path.isfile(f"{path.expanduser('~')}/{cap_file}"):
        log.warning(f"File downloaded and saved at {path.expanduser('~')}/{cap_file}")
    else:
        log.error(f"There was a problem downloading the file {cap_file}")


def copy_capture(ftd_ssh, cap_file):
    # Get to expert mode and copy the capture file to the API download directory
    ssh_session = ConnectHandler(**ftd_ssh)
    ssh_session.send_command("expert", expect_string=r"$")
    ssh_session.send_command("sudo su", expect_string=r":")
    ssh_session.write_channel(ftd_ssh["password"])
    ssh_session.send_command("mkdir -p /ngfw/var/cisco/deploy/pkg/diskfiles")
    ssh_session.send_command(f"cp /mnt/disk0/{cap_file} /ngfw/var/cisco/deploy/pkg/diskfiles/{cap_file}")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ftd_ip", help="IP address of the FTD")
    parser.add_argument("cap_file", help="The capture filename like akh1.pcap")
    parser.add_argument("-n", "--noverify", action="store_true", help="Ignore TLS certificate warnings")
    parser.add_argument("-d", "--debugssh", action="store_true", help="Log SSH session to ssh_log.txt")
    parser.add_argument("-p", "--password", default=None, help="Supply the password as a parameter")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    # Setup required input paramters
    ftd_ip = args.ftd_ip
    user = "admin"
    verify = False if args.noverify else True
    session_log = "ssh_log.txt" if args.debugssh else None
    cap_file = args.cap_file
    password = getpass() if args.password is None else args.password

    # Build the API Client
    ftd_api_client = FTDClient(ftd_ip, user, password, verify=verify)

    # Build the SSH client
    ftd_ssh = {
        "device_type": "cisco_ftd",
        "host": ftd_ip,
        "username": user,
        "password": password,
        "ssh_config_file": "~/.ssh/ssh_config",
        "session_log": session_log,
    }
    main(ftd_api_client, ftd_ssh, cap_file)
