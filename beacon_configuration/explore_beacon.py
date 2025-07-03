import argparse
import asyncio

from bleak import BleakScanner

ignored_macs = [
    "DC:C7:ED:2C:04:D1",
    "D1:DC:74:F2:C7:05",
    "D0:FB:A6:16:7D:AC",
    "C3:F0:97:50:8B:EA",
    "EC:7F:50:BE:D2:D1",
    "C0-0B-BD-29-25-9C",
    "DA-53-A2-B5-96-75",
    "D6-7E-98-FA-DE-01",
    "4E-EB-AF-16-F2-56",
    "D3-DE-76-F4-C9-07",
    "CF-DA-72-F0-C5-03",
    "72-EC-6D-C0-A6-E9",
    "EA-7D-4E-BC-D0-CF",
    "CE-F9-A4-14-7B-AA",
    "67-DE-AF-C7-A1-B9",
    "4E-EB-AF-16-F2-56",
]

async def main(args: argparse.Namespace):
    print("scanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True,
        service_uuids=args.services,
        cb=dict(use_bdaddr=args.macos_use_bdaddr),
    )

    for d, a in devices.values():
        if d.address.upper() in [mac.upper() for mac in ignored_macs]:
            continue
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--services",
        metavar="<uuid>",
        nargs="*",
        help="UUIDs of one or more services to filter for",
    )

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
