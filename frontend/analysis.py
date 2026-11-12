
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image


# Путь к папке проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")

BG_COLOR = "#00121F"
CARD_COLOR = "#003B55"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"


def analysis_page(window, back_command=None, aquarium=None):

    # Очищаем предыдущую страницу
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("320x650")
    window.configure(fg_color=BG_COLOR)
    window.resizable(False, False)

    selected_image = {"path": None}
    photo_reference = {"image": None}

    # Основной контейнер
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
        height=42,
        corner_radius=0
    )
    header.pack(fill="x", padx=12, pady=(8, 5))
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
        command=back_command if back_command else lambda: None
    )
    back_button.pack(side="left")

    title_label = ctk.CTkLabel(
        header,
        text="Аналіз акваріума",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    )
    title_label.place(
        relx=0.52,
        rely=0.5,
        anchor="center"
    )

    # ---------- ИКОНКА УВЕДОМЛЕНИЙ ----------

    bell_path = os.path.join(ICONS_DIR, "bell.png")

    def open_reminders():
        from reminders import reminders_page
        reminders_page(window, aquarium)

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

    # ---------- ОБЛАСТЬ ЗАГРУЗКИ ФОТО ----------

    upload_frame = ctk.CTkFrame(
        main_frame,
        fg_color=CARD_COLOR,
        border_color=CYAN,
        border_width=1,
        corner_radius=16,
        height=180
    )
    upload_frame.pack(
        fill="x",
        padx=17,
        pady=(0, 14)
    )
    upload_frame.pack_propagate(False)

    upload_title = ctk.CTkLabel(
        upload_frame,
        text="Завантажте фото або зробіть знімок",
        font=("Arial", 12, "bold"),
        text_color=WHITE
    )
    upload_title.pack(pady=(17, 5))

    photo_label = ctk.CTkLabel(
        upload_frame,
        text="＋\n\nНатисніть, щоб вибрати фото",
        font=("Arial", 14),
        text_color=GRAY,
        cursor="hand2"
    )
    photo_label.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0, 8)
    )

    # ---------- ВЫБОР ФОТОГРАФИИ ----------

    def choose_photo(event=None):

        path = filedialog.askopenfilename(
            title="Виберіть фото акваріума",
            filetypes=[
                ("Зображення", "*.png *.jpg *.jpeg *.webp"),
                ("Усі файли", "*.*")
            ]
        )

        if not path:
            return

        try:

            original = Image.open(path).convert("RGB")

            original.thumbnail((270, 120))

            image = ctk.CTkImage(
                light_image=original,
                dark_image=original,
                size=original.size
            )

            photo_reference["image"] = image
            selected_image["path"] = path

            photo_label.configure(
                image=image,
                text=""
            )

            upload_title.configure(
                text="Фото акваріума завантажено"
            )

        except Exception as error:

            messagebox.showerror(
                "Помилка",
                f"Не вдалося відкрити фото:\n{error}"
            )

    upload_frame.bind("<Button-1>", choose_photo)
    upload_title.bind("<Button-1>", choose_photo)
    photo_label.bind("<Button-1>", choose_photo)

    # ---------- КНОПКА АНАЛИЗА ----------

    def analyze_photo():

        if not selected_image["path"]:
            messagebox.showwarning(
                "Аналіз акваріума",
                "Спочатку завантажте фото акваріума."
            )

            return

        from ai_chat import ai_chat_page

        ai_chat_page(
            window,
            aquarium=aquarium,
            image_path=selected_image["path"]
        )

        # Открываем AI-чат и передаём фотографию
        from ai_chat import ai_chat_page

        ai_chat_page(
            window,
            aquarium=aquarium,
            image_path=selected_image["path"]
        )

    analyze_button = ctk.CTkButton(
        main_frame,
        text="Проаналізувати",
        height=42,
        corner_radius=14,
        fg_color=CYAN,
        hover_color="#00D5DE",
        text_color=BG_COLOR,
        font=("Arial", 17, "bold"),
        command=analyze_photo
    )

    analyze_button.pack(
        fill="x",
        padx=18,
        pady=(0, 16)
    )

    # ---------- AI-АССИСТЕНТ ----------

    def open_ai_capabilities():

        from ai_capabilities import ai_capabilities_page

        ai_capabilities_page(
            window,
            aquarium
        )

    assistant_frame = ctk.CTkFrame(
        main_frame,
        fg_color=CARD_COLOR,
        border_color=CYAN,
        border_width=1,
        corner_radius=15,
        height=60,
        cursor="hand2"
    )

    assistant_frame.pack(
        fill="x",
        padx=17,
        pady=(0, 17)
    )

    assistant_frame.pack_propagate(False)

    assistant_text = ctk.CTkLabel(
        assistant_frame,
        text="АІ Можливості",
        font=("Arial", 14, "bold"),
        text_color=WHITE,
        anchor="center",
        cursor="hand2"
    )

    assistant_text.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    assistant_frame.bind(
        "<Button-1>",
        lambda event: open_ai_capabilities()
    )

    assistant_text.bind(
        "<Button-1>",
        lambda event: open_ai_capabilities()
    )

    # ---------- ИНФОРМАЦИОННЫЕ КАРТОЧКИ ----------

    cards_frame = ctk.CTkFrame(
        main_frame,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    cards_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 8)
    )

    cards_frame.grid_columnconfigure(
        (0, 1),
        weight=1,
        uniform="cards"
    )

    cards_frame.grid_rowconfigure(
        (0, 1),
        weight=1,
        uniform="cards"
    )

    # Названия PNG-файлов для карточек
    cards = [
        ("plants.png", "Рослини", "Стан здоров’я"),
        ("fish.png", "Риби", "Активність"),
        ("water.png", "Чистота води", "Прозорість"),
        ("algae.png", "Водорості", "Ризик появи")
    ]

    card_images = []

    for index, (icon_file, heading, subtitle) in enumerate(cards):

        row = index // 2
        column = index % 2

        card = ctk.CTkFrame(
            cards_frame,
            fg_color=CARD_COLOR,
            border_color=CYAN,
            border_width=1,
            corner_radius=15
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=4,
            pady=4
        )

        # Размещаем иконку PNG
        icon_path = os.path.join(ICONS_DIR, icon_file)

        if os.path.exists(icon_path):

            icon_original = Image.open(icon_path).convert("RGBA")

            icon_image = ctk.CTkImage(
                light_image=icon_original,
                dark_image=icon_original,
                size=(35, 35)
            )

            card_images.append(icon_image)

            icon_label = ctk.CTkLabel(
                card,
                text="",
                image=icon_image,
                fg_color="transparent",
                width=35,
                height=35
            )

            icon_label.pack(
                side="left",
                padx=(9, 7),
                pady=8
            )

        # Текст карточки
        text_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
            corner_radius=0
        )

        text_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5),
            pady=5
        )

        text_label = ctk.CTkLabel(
            text_frame,
            text=f"{heading}\n{subtitle}",
            font=("Arial", 11),
            text_color=WHITE,
            justify="left",
            anchor="w",
            wraplength=85
        )

        text_label.pack(
            fill="both",
            expand=True
        )

    # Сохраняем ссылки на изображения
    cards_frame.card_images = card_images

    # ---------- НИЖНЯЯ ПАНЕЛЬ НАВИГАЦИИ ----------

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

    # ---------- ПЕРЕХОДЫ МЕЖДУ СТРАНИЦАМИ ----------

    def navigate(page_name):

        if page_name == "Аналіз":
            return

        elif page_name == "Головна":

            if back_command:
                back_command()

            else:
                from home import home_page
                home_page(window, aquarium)

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
            fg_color=(
                "#00435A" if page_name == "Аналіз"
                else "transparent"
            ),
            hover_color="#00506B",
            border_width=0,
            command=lambda name=page_name: navigate(name)
        )

        nav_button.place(
            x=4 + i * 59,
            y=5
        )

    bottom_frame.navigation_images = navigation_images
