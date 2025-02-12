import flet as ft
import threading
from camera import get_camera, get_frame, encode_frame_to_base64
from scanner import scan_code
import cv2
import pygame
import time
#from database import guardar_codigo, get_code


cap = get_camera()
scanning = False
result_text = None
page = None

pygame.mixer.init()
sound = pygame.mixer.Sound('beep.mp3')


def start_scan(e):
    global scanning
    scanning = True
    threading.Thread(target=scan_loop).start()

def scan_loop():
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
    items = []
    
    #datos = ['id_producto-PF4HD0K', 'hostname-WPHI002']
    for i in datos:
        item = {}
        item["name"] = i.split('-')[0]
        item["value"] = i.split('-')[1]

        items.append(item)
    
    print(items)

def camara_main(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"
    page.window.width = 800
    page.window.height = 600

    result_text = ft.Text(value="Resultado: ", size=20)
    #scan_button = ft.ElevatedButton(text="Scan", on_click=start_scan)
    start_scan(e="")

    camera_image = ft.Image(src="0.png", width=640, height=480)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            #scan_button,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "App con Navegación Lateral"
    
    def cambiar_pagina(seccion):
        page.controls.clear()  # 🔹 Limpia la página antes de cambiar de sección

        if seccion == "inicio":
            home(page)
        elif seccion == "add_items":
            add_items(page)
            #seccion_activa.value = add_items(page)
            #menu_btn.icon = ft.Icons.PERSON
        elif seccion == "configuracion":
            conf(page)
        else:
            home(page)

        page.drawer.open = False  # Cierra el menú lateral después de seleccionar
        page.update()

    contenedor_default = ft.Container(
        content=home(page),
        padding=10,
    )

    # Agregarlo a la página
    page.add(contenedor_default)

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),  # Espacio antes de los botones
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.HOME), ft.Text("Inicio")]),
                #selected=True,
                padding=10,
                on_click=lambda e: cambiar_pagina("inicio"),
            ),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.PLAYLIST_ADD), ft.Text("Agregar Items")]),
                padding=10,
                on_click=lambda e: cambiar_pagina("add_items"),
            ),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.SETTINGS), ft.Text("Configuración")]),
                padding=10,
                on_click=lambda e: cambiar_pagina("configuracion"),
            ),
        ]
    )

    # Barra superior con el botón de menú
    page.appbar = ft.AppBar(
        title=ft.Text("Mi Aplicación"),
        leading=ft.ElevatedButton(" ",icon=ft.Icons.MENU, bgcolor=ft.Colors.BLUE_GREY_500, on_click=lambda e: page.open(drawer)),
        center_title=True,
        bgcolor=ft.Colors.BLUE_GREY_500,
    )

    page.update()

def conf(page):
    code = '4026700424256'
    print(code)
    #get_code(code) 

def add_items(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"
    page.window.width = 800
    page.window.height = 600

    result_text = ft.Text(value="Resultado: ", size=20)
    #scan_button = ft.ElevatedButton(text="Scan", on_click=start_scan)
    start_scan(e="")

    camera_image = ft.Image(src="0.png", width=640, height=480)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            #scan_button,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

def home(page):
    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )


ft.app(target=main, view=ft.WEB_BROWSER)
#ft.app(target=main, view=ft.FLET_APP)
#ft.app(target=main)
