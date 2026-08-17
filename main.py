import flet as ft
import requests
import json
import os

SERVER_URL = "http://192.168.1.7:5000"  # Ajusta a la IP de tu laptop
ARCHIVO_LOCAL = "datos_perfiles.json"

# --- FUNCIONES DE MEMORIA LOCAL (PYTHON NATIVO) ---
def cargar_memoria_local():
    if os.path.exists(ARCHIVO_LOCAL):
        try:
            with open(ARCHIVO_LOCAL, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"Usuario 1": "Sin registrar", "Usuario 2": "Sin registrar"}

def guardar_memoria_local(perfil, nombre):
    datos = cargar_memoria_local()
    datos[perfil] = nombre
    try:
        with open(ARCHIVO_LOCAL, "w") as f:
            json.dump(datos, f)
    except Exception:
        pass

def main(page: ft.Page):
    page.title = "Sistema AIDA"
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado_general = ft.Text(size=14, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER)

    # Cargar nombres guardados previamente en el teléfono
    memoria = cargar_memoria_local()

    def enviar_al_servidor(perfil_etiqueta, nuevo_nombre):
        # 1. Guarda permanentemente en el archivo del teléfono
        guardar_memoria_local(perfil_etiqueta, nuevo_nombre)

        # 2. Intenta enviar a la laptop
        try:
            response = requests.post(
                f"{SERVER_URL}/guardar-nombre",
                json={"perfil": perfil_etiqueta, "nombre": nuevo_nombre},
                timeout=3
            )
            if response.status_code == 200:
                estado_general.value = f"✔ Guardado localmente y en PC"
                estado_general.color = ft.Colors.GREEN_400
            else:
                estado_general.value = f"✔ Guardado en cel (Error PC: {response.status_code})"
                estado_general.color = ft.Colors.AMBER_400
        except Exception:
            estado_general.value = "✔ Guardado en cel (Sin conexión con PC)"
            estado_general.color = ft.Colors.AMBER_400
        page.update()

    def crear_tarjeta_usuario(titulo_perfil, icono):
        nombre_guardado = memoria.get(titulo_perfil, "Sin registrar")
        texto_nombre = ft.Text(nombre_guardado, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_200)
        
        campo_edicion = ft.TextField(
            label=f"Nuevo nombre para {titulo_perfil}",
            border_radius=10,
            filled=True,
            visible=False
        )

        def guardar_cambios(e):
            nombre_ingresado = campo_edicion.value.strip()
            if not nombre_ingresado:
                estado_general.value = f"Escribe un nombre válido para {titulo_perfil}."
                estado_general.color = ft.Colors.RED_300
                page.update()
                return

            texto_nombre.value = nombre_ingresado
            campo_edicion.visible = False
            btn_guardar.visible = False
            btn_editar.visible = True
            
            enviar_al_servidor(titulo_perfil, nombre_ingresado)

        def habilitar_edicion(e):
            campo_edicion.value = texto_nombre.value if texto_nombre.value != "Sin registrar" else ""
            campo_edicion.visible = True
            btn_guardar.visible = True
            btn_editar.visible = False
            estado_general.value = ""
            page.update()

        btn_editar = ft.OutlinedButton(
            "Editar Perfil",
            icon=ft.Icons.EDIT,
            on_click=habilitar_edicion
        )
        
        btn_guardar = ft.FilledButton(
            "Guardar",
            icon=ft.Icons.SAVE,
            visible=False,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            on_click=guardar_cambios
        )

        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=18,
                bgcolor=ft.Colors.GREY_800,
                border_radius=14,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Icon(icono, size=28, color=ft.Colors.TEAL_300),
                                ft.Text(titulo_perfil, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Divider(height=10, color=ft.Colors.GREY_700),
                        ft.Row(
                            [
                                ft.Text("Nombre:", size=14, color=ft.Colors.GREY_400),
                                texto_nombre
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        campo_edicion,
                        ft.Row(
                            [btn_editar, btn_guardar],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=12
                )
            )
        )

    tarjeta_u1 = crear_tarjeta_usuario("Usuario 1", ft.Icons.PERSON)
    tarjeta_u2 = crear_tarjeta_usuario("Usuario 2", ft.Icons.PERSON_OUTLINE)

    page.add(
        ft.Container(
            width=380,
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.MONITOR_HEART, size=32, color=ft.Colors.TEAL_300),
                            ft.Text("SISTEMA AIDA", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text("Panel de Control de Perfiles", size=13, color=ft.Colors.GREY_400),
                    ft.Divider(height=20, color=ft.Colors.GREY_700),
                    tarjeta_u1,
                    tarjeta_u2,
                    ft.Divider(height=20, color=ft.Colors.GREY_700),
                    estado_general
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )

if __name__ == "__main__":
    ft.app(target=main)