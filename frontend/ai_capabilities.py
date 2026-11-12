
import os
import customtkinter as ctk
from PIL import Image


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")

BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"


def ai_capabilities_page(window, aquarium=None):

    # Очищаем предыдущую страницу
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("320x650")
    window.configure(fg_color=BG_COLOR)
    window.resizable(False, False)

    main_frame = ctk.CTkFrame(
        window,
        fg_color=BG_COLOR,
        corner_radius=0
    )
    main_frame.pack(fill="both", expand=True)

    # ---------- ВЕРХНЯЯ ПАНЕЛЬ ----------

    header = ctk.CTkFrame(
        main_frame,
        fg_color=BG_COLOR,
        height=55,
        corner_radius=0
    )
    header.pack(fill="x", padx=12, pady=(8, 8))
    header.pack_propagate(False)

    back_button = ctk.CTkButton(
        header,
        text="←",
        width=30,
        height=34,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 27, "bold"),
        command=lambda: go_back()
    )
    back_button.pack(side="left")

    title_label = ctk.CTkLabel(
        header,
        text="AI Можливості",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    )
    title_label.place(
        relx=0.52,
        rely=0.5,
        anchor="center"
    )

    # ---------- УВЕДОМЛЕНИЯ ----------

    def open_reminders():
        from reminders import reminders_page
        reminders_page(window, aquarium)

    bell_path = os.path.join(ICONS_DIR, "bell.png")

    if os.path.exists(bell_path):

        bell_original = Image.open(bell_path).convert("RGBA")

        bell_image = ctk.CTkImage(
            light_image=bell_original,
            dark_image=bell_original,
            size=(23, 23)
        )

        bell_button = ctk.CTkButton(
            header,
            text="",
            image=bell_image,
            width=28,
            height=32,
            fg_color="transparent",
            hover_color=CARD_COLOR,
            border_width=0,
            command=open_reminders
        )

        header.bell_image = bell_image

    else:
        bell_button = ctk.CTkButton(
            header,
            text="♟",
            width=28,
            height=32,
            fg_color="transparent",
            hover_color=CARD_COLOR,
            text_color=CYAN,
            command=open_reminders
        )

    bell_button.pack(side="right")

    # ---------- КАРТОЧКИ AI ----------

    cards_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color=BG_COLOR,
        corner_radius=0,
        scrollbar_button_color=CARD_COLOR,
        scrollbar_button_hover_color=CYAN
    )

    cards_frame.pack(
        fill="both",
        expand=True,
        padx=17,
        pady=(0, 5)
    )

    cards_frame.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="cards"
    )

    cards = [
        ("auto_diagnostics.png", "Авто-\nДіагностика", "◉"),
        ("care_plan.png", "План догляду", "▦"),
        ("compatibility.png", "Сумісність", "♧"),
        ("parameters.png", "Аналіз\nпараметрів", "▥"),
        ("equipment.png", "Пакет\nналаштувань", "✚"),
        ("equipment_search.png", "Пошук\nобладнання", "▽")
    ]

    card_images = []

    for index, (icon_file, heading, fallback_symbol) in enumerate(cards):

        row = index // 2
        column = index % 2

        card = ctk.CTkFrame(
            cards_frame,
            fg_color=CARD_COLOR,
            corner_radius=16,
            height=185
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=7,
            pady=9
        )

        card.grid_propagate(False)


        # Иконка карточки
        icon_path = os.path.join(ICONS_DIR, icon_file)

        if os.path.exists(icon_path):

            icon_original = Image.open(icon_path).convert("RGBA")

            # Сохраняем пропорции изображения
            icon_original.thumbnail(
                (120, 105),
                Image.Resampling.LANCZOS
            )

            icon_image = ctk.CTkImage(
                light_image=icon_original,
                dark_image=icon_original,
                size=icon_original.size
            )

            card_images.append(icon_image)

            icon_label = ctk.CTkLabel(
                card,
                text="",
                image=icon_image,
                fg_color="transparent",
                width=120,
                height=105
            )

        else:
            icon_label = ctk.CTkLabel(
                card,
                text=fallback_symbol,
                font=("Arial", 55),
                text_color=CYAN,
                fg_color="#004158",
                corner_radius=15,
                width=110,
                height=90
            )

        icon_label.pack(
            pady=(15, 8)
        )

        # Название карточки
        heading_label = ctk.CTkLabel(
            card,
            text=heading,
            font=("Arial", 14, "bold"),
            text_color=WHITE,
            justify="center",
            anchor="center",
            wraplength=125
        )

        heading_label.pack(
            fill="x",
            padx=5,
            pady=(0, 8)
        )

    cards_frame.card_images = card_images

    # ---------- НИЖНЯЯ НАВИГАЦИЯ ----------

    bottom_frame = ctk.CTkFrame(
        main_frame,
        width=304,
        height=65,
        corner_radius=20,
        fg_color="#003047",
        border_width=1,
        border_color=CYAN
    )

    bottom_frame.pack(
        side="bottom",
        fill="x",
        padx=8,
        pady=(0, 5)
    )

    bottom_frame.pack_propagate(False)

    navigation_items = [
        ("home.png", "Головна"),
        ("analysis.png", "Аналіз"),
        ("care.png", "Догляд"),
        ("history1.png", "Історія"),
        ("profile.png", "Профіль")
    ]

    navigation_images = []

    def navigate(page_name):

        if page_name == "Головна":
            from home import home_page
            home_page(window, aquarium)

        elif page_name == "Аналіз":
            from analysis import analysis_page
            analysis_page(window, aquarium=aquarium)

        elif page_name == "Догляд":
            from care import care_page
            care_page(window, aquarium)

        elif page_name == "Історія":
            from history import history_page
            history_page(window, aquarium)

        elif page_name == "Профіль":
            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):

        icon_path = os.path.join(ICONS_DIR, icon_file)

        icon_image = None

        if os.path.exists(icon_path):

            icon_original = Image.open(icon_path).convert("RGBA")

            icon_image = ctk.CTkImage(
                light_image=icon_original,
                dark_image=icon_original,
                size=(30, 30)
            )

            navigation_images.append(icon_image)

        nav_button = ctk.CTkButton(
            bottom_frame,
            text="",
            image=icon_image,
            width=48,
            height=52,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#00506B",
            border_width=0,
            command=lambda name=page_name: navigate(name)
        )

        nav_button.place(
            x=4 + i * 59,
            y=5
        )

    bottom_frame.navigation_images = navigation_images

    # ---------- ВОЗВРАТ НАЗАД ----------

    def go_back():
        from analysis import analysis_page
        analysis_page(window, aquarium=aquarium)
