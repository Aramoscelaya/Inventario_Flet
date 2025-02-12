import flet as ft
import threading
from camera import get_camera, get_frame, encode_frame_to_base64
from scanner import scan_code
import cv2
import pygame
import time

cap = get_camera()
scanning = False
result_text = None
page = None

pygame.mixer.init()
sound = pygame.mixer.Sound('beep.mp3')


def scan_loop2():
    global scanning, page
    code_count = {}
    frames_checked = 0

    while scanning:
        frame = get_frame(cap)
        code = scan_code(frame)

        if code:
            if code in code_count:
                code_count[code] += 1
            else:
                code_count[code] = 1
            frames_checked += 1 

            height, width, _ = frame.shape
            cv2.rectangle(frame, (50, height - 60), 
                          (width - 50, height - 10), 
                          (0, 255, 0), -1)
            cv2.putText(frame, f"Detected: {code}", 
                        (60, height - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 
                        (255, 255, 255), 2)

            if frames_checked >= 10:
                for c, count in code_count.items():
                    if count >= 10:
                        result_text.value = f"Resultado: {c}"
                        getCode(c)
                        sound.play()
                        time.sleep(0.5)
                        break

                code_count.clear()
                frames_checked = 0

        page.image.src_base64 = encode_frame_to_base64(frame)
        page.update()

def getCode(code):
    codes = code[0]
    # Dividir la cadena por comas
    datos = codes.split(',')
    
    print('Este es el codigo final')
    print(datos)

def camara_main2(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"
    page.window.width = 800
    page.window.height = 600

    result_text = ft.Text(value="Resultado: ", size=20)
    global scanning
    scanning = True
    threading.Thread(target=scan_loop2).start()

    camera_image = ft.Image(src="0.png", width=640, height=480)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )



ft.app(target=camara_main2)
