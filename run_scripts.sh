#!/bin/bash
trap "pkill -P $$; exit" SIGINT SIGTERM EXIT

sudo -E python3 app.py &
sudo -E python3 triangleWithSquareOpt.py &
sudo -E python3 NatNet_SDK_4.1.1/NatNetSDK/Samples/PythonClient/PythonSample.py &
sudo -E python3 robot-control.py &
wait
