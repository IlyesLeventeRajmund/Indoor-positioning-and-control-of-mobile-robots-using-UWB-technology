import argparse
import ast
import asyncio
import logging
import os
import math
import time
import threading
import numpy as np
from collections import deque
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from scipy.optimize import least_squares

logger = logging.getLogger(__name__)

class BeaconLocalization:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        self.is_alive = False
        self.position_lock = threading.Lock()
        self.tracking_thread = None
        self.rssi_data = {}
        self.SAMPLE_SIZE = 3
        self.TIME_LIMIT = 25
        self.complete_devices = set()
        self.start_time = None
        self.method = 'Trilateration'
        self.kalman_filters = {}
        
        # Device positions (beacons)
        # TODO: These should be in config
        # TODO: remove hungarian 
        self.device_positions = {
            "DC:C7:ED:2C:04:D1": (1.9146842956542969, -0.40974411368370056, 0.5664147138595581),  #kek
            "D1:DC:74:F2:C7:05": (-0.12133240699768066, -3.605344772, 0.889655590057373), #sarga
            "D0:FB:A6:16:7D:AC": (1.2901723384857178, -2.0813114643096924, 0.5793644785881042),    #cekla
            "C3:F0:97:50:8B:EA": (-1.4125473499298096, -0.4882330298423767, 0.6970527768135071), #zold
            "EC:7F:50:BE:D2:D1": (-1.2612544298171997, -1.9906595945358276, 0.7028661370277405),   #rozsaszin
            "C0-0B-BD-29-25-9C": (1.9020336866378784, 1.0856691598892212, 0.6161160469055176), #sargazoldmarkerezett
            "DA-53-A2-B5-96-75": (0.45428064465522766, 1.9725672006607056, 0.5662478804588318), #bordo15
            "D6-7E-98-FA-DE-01": (-1.4703487157821655, 1.0286478996276855, 0.7123057246208191),#rozsaszin14es
        }
        
        # Load target devices
        # TODO: This shoud be in config
        self.TARGET_DEVICES = self.load_target_devices("eszkozok.txt")
    
    def set_coordinates(self, x: float, y: float):
        """Set robot coordinates with thread safety"""
        with self.position_lock:
            self.x = x
            self.y = y

    def get_coordinates(self):
        """Get current robot coordinates with thread safety"""
        with self.position_lock:
            return self.x, self.y

    def load_target_devices(self, file_path: str):
        """Load target devices from a file"""
        devices = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    mac, coords = line.strip().split(": ", 1)
                    devices[mac.strip('"')] = ast.literal_eval(coords)
            return devices
        except FileNotFoundError:
            logger.error(f"Target devices file not found: {file_path}")
            return {}
        except Exception as e:
            logger.error(f"Error loading target devices: {e}")
            return {}

    def estimate_distance(self, rssi, rssi_0=-77.5, path_loss_exponent=3):
        """Estimate distance based on RSSI value"""
        return 10 ** ((rssi_0 - rssi) / (10 * path_loss_exponent))

    def trilateration(self, known_positions, distances):
        """Calculate position using trilateration"""
        (x1, y1, _), (x2, y2, _), (x3, y3, _) = known_positions
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

    def calculate_average_rssi(self, device_address):
        """Calculate average RSSI for a device"""
        if device_address in self.rssi_data and len(self.rssi_data[device_address]) >= self.SAMPLE_SIZE:
            return sum(self.rssi_data[device_address]) / len(self.rssi_data[device_address])
        return None

    def residuals(self, x, positions, distances):
        """Calculate residuals for least squares optimization"""
        return [
            math.sqrt((x[0] - px[0])**2 + (x[1] - px[1])**2) - d
            for px, d in zip(positions, distances)
        ]

    def least_squares_method(self, positions, distances):
        """Calculate position using least squares method"""
        initial_guess = [0.0, 0.0] 
        result = least_squares(self.residuals, initial_guess, args=(positions, distances))
        return result.x

    def ble_callback(self, device: BLEDevice, advertisement_data: AdvertisementData):
        """Callback for BLE scanner when a device is detected"""
        if device.address in self.TARGET_DEVICES:
            if self.start_time is None:
                self.start_time = time.time()

            if device.address in self.complete_devices:
                return

            logger.info(f"Target device found: {device.address}, RSSI: {advertisement_data.rssi}")

            if device.address not in self.rssi_data:
                self.rssi_data[device.address] = []

            self.rssi_data[device.address].append(advertisement_data.rssi)

            if len(self.rssi_data[device.address]) >= self.SAMPLE_SIZE:
                logger.info(f"Elérte a minta méretét: {device.address}")
                self.complete_devices.add(device.address)

            if len(self.complete_devices) == 4:
                logger.info("4 eszköz adata megvan, Least Squares Method használata")
                self.process_all_devices(device_count=4, method='LSM') 
                self.reset_data()
            
            elif time.time() - self.start_time >= self.TIME_LIMIT:
                if len(self.complete_devices) >= 3:
                    logger.info(f"Időkorlát lejárt, {len(self.complete_devices)} eszköz adata megvan, Trilateration használata")
                    self.process_all_devices(device_count=len(self.complete_devices), method='Trilateration')  
                    self.reset_data()  
                else:
                    logger.info("Időkorlát lejárt, de nincs meg három eszköz adata, további adatgyűjtés.")
                    return

    def process_all_devices(self, device_count, method):
        """Process collected data and calculate robot position"""
        distances = {}
        positions = []

        for dev in self.complete_devices: 
            avg_rssi = self.calculate_average_rssi(dev)
            if avg_rssi is not None:
                distances[dev] = self.estimate_distance(avg_rssi)
                positions.append(self.device_positions[dev][:2])    

        if method == 'LSM' and device_count == 4:
            new_location = self.least_squares_method(positions, list(distances.values()))
            self.set_coordinates(new_location[0], new_location[1])
            logger.info(f"Helymeghatározás Least Squares módszerrel: {self.get_coordinates()}")
        
        elif method == 'Trilateration' and device_count >= 3:
            new_location = self.trilateration(positions[:3], list(distances.values())[:3])
            if new_location:
                self.set_coordinates(new_location[0], new_location[1])
                logger.info(f"Helymeghatározás Trilateration módszerrel {device_count} eszköz alapján: {self.get_coordinates()}")

    def reset_data(self):
        """Reset collected data"""
        self.complete_devices.clear()
        self.rssi_data.clear()
        self.start_time = None
        logger.info("Az adatok nullázva.")

    async def run_ble_scanning(self, scanner):
        """Run BLE scanning in an infinite loop"""
        while self.is_alive:
            logger.info("Scanning started...")
            async with scanner:
                await asyncio.sleep(1.0)
            
            if not self.is_alive:
                break
    
    def start_tracking(self, services=None, macos_use_bdaddr=False):
        """Start the BLE tracking process"""
        if self.is_alive:
            logger.info("Tracking already running.")
            return
        
        self.is_alive = True
        self.tracking_thread = threading.Thread(target=self._tracking_thread, args=(services, macos_use_bdaddr))
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
        logger.info("BLE tracking started")
    
    def stop_tracking(self):
        """Stop the BLE tracking process"""
        if not self.is_alive:
            logger.info("Tracking not running.")
            return
        
        logger.info("Stopping BLE tracking...")
        self.is_alive = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=2.0)
            self.tracking_thread = None
        logger.info("BLE tracking stopped")
    
    def _tracking_thread(self, services=None, macos_use_bdaddr=False):
        """Thread function that runs the asyncio event loop for BLE scanning"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            scanner = BleakScanner(
                self.ble_callback, services, cb=dict(use_bdaddr=macos_use_bdaddr)
            )
            
            loop.run_until_complete(self._run_scanning(scanner))
        except Exception as e:
            logger.error(f"Error in tracking thread: {e}")
        finally:
            loop.close()
    
    async def _run_scanning(self, scanner):
        """Run the BLE scanning loop"""
        while self.is_alive:
            logger.info("Scanning started...")
            async with scanner:
                await asyncio.sleep(1.0)
            
            if not self.is_alive:
                break

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )
    
    robot = BeaconLocalization()

    robot.start_tracking()
    
    try:
        print("Robot tracking running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            print(f"Current position: {robot.get_coordinates()}")
    except KeyboardInterrupt:
        print("Stopping tracking...")
    finally:
        robot.stop_tracking()