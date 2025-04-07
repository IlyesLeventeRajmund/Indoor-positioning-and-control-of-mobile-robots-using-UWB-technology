import asyncio
import logging
import statistics
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


TARGET_DEVICE = "C3:F0:97:50:8B:EA"


rssi_values = []

def rssi_logger_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    if device.address == TARGET_DEVICE:
        rssi = advertisement_data.rssi
        rssi_values.append(rssi)  
        logger.info(f"RSSI from {device.address}: {rssi}")


async def main():
    scanner = BleakScanner(rssi_logger_callback)
    await scanner.start()
    
    try:
        logger.info(f"Listening for device: {TARGET_DEVICE}")
        await asyncio.sleep(10.0)  
    finally:
        await scanner.stop()

        if rssi_values:
            avg_rssi = sum(rssi_values) / len(rssi_values)
            median_rssi = statistics.median(rssi_values)
            
            logger.info(f"Átlag RSSI: {avg_rssi}")
            logger.info(f"Medián RSSI: {median_rssi}")
        else:
            logger.info("Nem érkezett RSSI adat az eszköztől.")

if __name__ == "__main__":
    asyncio.run(main())