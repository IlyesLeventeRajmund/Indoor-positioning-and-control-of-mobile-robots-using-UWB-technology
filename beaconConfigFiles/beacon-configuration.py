import argparse
import asyncio
import logging
import os
import math
import time
import numpy as np
from collections import deque
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import requests

SAMPLE_SIZE = 3
rssi_data = {}
robot_opti_location_list =[]

def load_target_devices(file_path: str):
    with open(file_path, 'r') as file:
        devices = [line.strip() for line in file.readlines()]
    return devices

TARGET_DEVICES = load_target_devices("eszkozok.txt")

def get_opti_position():
    robot_opti_location = {"x": 0, "y": 0}
    global robot_opti_location_list
    try:
        response = requests.get("http://10.42.0.1:5001/Optitracking_data_forward")
        if response.status_code ==200:
            robot_opti_location = response.json()
            print("opti locations:",robot_opti_location)
            robot_opti_location_list = extract_marker_positions(robot_opti_location)
            print("opti locationok:",robot_opti_location_list)
        else:
            print("failed to update opti positions")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching  robot opti position: {e}")

def extract_marker_positions(data):
    markers = data.get("Opti_data", {}).get("markers", [])
    return [{"id": marker["id"], "position": marker["position"]} for marker in markers]

def configurate_one_device_position_with_opti(dev_id,advertisement_data: AdvertisementData):
    global device_positions
    global robot_opti_location_list
    one_device_distances = []
    dev_pos = {"x": 0, "y": 0}

    for i in range (3):
        rssi= calculate_average_rssi
        one_device_distances.append(estimate_distance(rssi,rssi_0=-77.5, path_loss_exponent=3))

    device_positions[dev_id] = (dev_pos[x],dev_pos[y])

def calculate_average_rssi(device_address):
    if device_address in rssi_data and len(rssi_data[device_address]) >= SAMPLE_SIZE:
        return sum(rssi_data[device_address]) / len(rssi_data[device_address])
    return None

def estimate_distance(rssi, rssi_0=-77.5, path_loss_exponent=3):
    return 10 ** ((rssi_0 - rssi) / (10 * path_loss_exponent))

def main():
    print

if __name__ == "__main__":
    main()