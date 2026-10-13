import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import os


def welcome_page(window):

    background_path = os.path.join(
        "assets", "images", "underwater.png"
    )

    if not os.path.exists(background_path):
        background_path = "../assets/images/underwater.png"

    if os.path.exists(background_path):
        image = Image.open(background_path).convert("RGBA")
        image = image.resize((320, 650))

        draw = ImageDraw.Draw(image)

        def get_font(size, bold=True):
            font_names = [
                "arialbd.ttf" if bold else "arial.ttf",
                "Arial.ttf"
            ]

            for font_name in font_names:
                try:
                    return ImageFont.truetype(font_name, size)
                except OSError:
                    pass

            return ImageFont.load_default()

        def draw_outlined_text(x, y, text, size, color):
            font = get_font(size)

            draw.text(
                (x, y),
                text,
                font=font,
                fill=color,
                spacing=2
            )

        draw_outlined_text(
            32, 30,
            "Привіт!",
            27,
            "#00F8FB"
        )

        draw_outlined_text(
            32, 75,
            "Раді бачити тебе\nв нашому додатку!",
            22,
            "#FFFFFF"
        )

        draw_outlined_text(
            32, 165,
            "Створи свій акаунт і почни\nдосліджувати підводний світ!",
            13,
            "#FFFFFF"
        )

        background_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(320, 650)
        )

        background_label = ctk.CTkLabel(
            window,
            text="",
            image=background_image
        )
        background_label.place(x=0, y=0)
        background_label.lower()

    else:
        window.configure(fg_color="#001B2E")

    # Регистрация
    def open_register():
        from register import register_page

        for widget in window.winfo_children():
            widget.destroy()

        register_page(window)

    register_button = ctk.CTkButton(
        window,
        text="Зареєструватися",
        width=270,
        height=45,
        corner_radius=15,
        fg_color="#00F8FB",
        hover_color="#00D5D8",
        text_color="#001B2E",
        font=("Arial", 15, "bold"),
        command=open_register
    )
    register_button.place(x=25, y=455)

    # Вход
    def open_login():
        from login import login_page

        for widget in window.winfo_children():
            widget.destroy()

        login_page(window)

    login_button = ctk.CTkButton(
        window,
        text="Увійти",
        width=270,
        height=45,
        corner_radius=15,
        fg_color="#003047",
        hover_color="#004B65",
        border_width=1,
        border_color="#00F8FB",
        text_color="#FFFFFF",
        font=("Arial", 15, "bold"),
        command=open_login
    )
    login_button.place(x=25, y=510)

    # Вход администратора
    def open_admin():
        from home import home_page

        home_page(window)

    admin_button = ctk.CTkButton(
        window,
        text="Увійти як адміністратор",
        width=270,
        height=45,
        corner_radius=15,
        fg_color="#001B2E",
        hover_color="#003047",
        border_width=1,
        border_color="#60D48C",
        text_color="#60D48C",
        font=("Arial", 14, "bold"),
        command=open_admin
    )
    admin_button.place(x=25, y=565)


