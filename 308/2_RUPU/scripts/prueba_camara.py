import numpy as np
import cv2
import math

# Initialize the camera; adjust the index based on your setup
# Use 0 for most USB webcams or -1 for the Raspberry Pi Camera Module.
video_capture = cv2.VideoCapture(0)  # For USB webcam; use 0 or try -1 for Pi camera.

# Set the desired resolution; adjust as needed if you experience performance issues.
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height

while True:
    # Capture the frames
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Crop the image - adjust cropping dimensions according to new resolution
    crop_img = frame[240:480, 0:640]  # Adjusted for the chosen resolution

    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding to detect white line
    # Use THRESH_BINARY to detect white areas
    ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        
        # Fit a line to the largest contour
        [vx, vy, x, y] = cv2.fitLine(c, cv2.DIST_L2, 0, 0.01, 0.01)
        
        # Calculate the angle of the line in radians and convert to degrees
        angle = math.degrees(math.atan2(vy, vx))

        # Draw the fitted line on the image
        # Extend the line points to cover the width of the image
        lefty = int((-x * vy / vx) + y)
        righty = int(((crop_img.shape[1] - x) * vy / vx) + y)
        cv2.line(crop_img, (crop_img.shape[1] - 1, righty), (0, lefty), (0, 255, 0), 2)

        # Display the angle on the image
        cv2.putText(crop_img, f"Angle: {angle:.2f} degrees", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        print(f"Angle: {angle:.2f} degrees")

    else:
        print("I don't see the line")

    # Display the resulting frame
    cv2.imshow('frame', crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
