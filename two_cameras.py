#setting up media pipe
#https://www.geeksforgeeks.org/face-and-hand-landmarks-detection-using-python-mediapipe-opencv/
#https://techtutorialsx.com/2021/04/20/python-real-time-hand-tracking/
#https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/
#https://www.youtube.com/watch?v=vQZ4IvB07ec

#code example I built from
#https://github.com/spmallick/learnopencv/blob/master/zoom-gestures

#Good write-up
#https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
import cv2
import mediapipe as mp
from datetime import datetime

WRIST               = 0
THUMB_CMC           = 1
THUMB_MCP           = 2
THUMB_IP            = 3
THUMBS_TIP          = 4
INDEX_FINGER_PIP    = 6
INDEX_FINGER_DIP    = 7
INDEX_FINGER_TIP    = 8
MIDDLE_FINGER_MCP   = 9
MIDDLE_FINGER_PIP   = 10
MIDDLE_FINGER_DIP   = 11
MIDDLE_FINGER_TIP   = 12
RING_FINGER_MCP     = 13
RING_FINGER_PIP     = 14
RING_FINGER_DIP     = 15
RING_FINGER_TIP     = 16
PINKY_MCP           = 17
PINKY_PIP           = 18
PINKY_DIP           = 19
PINKY_TIP           = 20

hand_str = [ 'WRIST', 'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMBS_TIP', 'INDEX_FINGER_PIP', 
             'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 
             'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP', 'RING_FINGER_MCP', 'RING_FINGER_PIP', 
             'RING_FINGER_DIP', 'RING_FINGER_TIP', 'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP' ]

#How do you want to parse file space or comma?
delimeter = ","

print("Initializing");

now = datetime.now()
f = open("hands_output_1.txt", "w")
f.write("Date " + now.strftime("%m/%d/%Y, %H:%M:%S-%f" +"\n"))

f1 = open("hands_output_2.txt", "w")
f1.write("Date " + now.strftime("%m/%d/%Y, %H:%M:%S-%f" +"\n"))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# 3 different ways to read video file input ... uncomment and change accordingly
# read video from file
#cap = cv2.VideoCapture('SIMPLE_VIDEO.mp4')

# read from network
#cap = cv2.VideoCapture('IP_HERE')

# For webcam input:
print("Initializing Camera (may take a minute or two)\n")
cap0 = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(0)

pref_width = 1280
pref_height = 720
pref_fps = 60

#This is taking a long time to set camera settings
#Commenting out for now and will revisit later
#print("Setting Camera 1 Settings")

#cap0.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
#cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
#cap0.set(cv2.CAP_PROP_FPS, pref_fps)

#print("Setting Camera 2 Settings ")

#cap1.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
#cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
#cap1.set(cv2.CAP_PROP_FPS, pref_fps)

print("Confirming Camera Settings")

width = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap0.get(cv2.CAP_PROP_FPS)

width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps1 = cap1.get(cv2.CAP_PROP_FPS)

print("Configuring Video ")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('hands_video_output_1.mp4', fourcc, fps, (width,height))

fourcc1 = cv2.VideoWriter_fourcc(*'mp4v')
out1 = cv2.VideoWriter('hands_video_output_2.mp4', fourcc1, fps1, (width1,height1))

print("Starting Detection")

frame = 0

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    
  while cap0.isOpened():
    success, image = cap0.read()
    success1, image1 = cap1.read()
    
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
    f1.write("frame " + str(frame) + " " + now.strftime("%H:%M:%S-%f") + "\n")
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image1.flags.writeable = False    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)    

    #process hand results for camera 1
    results = hands.process(image)

    #Get image height and width for processing later
    image_height, image_width, _ = image.shape
    image_height1, image_width1, _ = image1.shape
    
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image1.flags.writeable = True
    image1 = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
      
        h, w, c = image.shape
        landmarks = hand_landmarks.landmark
        for lm_id, lm in enumerate(landmarks):
            # Convert landmark coordinates to actual image coordinates
            cx, cy = int(lm.x * w), int(lm.y * h)
        
        #Write all variables and X,Y,Z coordinates to file separated by delimeter variable
        for i in range(len(hand_str)):
            f.write(hand_str[i] + delimeter + "X" + delimeter + str(landmarks[i].x) + delimeter + 
                    "Y" + delimeter + str(landmarks[i].y) + delimeter + "Z" + delimeter + str(landmarks[i].z) + "\n")

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())


    #process hand results for camera 2
    results1 = hands.process(image1)

    if results1.multi_hand_landmarks:
      for hand_landmarks in results1.multi_hand_landmarks:

        h, w, c = image1.shape
        landmarks = hand_landmarks.landmark
        for lm_id, lm in enumerate(landmarks):
            # Convert landmark coordinates to actual image coordinates
            cx, cy = int(lm.x * w), int(lm.y * h)
        
        #Write all variables and X,Y,Z coordinates to file separated by delimeter variable
        for i in range(len(hand_str)):
            f1.write(hand_str[i] + delimeter + "X" + delimeter + str(landmarks[i].x) + delimeter + 
                    "Y" + delimeter + str(landmarks[i].y) + delimeter + "Z" + delimeter + str(landmarks[i].z) + "\n")

        landmarks = hand_landmarks.landmark

        mp_drawing.draw_landmarks(
            image1,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    out.write(image)
    out1.write(image1)
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands(1) - Hit Excape to Exit', image1)    
    cv2.imshow('MediaPipe Hands - Hit Excape to Exit', cv2.flip(image, 1))

cap0.release()
cap1.release()
f.close()
f1.close()
out.release()
out1.release()