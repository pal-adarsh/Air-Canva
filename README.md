# Air Slate - Hand Gesture Recognition for Air Drawing
This basic project demonstrates a web-based hand gesture recognition system for air drawing, called Air Slate. The system allows users to write or draw in the air using their hand movements, which are tracked by a webcam. The following functionalities are included:

1. Hand Tracking: The system uses computer vision techniques to detect the hand and track the movement of the index finger. Red dots indicate joint positions, and the green dot represents the tip of the index finger, which is used to draw on the virtual canvas.
2. Air Drawing: The right side of the screen is a digital canvas where the user’s hand movement (tracked by the index finger) is translated into blue lines, simulating writing or drawing.
3. The image shows the writing of "HI" using hand gestures.
4. Canvas Controls: Users can clear the canvas or save their drawings as a PDF using the provided buttons below the canvas.
Features:
a. Clear Canvas: Erases all drawings on the canvas.
b. Save as PDF: Saves the current drawing as a PDF file.
c. Real-time Hand Gesture Tracking: The system is connected to a server for real-time hand tracking.
d. This project demonstrates how computer vision can be combined with interactive features to provide intuitive, gesture-based drawing experiences.

# How to use this repository
1. python -m venv venv
2. activate virtual environment using this command .\venv\Scripts\activate
3. pip install fastapi uvicorn opencv-python mediapipe numpy pillow
4. python main.py
#Note: I used python version 3.11.1

now run your html file
