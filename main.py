import asyncio
import cv2
import mediapipe as mp
import numpy as np
import math
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image
import io

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Canvas setup
canvas_width, canvas_height = 640, 480
canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255

# Global variables
prev_x, prev_y = None, None
drawing = True
pinch_threshold = 40

def calculate_distance(point1, point2):
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)

    try:
        while True:
            success, image = cap.read()
            if not success:
                await websocket.send_text("Error: Cannot read from webcam")
                continue

            # Process the frame
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            global prev_x, prev_y, drawing, canvas

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    
                    h, w, _ = image.shape
                    index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                    thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                    
                    distance = calculate_distance((index_x, index_y), (thumb_x, thumb_y))

                    cv2.circle(image, (index_x, index_y), 10, (0, 255, 0), -1)

                    if distance < pinch_threshold:
                        drawing = False
                    else:
                        drawing = True

                    if prev_x is not None and prev_y is not None and drawing:
                        cv2.line(canvas, (prev_x, prev_y), (index_x, index_y), (255, 0, 0), 3)

                    prev_x, prev_y = index_x, index_y
            else:
                prev_x, prev_y = None, None

            # Convert the processed frame to base64
            _, buffer = cv2.imencode('.jpg', image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            # Convert the canvas to base64
            _, canvas_buffer = cv2.imencode('.png', canvas)
            canvas_base64 = base64.b64encode(canvas_buffer).decode('utf-8')

            # Send the processed frame and canvas to the client
            await websocket.send_json({
                "image": img_base64,
                "canvas": canvas_base64
            })

            # Check for client messages
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                if data == "clear":
                    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
                elif data == "save":
                    save_path = "canvas_image.png"
                    cv2.imwrite(save_path, canvas)
                    image_pil = Image.open(save_path)
                    pdf_path = "canvas_image.pdf"
                    image_pil.convert('RGB').save(pdf_path, "PDF")
                    await websocket.send_text(f"Image saved as {pdf_path}")
            except asyncio.TimeoutError:
                pass

    finally:
        cap.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)