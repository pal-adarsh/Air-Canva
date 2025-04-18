import cv2
import numpy as np
import mediapipe as mp
import time

class FingerCanvas:
    def __init__(self):
        # Initialize camera with proper error handling
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
            
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Initialize canvas
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.drawing = False
        
        # MediaPipe Hands configuration
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Drawing settings
        self.colors = {
            'black': (0, 0, 0),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'yellow': (0, 255, 255)
        }
        self.current_color = 'black'
        self.brush_size = 8
        
        # For frame skipping
        self.frame_counter = 0

    def init_canvas(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def detect_finger(self, frame):
        # Mirror the frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        x, y = None, None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get landmarks
                landmarks = hand_landmarks.landmark
                index_tip = landmarks[8]
                thumb_tip = landmarks[4]
                
                h, w = frame.shape[:2]
                index_x = int(index_tip.x * w)
                index_y = int(index_tip.y * h)
                thumb_x = int(thumb_tip.x * w)
                thumb_y = int(thumb_tip.y * h)
                
                # Check pinch gesture
                distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2)**0.5
                self.drawing = distance < 30  # Pinch threshold
                
                if self.drawing:
                    return index_x, index_y, frame
        
        return x, y, frame

    def process_frame(self):
        # Read frame from camera
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return None, None
        
        self.init_canvas(frame)
        x, y, frame = self.detect_finger(frame)
        
        # Draw on canvas if pinching
        if x is not None and y is not None:
            if self.prev_x == 0 and self.prev_y == 0:
                self.prev_x, self.prev_y = x, y
            
            if self.drawing:
                cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), 
                         self.colors[self.current_color], self.brush_size)
            
            self.prev_x, self.prev_y = x, y
        else:
            self.prev_x, self.prev_y = 0, 0
        
        # Combine canvas and camera feed
        output = cv2.add(frame, self.canvas)
        
        # Encode frames
        _, jpeg = cv2.imencode('.jpg', output)
        _, canvas_jpeg = cv2.imencode('.png', self.canvas)
        return jpeg.tobytes(), canvas_jpeg.tobytes()

    def clear_canvas(self):
        if self.cap.isOpened() and self.canvas is not None:
            self.canvas = np.zeros_like(self.canvas)
        self.prev_x, self.prev_y = 0, 0

    def change_color(self, color):
        if color in self.colors:
            self.current_color = color

    def change_brush_size(self, size):
        self.brush_size = int(size)

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'hands'):
            self.hands.close()

# Test the camera
if __name__ == "__main__":
    canvas = FingerCanvas()
    try:
        while True:
            frame_data, _ = canvas.process_frame()
            if frame_data:
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('Test Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        canvas.release()
        cv2.destroyAllWindows()