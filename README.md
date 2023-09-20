# Finger detection within Google Mediapipe
This code

# Installation
The code is written in Python and uses Google Mediapipe and OpenCV library

This link describes installation

https://developers.google.com/mediapipe/solutions/setup_python

# Running

With proper libraries installed you can run code by double clicking in Windows or on commandline by

py hands_2.py

# Output 

The X,Y,Z coordinates for index finger tip and thumb finger tip is written to text file hands_output.txt

The video output of the detection is written to media file hands_video_output.mp4

# Input from camera or video file
In python code there is a commented out line that reads from SIMPLE_VIDEO.mp4 instead of camera. Modify the code to read from camera or a video.

cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture('SIMPLE_VIDEO.mp4')
