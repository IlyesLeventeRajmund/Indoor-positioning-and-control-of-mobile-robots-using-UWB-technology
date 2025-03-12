import argparse
import asyncio
import logging
import os
import math
import time
import numpy as np
from collections import deque
#from filterpy.kalman import KalmanFilter
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import requests

from scipy.optimize import least_squares

logger = logging.getLogger(__name__)

rssi_data = {}
SAMPLE_SIZE = 3
TIME_LIMIT = 25
complete_devices = set()
start_time = None
method = 'Trilateration'

device_positions = {
    "DC:C7:ED:2C:04:D1": (1.20, 0.10), #1   sarga
    "D1:DC:74:F2:C7:05": (0.30, 0.80), #2   lila
    "D0:FB:A6:16:7D:AC": (0.20, 0),    #3   piros
    "C3:F0:97:50:8B:EA": (0.90, 0.50)  #4   kek
}


#def initialize_kalman():
#    kf = KalmanFilter(dim_x=1, dim_z=1)
#    kf.x = np.array([[0.]])  
#    kf.F = np.array([[1.]])  
#    kf.H = np.array([[1.]])  
#    kf.P *= 1000.  
#    kf.R = 5  
#    kf.Q = 0.1
#    return kf

kalman_filters = {}

def send_location_to_server(x, y):
    url = "http://10.42.0.1:5001/position"
    data = {"x": x, "y": y}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info("Location data sent to server successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send data to server: {e}")

def load_target_devices(file_path: str):
    with open(file_path, 'r') as file:
        devices = [line.strip() for line in file.readlines()]
    return devices

TARGET_DEVICES = load_target_devices("eszkozok.txt")

def estimate_distance(rssi, rssi_0=-77.5, path_loss_exponent=3):
    return 10 ** ((rssi_0 - rssi) / (10 * path_loss_exponent))

def trilateration(known_positions, distances):
    (x1, y1), (x2, y2), (x3, y3) = known_positions
    d1, d2, d3 = distances

    if any(d <= 0 for d in distances):
        logger.error("Invalid distance values provided.")
        return None

    A = 2 * (x2 - x1)
    B = 2 * (y2 - y1)
    D = 2 * (x3 - x1)
    E = 2 * (y3 - y1)

    C = d1 ** 2 - d2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    F = d1 ** 2 - d3 ** 2 - x1 ** 2 + x3 ** 2 - y1 ** 2 + y3 ** 2

    if B == 0 or E == 0:
        logger.error("Zero division error in trilateration.")
        return None

    x = (C - B * F / E) / (A - B * D / E)
    y = (C - A * x) / B

    return (x, y)

def calculate_average_rssi(device_address):
    if device_address in rssi_data and len(rssi_data[device_address]) >= SAMPLE_SIZE:
        return sum(rssi_data[device_address]) / len(rssi_data[device_address])
    return None

def kalman_filtered_rssi(device_address, rssi):
    if device_address not in kalman_filters:
        kalman_filters[device_address] = initialize_kalman()
    kf = kalman_filters[device_address]
    kf.predict()
    kf.update(rssi)
    return kf.x[0]

def residuals(x, positions, distances):
    return [
        math.sqrt((x[0] - px)**2 + (x[1] - py)**2) - d
        for (px, py), d in zip(positions, distances)
    ]

def least_squares_method(positions, distances):
    initial_guess = [0.0, 0.0] 
    result = least_squares(residuals, initial_guess, args=(positions, distances))
    return result.x  

def simple_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    global start_time, method

    if device.address in TARGET_DEVICES:
        if start_time is None:
            start_time = time.time()

        if device.address in complete_devices:
            return

        logger.info(f"Target device found: {device.address}, RSSI: {advertisement_data.rssi}")

        if device.address not in rssi_data:
            rssi_data[device.address] = []

        rssi_data[device.address].append(advertisement_data.rssi)

        if len(rssi_data[device.address]) >= SAMPLE_SIZE:
            logger.info(f"Elérte a minta méretét: {device.address}")
            complete_devices.add(device.address)

        if len(complete_devices) == 4:
            logger.info("4 eszköz adata megvan, Least Squares Method használata")
            process_all_devices(device_count=4, method='LSM') 
            reset_data()
    
        
        
        elif time.time() - start_time >= TIME_LIMIT:
            if len(complete_devices) >= 3:
                logger.info(f"Időkorlát lejárt, {len(complete_devices)} eszköz adata megvan, Trilateration használata")
                process_all_devices(device_count=len(complete_devices), method='Trilateration')  
                reset_data()  
            else:
                logger.info("Időkorlát lejárt, de nincs meg három eszköz adata, további adatgyűjtés.")
                
                return

def update_device_positions():
    global device_positions
    try:
        response = requests.get("http://10.42.0.1:5001/beacons")
        if response.status_code == 200:
            device_positions = response.json()
            print("Device positions updated:", device_positions)
        else:
            print("Failed to update device positions.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching beacon positions: {e}")

def process_all_devices(device_count, method):
    update_device_positions()
    global device_positions

    distances = {}
    positions = []

    for dev in complete_devices: 
        avg_rssi = calculate_average_rssi(dev)
        if avg_rssi is not None:
            distances[dev] = estimate_distance(avg_rssi)
            positions.append(device_positions[dev])  

    
    if method == 'LSM' and device_count == 4:
        position = least_squares_method(positions, list(distances.values()))
        logger.info(f"Helymeghatározás Least Squares módszerrel: {position}")
        send_location_to_server(position[0], position[1])
    
    
    elif method == 'Trilateration' and device_count >= 3:
        trilateration_distances = list(distances.values())
        position = trilateration(positions[:3], trilateration_distances[:3])  
        logger.info(f"Helymeghatározás Trilateration módszerrel {device_count} eszköz alapján: {position}")
        send_location_to_server(position[0], position[1])


def reset_data():
    global complete_devices, rssi_data, start_time
    complete_devices.clear()
    rssi_data.clear()
    start_time = None
    logger.info("Az adatok nullázva.")

async def main(args: argparse.Namespace):
    global start_time
    scanner = BleakScanner(
        simple_callback, args.services, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    while True:
        logger.info("Scanning started...")
        async with scanner:
            await asyncio.sleep(1.0)  

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    parser.add_argument(
        "--services",
        metavar="<uuid>",
        nargs="*",
        help="UUIDs of one or more services to filter for",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="sets the logging level to debug",
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main(args))
