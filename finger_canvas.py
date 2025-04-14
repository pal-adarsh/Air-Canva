import cv2
import numpy as np
import mediapipe as mp

class FingerCanvas:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0
        self.drawing = False
        
        # MediaPipe Hands setup
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

    def init_canvas(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def detect_finger(self, frame):
        # Mirror the frame (fix camera orientation)
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        x, y = None, None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks (for visualization)
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get index finger tip (landmark 8) and thumb tip (landmark 4)
                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]
                
                h, w = frame.shape[:2]
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                
                # Draw circles on finger tips (for visualization)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
                
                # Check pinch gesture
                distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2)**0.5
                self.drawing = distance < 30  # Pinch threshold
                
                if self.drawing:
                    # Draw line between fingers when pinching
                    cv2.line(frame, (index_x, index_y), (thumb_x, thumb_y), 
                             (0, 0, 255), 2)
                    return index_x, index_y, frame
        
        return x, y, frame

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
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
        _, jpeg = cv2.imencode('.jpg', output)
        _, canvas_jpeg = cv2.imencode('.png', self.canvas)
        return jpeg.tobytes(), canvas_jpeg.tobytes()

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas = np.zeros_like(self.canvas)
        self.prev_x, self.prev_y = 0, 0

    def change_color(self, color):
        if color in self.colors:
            self.current_color = color

    def change_brush_size(self, size):
        self.brush_size = size

    def release(self):
        self.cap.release()
        self.hands.close()