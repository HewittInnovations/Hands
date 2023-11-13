# Finger detection within Google Mediapipe

This code detects finger positions within video and outputs x,y,z coordinates to text file.

# Installation
The code is written in Python and uses Google Mediapipe and OpenCV library

This link describes installation

https://developers.google.com/mediapipe/solutions/setup_python


Download and install Python (needs to be version 3.8 - 3.11)

https://www.python.org/downloads/windows/

Install Pip

https://www.activestate.com/resources/quick-reads/how-to-install-pip-on-windows/

On windows command line

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

or

py get-pip.py

Install Mediapipe

https://developers.google.com/mediapipe/solutions/setup_python

python -m pip install mediapipe

or

py -m pip install mediapipe

# Running

With proper libraries installed you can run code by double clicking in Windows or on commandline by

py hands_2.py

# Output 

The X,Y,Z coordinates for index finger tip and thumb finger tip is written to text file hands_output.txt

Change the delimeter variable to make parsing the output file easier for you.

The video output of the detection is written to media file hands_video_output.mp4

# Input from camera or video file
In python code there is a commented out line that reads from SIMPLE_VIDEO.mp4 instead of camera. Modify the code to read from camera or a video.

cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture('SIMPLE_VIDEO.mp4')

# Support

reach out to chadhewitt@gmail.com

# More info

https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md

![alt text](https://camo.githubusercontent.com/b0f077393b25552492ef5dd7cd9fd13f386e8bb480fa4ed94ce42ede812066a1/68747470733a2f2f6d65646961706970652e6465762f696d616765732f6d6f62696c652f68616e645f6c616e646d61726b732e706e67)

https://github.com/google/mediapipe/blob/master/docs/solutions/holistic.md

![alt text](https://developers.google.com/static/mediapipe/images/solutions/pose_landmarks_index.png)
