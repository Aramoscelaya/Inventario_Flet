import cv2

import base64

def get_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("No se pudo abrir la cámara.")
    return cap

def get_frame(cap):
    ret, frame = cap.read()
    if not ret:
        raise Exception("No se pudo leer el frame.")
    return frame

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')
