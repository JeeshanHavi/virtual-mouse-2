import cv2  # Import OpenCV for video processing
import mediapipe as mp  # Import MediaPipe for hand tracking
import pyautogui  # Import PyAutoGUI for controlling the mouse

# Open the video file or camera for processing
cap = cv2.VideoCapture() #enter your camera id or video path within the parenthesis

# Initialize MediaPipe Hands module for hand detection
hand_detector = mp.solutions.hands.Hands()
# Initialize MediaPipe drawing utilities for visualizing hand landmarks
drawing_utils = mp.solutions.drawing_utils

# Get the screen width and height for mouse movement
screen_width, screen_height = pyautogui.size()

# Initialize variable to store the y-coordinate of the index finger
index_y = 0

# Start an infinite loop to process video frames
while True:
    # Read a frame from the video
    _, frame = cap.read()
    
    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    
    # Get the dimensions of the frame
    frame_height, frame_width, _ = frame.shape
    
    # Convert the frame to RGB format for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the RGB frame to detect hands
    output = hand_detector.process(rgb_frame)
    
    # Get the detected hand landmarks
    hands = output.multi_hand_landmarks
    
    # If hands are detected, process each hand
    if hands:
        for hand in hands:
            # Draw the hand landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            
            # Iterate through the landmarks to find specific ones
            for id, landmark in enumerate(landmarks):
                # Calculate the x and y coordinates of the landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # If the landmark is the index finger tip (id 8)
                if id == 8:
                    # Draw a circle at the index finger tip position
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # Map the index finger position to the screen coordinates
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                # If the landmark is the thumb tip (id 4)
                if id == 4:
                    # Draw a circle at the thumb tip position
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # Map the thumb position to the screen coordinates
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    
                    # Check the distance between the index finger and thumb
                    print('outside', abs(index_y - thumb_y))
                    # If the index finger and thumb are close enough, perform a click
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()  # Simulate a mouse click
                        pyautogui.sleep(1)  # Pause for a second after clicking
                    # If they are within a certain distance, move the mouse
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)  # Move the mouse to the index finger position
    
    # Display the processed frame in a window
    cv2.imshow('Virtual Mouse', frame)
    
    # Wait for 1 millisecond before processing the next frame
    cv2.waitKey(1)
