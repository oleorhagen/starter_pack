import sys
import argparse

from cf_remote import remote
from cf_remote.utils import package_path, read_json, user_error
from cf_remote import log

def get_args():
    ap = argparse.ArgumentParser(
        description="Spooky CFEngine at a distance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # ALL:
    ap.add_argument(
        "--hosts", "-H", help="What hosts to connect to (ssh)", type=str)
    ap.add_argument(
        "--log-level", "-l", help="Specify detail of logging", type=str, default="WARNING")
    ap.add_argument(
        "command", help="Action to perform", type=str, nargs='?', default="install")

    args = ap.parse_args()
    if args.hosts:
        args.hosts = args.hosts.split(",")
    return args

def run(command, hosts):
    commands = {
        "info": remote.info
    }
    if command not in commands:
        raise NotImplemented
    command = commands[command]
    command(hosts)

def main():
    args = get_args()
    if args.log_level:
        log.set_level(args.log_level)
    if not args.hosts:
        args.hosts = read_json(package_path() + "/hosts.json")
    if not args.hosts:
        user_error("Use -H or hosts.json to specify remote hosts")
    run(args.command, args.hosts)

if __name__ == "__main__":
    main()
