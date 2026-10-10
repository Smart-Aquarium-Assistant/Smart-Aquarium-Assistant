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
                stroke_width=1,
                stroke_fill="black",
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
        corner_radius=20,
        fg_color="#00F8FB",
        hover_color="#00D5D8",
        text_color="#001B2E",
        font=("Arial", 16, "bold"),
        command=open_register
    )
    register_button.place(x=25, y=490)

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
        corner_radius=20,
        fg_color="#003047",
        hover_color="#00415B",
        border_width=1,
        border_color="#FFFFFF",
        text_color="#FFFFFF",
        font=("Arial", 16, "bold"),
        command=open_login
    )
    login_button.place(x=25, y=545)

    guest_label = ctk.CTkLabel(
        window,
        text="──────    Або продовжити як гість    ──────",
        font=("Arial", 11, "bold"),
        text_color="#FFFFFF",
        fg_color="transparent",
        cursor="hand2"
    )
    guest_label.place(relx=0.5, y=610, anchor="n")

    def continue_as_guest():
        for widget in window.winfo_children():
            widget.destroy()

        window.configure(fg_color="#001B2E")

        def back_to_welcome():
            for widget in window.winfo_children():
                widget.destroy()

            welcome_page(window)

        back_button = ctk.CTkButton(
            window,
            text="←",
            width=40,
            height=35,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#003047",
            text_color="#FFFFFF",
            font=("Arial", 24, "bold"),
            command=back_to_welcome
        )
        back_button.place(x=15, y=15)

        guest_title = ctk.CTkLabel(
            window,
            text="Вітаємо в Smart Aquarium!",
            font=("Arial", 20, "bold"),
            text_color="#00F8FB",
            fg_color="transparent"
        )
        guest_title.place(x=20, y=200)

        guest_subtitle = ctk.CTkLabel(
            window,
            text="Ви продовжуєте як гість",
            font=("Arial", 14),
            text_color="#FFFFFF",
            fg_color="transparent"
        )
        guest_subtitle.place(x=50, y=245)

    guest_label.bind(
        "<Button-1>",
        lambda event: continue_as_guest()
    )

