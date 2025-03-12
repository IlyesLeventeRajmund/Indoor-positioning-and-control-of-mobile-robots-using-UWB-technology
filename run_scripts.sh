#!/bin/bash
trap "kill 0" EXIT

python3 app.py &
python3 NatNet_SDK_4.1.1/NatNetSDK/Samples/PythonClient/PythonSample.py &
python3 robot-control.py &
python3 triangleWithSquareOpt.py &
wait
