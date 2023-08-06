import argparse
import logging
import sys
from shekan_cli.shekan import *
from shekan_cli.functions import *
import os


version = '0.0.1'
logger = logging.getLogger(__name__)


def main():
    
    if os.name != 'posix':
        print("Sorry, Currently Just Linux is Supported")
        return 1

    parser = argparse.ArgumentParser(description="CLI for Shekan BY Seyed Moala Takhtdar")
    
    parser.add_argument(
        "--version", action="version", version=f"shekan {version}"
    )

    subparsers = parser.add_subparsers()
    
    enable = subparsers.add_parser("enable", help="Enable Shekan DNS")
    enable.set_defaults(op="enable")

    disable = subparsers.add_parser("disable", help="Disable Shekan DNS")
    disable.set_defaults(op="disable")

    status = subparsers.add_parser("status", help="Status of Shekan")
    status.set_defaults(op="status")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    elif args.op == "enable":
        enable_shekan()

    elif args.op == "disable":
        disable_shekan()

    elif args.op == "status":
        status_shekan()




if __name__ == '__main__':
    main()