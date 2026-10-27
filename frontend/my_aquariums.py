import os
import customtkinter as ctk
from PIL import Image, ImageOps

BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CARD_DARK = "#002B40"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"
GREEN = "#43E6A1"
ORANGE = "#FFB000"
BLACK = "#000000"


def my_aquariums_page(window, aquarium=None):

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color=BG_COLOR)

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    icons_folder = os.path.join(
        project_folder, "assets", "icons"
    )

    images_folder = os.path.join(
        project_folder, "assets", "images"
    )

    main = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        fg_color=BG_COLOR,
        corner_radius=0,
        border_width=0
    )
    main.place(x=0, y=0)

    # ---------------- ВЕРХНЯЯ ПАНЕЛЬ ----------------

    def back_profile():
        from profile import profile_page
        profile_page(window, aquarium)

    ctk.CTkButton(
        main,
        text="←",
        width=34,
        height=34,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 27, "bold"),
        command=back_profile
    ).place(x=12, y=8)

    ctk.CTkLabel(
        main,
        text="Мої акваріуми",
        font=("Arial", 19, "bold"),
        text_color=WHITE
    ).place(relx=0.5, y=25, anchor="center")

    # ---------------- ОПОВЕЩЕНИЯ ----------------

    def open_notifications():
        notifications_page(window, aquarium)

    bell_image = None

    bell_path = os.path.join(
        icons_folder, "bell.png"
    )

    if os.path.exists(bell_path):
        try:
            with Image.open(bell_path) as source:
                img = source.convert("RGBA")

            bell_image = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(22, 22)
            )

        except Exception as error:
            print("Помилка іконки сповіщень:", error)

    ctk.CTkButton(
        main,
        text="" if bell_image else "♧",
        image=bell_image,
        width=34,
        height=34,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 22, "bold"),
        command=open_notifications
    ).place(x=274, y=8)

    main.bell_image = bell_image

    # ---------------- ОБРАБОТКА ФОТОГРАФИЙ ----------------

    def load_image(filename, size, border=2):

        path = os.path.join(images_folder, filename)

        if not os.path.exists(path):
            return None

        try:
            with Image.open(path) as source:
                img = source.convert("RGB")

            img = ImageOps.fit(
                img,
                size,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )

            bordered = ImageOps.expand(
                img,
                border=border,
                fill=BLACK
            )

            return ctk.CTkImage(
                light_image=bordered,
                dark_image=bordered,
                size=bordered.size
            )

        except Exception as error:
            print(
                f"Помилка завантаження {filename}: {error}"
            )
            return None

    def load_photo(name, size, border=2):

        image = load_image(
            name + ".jpg",
            size,
            border
        )

        if image is None:
            image = load_image(
                name + ".png",
                size,
                border
            )

        return image

    # ---------------- ФОТОГРАФИИ ----------------

    reef_banner = load_photo(
        "reef",
        (264, 124),
        border=2
    )

    grass_square = load_photo(
        "grass",
        (68, 68),
        border=2
    )

    reef_square = load_photo(
        "reef",
        (68, 68),
        border=2
    )

    nano_square = load_photo(
        "nano",
        (68, 68),
        border=2
    )

    # ---------------- БОЛЬШАЯ КАРТОЧКА ----------------

    top_card = ctk.CTkFrame(
        main,
        width=296,
        height=168,
        fg_color=CARD_COLOR,
        border_width=1,
        border_color=CYAN,
        corner_radius=14
    )
    top_card.place(x=12, y=58)

    ctk.CTkLabel(
        top_card,
        text="" if reef_banner else "Фото акваріума",
        image=reef_banner,
        width=268,
        height=128,
        corner_radius=0,
        fg_color=CARD_DARK,
        text_color=GRAY,
        font=("Arial", 12)
    ).place(
        relx=0.5,
        y=12,
        anchor="n"
    )

    # ---------------- ПРОСТАЯ КНОПКА 120 Л ----------------

    volume = ctk.CTkButton(
        top_card,
        text="120 л",
        width=66,
        height=26,
        fg_color="#004052",
        hover_color="#00566A",
        text_color=WHITE,
        border_width=0,
        corner_radius=9,
        font=("Arial", 12, "bold"),
        command=lambda: None
    )

    volume.place(
        x=15,
        y=118
    )

    # ---------------- МАЛЕНЬКИЕ КАРТОЧКИ ----------------

    cards = [
        (
            "Мій травник",
            GREEN,
            "Все в нормі",
            grass_square
        ),
        (
            "Мій риф",
            ORANGE,
            "Потрібна увага",
            reef_square
        ),
        (
            "Мій Нано-акваріум",
            GREEN,
            "Все в нормі",
            nano_square
        )
    ]

    y_positions = [244, 359, 474]

    for i, (title, color, status, image) in enumerate(cards):

        card = ctk.CTkFrame(
            main,
            width=296,
            height=110,
            fg_color=CARD_COLOR,
            border_width=1,
            border_color=CYAN,
            corner_radius=14
        )

        card.place(
            x=12,
            y=y_positions[i]
        )

        photo_label = ctk.CTkLabel(
            card,
            text="" if image else "Фото",
            image=image,
            width=72,
            height=72,
            corner_radius=0,
            fg_color=BLACK,
            text_color=GRAY,
            font=("Arial", 10)
        )

        photo_label.place(
            x=10,
            rely=0.5,
            anchor="w"
        )

        text_frame = ctk.CTkFrame(
            card,
            width=146,
            height=84,
            fg_color="transparent",
            corner_radius=0
        )

        text_frame.place(
            x=94,
            rely=0.5,
            anchor="w"
        )

        ctk.CTkLabel(
            text_frame,
            text=title,
            width=146,
            height=30,
            font=("Arial", 12, "bold"),
            text_color=WHITE,
            anchor="w",
            justify="left",
            wraplength=140
        ).place(
            x=0,
            y=0
        )

        ctk.CTkLabel(
            text_frame,
            text="120 л",
            font=("Arial", 11),
            text_color=WHITE,
            anchor="w"
        ).place(
            x=0,
            y=32
        )

        ctk.CTkLabel(
            text_frame,
            text=status,
            width=146,
            height=22,
            font=("Arial", 10, "bold"),
            text_color=color,
            anchor="w",
            justify="left",
            wraplength=140
        ).place(
            x=0,
            y=58
        )

        ctk.CTkLabel(
            card,
            text="➜",
            width=22,
            height=32,
            text_color=CYAN,
            font=("Arial", 21, "bold")
        ).place(
            x=270,
            rely=0.5,
            anchor="center"
        )

    # ---------------- НИЖНЯЯ НАВИГАЦИЯ ----------------
    # Оставлена без изменений из твоего исходного кода.

    nav = ctk.CTkFrame(
        main,
        width=304,
        height=55,
        fg_color=CARD_COLOR,
        border_width=1,
        border_color=CYAN,
        corner_radius=20
    )

    nav.place(
        x=8,
        y=590
    )

    nav_items = [
        ("home.png", "Головна"),
        ("analysis.png", "Аналіз"),
        ("care.png", "Догляд"),
        ("history1.png", "Історія"),
        ("profile.png", "Профіль")
    ]

    nav_images = []

    def navigate(page):

        if page == "Головна":
            from home import home_page
            home_page(window, aquarium)

        elif page == "Аналіз":
            from analysis import analysis_page

            analysis_page(
                window,
                back_command=lambda: my_aquariums_page(
                    window, aquarium
                ),
                aquarium=aquarium
            )

        elif page == "Догляд":
            from care import care_page
            care_page(window, aquarium)

        elif page == "Історія":
            from history import history_page
            history_page(window, aquarium)

        elif page == "Профіль":
            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, name) in enumerate(nav_items):

        icon = None

        path = os.path.join(
            icons_folder,
            icon_file
        )

        if os.path.exists(path):
            try:
                with Image.open(path) as source:
                    img = source.convert("RGBA")

                icon = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(27, 27)
                )

                nav_images.append(icon)

            except Exception as error:
                print(
                    f"Помилка іконки {icon_file}: {error}"
                )

        ctk.CTkButton(
            nav,
            text="",
            image=icon,
            width=48,
            height=44,
            fg_color=(
                "#00435A"
                if name == "Профіль"
                else "transparent"
            ),
            hover_color="#00506B",
            command=lambda n=name: navigate(n)
        ).place(
            x=4 + i * 59,
            y=5
        )

    nav.nav_images = nav_images


# ==================================================
#                  СТРАНИЦА ОПОВЕЩЕНИЙ
# ==================================================

def notifications_page(window, aquarium=None):

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color=BG_COLOR)

    main = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        fg_color=BG_COLOR,
        corner_radius=0,
        border_width=0
    )
    main.place(x=0, y=0)

    # ---------------- ВЕРХНЯЯ ПАНЕЛЬ ----------------

    def go_back():
        my_aquariums_page(window, aquarium)

    ctk.CTkButton(
        main,
        text="←",
        width=34,
        height=34,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 27, "bold"),
        command=go_back
    ).place(
        x=12,
        y=8
    )

    ctk.CTkLabel(
        main,
        text="Оповіщення",
        font=("Arial", 19, "bold"),
        text_color=WHITE
    ).place(
        relx=0.5,
        y=25,
        anchor="center"
    )

    # ---------------- ЗАГОЛОВОК ----------------

    ctk.CTkLabel(
        main,
        text="Ваші сповіщення",
        font=("Arial", 15, "bold"),
        text_color=WHITE,
        anchor="w"
    ).place(
        x=18,
        y=73
    )

    # ---------------- КАРТОЧКА ОПОВЕЩЕНИЙ ----------------

    empty_card = ctk.CTkFrame(
        main,
        width=284,
        height=220,
        fg_color=CARD_COLOR,
        corner_radius=16,
        border_width=1,
        border_color="#06465A"
    )

    empty_card.place(
        x=18,
        y=125
    )

    ctk.CTkLabel(
        empty_card,
        text="♧",
        font=("Arial", 42),
        text_color=CYAN
    ).place(
        relx=0.5,
        y=38,
        anchor="center"
    )

    ctk.CTkLabel(
        empty_card,
        text="Поки немає оповіщень",
        font=("Arial", 15, "bold"),
        text_color=WHITE
    ).place(
        relx=0.5,
        y=95,
        anchor="center"
    )

    ctk.CTkLabel(
        empty_card,
        text="Тут з'являтимуться повідомлення\n"
             "про стан води, догляд та інші\n"
             "важливі події у твоїх акваріумах.",
        font=("Arial", 11),
        text_color=GRAY,
        justify="center"
    ).place(
        relx=0.5,
        y=148,
        anchor="center"
    )

    # ---------------- КНОПКА ВОЗВРАТА ----------------

    ctk.CTkButton(
        main,
        text="До моїх акваріумів",
        width=220,
        height=40,
        fg_color=CARD_COLOR,
        hover_color="#00506B",
        border_width=1,
        border_color=CYAN,
        corner_radius=12,
        text_color=WHITE,
        font=("Arial", 12, "bold"),
        command=go_back
    ).place(
        relx=0.5,
        y=390,
        anchor="center"
    )
