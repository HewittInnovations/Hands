#setting up media pipe
#https://www.geeksforgeeks.org/face-and-hand-landmarks-detection-using-python-mediapipe-opencv/
#https://techtutorialsx.com/2021/04/20/python-real-time-hand-tracking/
#https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
#https://www.youtube.com/watch?v=vQZ4IvB07ec

#code example I built from
#https://colab.research.google.com/drive/16UOYQ9hPM6L5tkq7oQBl1ULJ8xuK5Lae

#Good write-up
#https://github.com/google/mediapipe/blob/master/docs/solutions/holistic.md

import cv2
import mediapipe as mp
from datetime import datetime

now = datetime.now()
f = open("holistic_output.txt", "w")
f.write("Date " + now.strftime("%m/%d/%Y, %H:%M:%S-%f" +"\n"))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# 3 different ways to read video file input ... uncomment and change accordingly
# read video from file
#cap = cv2.VideoCapture('SIMPLE_VIDEO.mp4')

# read from network
#cap = cv2.VideoCapture('IP_HERE')

# For webcam input:
cap = cv2.VideoCapture(0)

pref_width = 1280
pref_height = 720
pref_fps = 30

cap.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
cap.set(cv2.CAP_PROP_FPS, pref_fps)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('holistic_video_output.mp4', fourcc, fps, (width,height))

frame = 0

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    
    
  while cap.isOpened():
    success, image = cap.read()
    
    #Hit ESC key to exit
    if cv2.waitKey(5) & 0xFF == 27:
      break
      
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    now = datetime.now()
    frame = frame + 1
    f.write("frame " + str(frame) + " " + now.strftime("%H:%M:%S-%f") + "\n")
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    #Get image height and width for processing later
    image_height, image_width, _ = image.shape

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())
            
    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS)
            
    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS)
        
    out.write(image)
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands - Hit Excape to Exit', cv2.flip(image, 1))

cap.release()
f.close()
out.release()
