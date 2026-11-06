#!/usr/bin/env python3
"""Start pairing on an original SteelSeries Rival 3 Wireless receiver."""
import argparse
import os
import select
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", action="store_true", help="Send the pairing report")
    parser.add_argument("--status", action="store_true", help="Query the 2.4 GHz link")
    args = parser.parse_args()
    matches = []
    for entry in Path("/sys/class/hidraw").glob("hidraw*"):
        device = entry / "device"
        if "HID_ID=0003:00001038:00001830" not in (device / "uevent").read_text().splitlines():
            continue
        if (device / "report_descriptor").read_bytes().startswith(bytes.fromhex("06 c0 ff 09 01 a1 01")):
            matches.append(Path("/dev") / entry.name)
    if len(matches) != 1:
        parser.exit(1, f"Expected one Rival 3 Wireless command interface, found {len(matches)}.\n")
    target = matches[0]
    print(f"Receiver command interface: {target}")
    if args.status:
        with target.open("r+b", buffering=0) as receiver:
            receiver.write(bytes((0, 0xE8)).ljust(65, b"\0"))
            if not select.select([receiver], [], [], 2)[0]:
                parser.exit(1, "Receiver did not answer the link status query.\n")
            response = receiver.read(64)
            if len(response) != 64:
                parser.exit(1, f"Unexpected status report length: {len(response)}.\n")
            print(f"RF status: {response[0]} ({'connected' if response[0] == 4 else 'disconnected'})")
    if args.pair:
        report = bytes((0x00, 0x71, 0x00)).ljust(65, b"\0")
        try:
            with target.open("wb", buffering=0) as receiver:
                written = os.write(receiver.fileno(), report)
        except PermissionError:
            parser.exit(1, "Receiver requires elevated access. Run this script with sudo.\n")
        if written != len(report):
            parser.exit(1, f"Incomplete HID report ({written}/{len(report)} bytes).\n")
        print("Pairing report sent. Hold CPI while switching the mouse from Off to 2.4 GHz.")


if __name__ == "__main__":
    main()
