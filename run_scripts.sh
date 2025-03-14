#!/bin/bash
trap "pkill -P $$; exit" SIGINT SIGTERM EXIT

sudo python3 app.py &
sudo python3 triangleWithSquareOpt.py &
sudo python3 NatNet_SDK_4.1.1/NatNetSDK/Samples/PythonClient/PythonSample.py &
sudo python3 robot-control.py &
wait
