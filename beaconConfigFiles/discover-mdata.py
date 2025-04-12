from bleak import BleakScanner
import asyncio

async def main():
    print("Keresés...")
    devices = await BleakScanner.discover(return_adv=True)
    for d, adv in devices.values():
        print(f"{d.address} | {d.name} | RSSI: {adv.rssi} | Manufacturer: {adv.manufacturer_data}")

asyncio.run(main())
