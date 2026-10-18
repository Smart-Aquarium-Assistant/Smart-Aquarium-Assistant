
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageOps


BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CARD_DARK = "#002B40"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"

PROFILE_AVATAR_PATH = None


def profile_page(window, aquarium=None):

    global PROFILE_AVATAR_PATH

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x720")
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

    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=720,
        corner_radius=0,
        fg_color=BG_COLOR,
        border_width=0
    )
    main_frame.place(x=0, y=0)

    # ---------- ВЕРХНЯ ПАНЕЛЬ ----------

    def open_home():
        from home import home_page
        home_page(window, aquarium)

    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=36,
        height=36,
        corner_radius=10,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 28, "bold"),
        border_width=0,
        command=open_home
    )
    back_button.place(x=17, y=10)

    title_label = ctk.CTkLabel(
        main_frame,
        text="Профіль",
        font=("Arial", 19, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        bg_color=BG_COLOR
    )
    title_label.place(relx=0.5, y=28, anchor="center")

    # ---------- КАЛЕНДАР ----------

    calendar_image = None

    calendar_icon_path = os.path.join(
        icons_folder, "calendar.png"
    )

    if os.path.exists(calendar_icon_path):
        try:
            calendar_original = Image.open(
                calendar_icon_path
            ).convert("RGBA")

            calendar_image = ctk.CTkImage(
                light_image=calendar_original,
                dark_image=calendar_original,
                size=(25, 25)
            )
        except Exception:
            pass

    calendar_button = ctk.CTkButton(
        main_frame,
        text="" if calendar_image else "▦",
        image=calendar_image,
        width=35,
        height=35,
        corner_radius=9,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color="#D9F5FF",
        font=("Arial", 23),
        border_width=0,
        command=lambda: print("Календар")
    )
    calendar_button.place(x=275, y=10)
    main_frame.calendar_image = calendar_image

    # ---------- ПОШУК АВАТАРА ----------

    def find_default_avatar():

        possible_avatars = [
            os.path.join(images_folder, "avatar.png"),
            os.path.join(images_folder, "avatar.jpg"),
            os.path.join(images_folder, "profile.jpg"),
            os.path.join(images_folder, "profile.png")
        ]

        for path in possible_avatars:
            if os.path.exists(path):
                return path

        return None

    if (
        PROFILE_AVATAR_PATH is None
        or not os.path.exists(PROFILE_AVATAR_PATH)
    ):
        avatar_path = find_default_avatar()
    else:
        avatar_path = PROFILE_AVATAR_PATH

    # ---------- ОБРОБКА КРУГЛОГО АВАТАРА ----------

    AVATAR_SIZE = 100

    def load_avatar(path):

        try:
            with Image.open(path) as source:
                original = source.convert("RGB")

            original = ImageOps.fit(
                original,
                (AVATAR_SIZE, AVATAR_SIZE),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )

            scale = 4
            large_size = AVATAR_SIZE * scale

            mask = Image.new(
                "L",
                (large_size, large_size),
                0
            )

            draw = ImageDraw.Draw(mask)

            draw.ellipse(
                (0, 0, large_size - 1, large_size - 1),
                fill=255
            )

            mask = mask.resize(
                (AVATAR_SIZE, AVATAR_SIZE),
                Image.Resampling.LANCZOS
            )

            rounded_image = original.convert("RGBA")
            rounded_image.putalpha(mask)

            return ctk.CTkImage(
                light_image=rounded_image,
                dark_image=rounded_image,
                size=(AVATAR_SIZE, AVATAR_SIZE)
            )

        except Exception as error:
            print(f"Помилка завантаження аватара: {error}")
            return None

    # ---------- КРУГЛИЙ АВАТАР ----------

    avatar_frame = ctk.CTkFrame(
        main_frame,
        width=AVATAR_SIZE,
        height=AVATAR_SIZE,
        corner_radius=0,
        fg_color=BG_COLOR,
        border_width=0
    )
    avatar_frame.place(x=25, y=82)
    avatar_frame.pack_propagate(False)

    avatar_image = (
        load_avatar(avatar_path)
        if avatar_path
        else None
    )

    avatar_label = ctk.CTkLabel(
        avatar_frame,
        text="" if avatar_image else "☺",
        image=avatar_image,
        width=AVATAR_SIZE,
        height=AVATAR_SIZE,
        corner_radius=0,
        fg_color=BG_COLOR,
        bg_color=BG_COLOR,
        text_color=CYAN,
        font=("Arial", 55, "bold")
    )
    avatar_label.place(x=0, y=0, anchor="nw")

    main_frame.avatar_image = avatar_image

    # ---------- РЕДАГУВАННЯ АВАТАРА ----------

    avatar_button = ctk.CTkButton(
        main_frame,
        text=(
            "Редагувати аватар"
            if PROFILE_AVATAR_PATH
            and os.path.exists(PROFILE_AVATAR_PATH)
            else "Завантажити фото"
        ),
        width=130,
        height=27,
        corner_radius=10,
        fg_color=CARD_COLOR,
        hover_color="#00445C",
        border_width=1,
        border_color=CYAN,
        text_color=CYAN,
        font=("Arial", 10, "bold")
    )
    avatar_button.place(x=10, y=187)

    def choose_avatar():

        global PROFILE_AVATAR_PATH

        file_path = filedialog.askopenfilename(
            title="Виберіть фотографію профілю",
            filetypes=[
                (
                    "Зображення",
                    "*.png *.jpg *.jpeg *.webp *.bmp"
                ),
                ("Усі файли", "*.*")
            ]
        )

        if not file_path:
            return

        new_image = load_avatar(file_path)

        if new_image is None:
            messagebox.showerror(
                "Помилка",
                "Не вдалося відкрити фотографію."
            )
            return

        PROFILE_AVATAR_PATH = file_path

        avatar_label.configure(
            image=new_image,
            text=""
        )

        avatar_label.image = new_image
        main_frame.avatar_image = new_image

        avatar_button.configure(
            text="Редагувати аватар"
        )

    avatar_button.configure(command=choose_avatar)

    avatar_label.configure(cursor="hand2")
    avatar_label.bind(
        "<Button-1>",
        lambda event: choose_avatar()
    )

    avatar_frame.configure(cursor="hand2")
    avatar_frame.bind(
        "<Button-1>",
        lambda event: choose_avatar()
    )

    # ---------- ІМ'Я ТА РІВЕНЬ ----------

    name_label = ctk.CTkLabel(
        main_frame,
        text="Настя",
        font=("Arial", 22, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        bg_color=BG_COLOR,
        anchor="w"
    )
    name_label.place(x=140, y=105)

    level_label = ctk.CTkLabel(
        main_frame,
        text="Рівень 3",
        font=("Arial", 14, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        bg_color=BG_COLOR,
        anchor="w"
    )
    level_label.place(x=140, y=141)

    progress_bg = ctk.CTkFrame(
        main_frame,
        width=140,
        height=10,
        corner_radius=0,
        fg_color=CARD_COLOR,
        border_width=0
    )
    progress_bg.place(x=140, y=165)

    progress_fill = ctk.CTkFrame(
        progress_bg,
        width=91,
        height=10,
        corner_radius=0,
        fg_color=CYAN,
        border_width=0
    )
    progress_fill.place(x=0, y=0)

    progress_text = ctk.CTkLabel(
        main_frame,
        text="130/200",
        font=("Arial", 10, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        bg_color=BG_COLOR
    )
    progress_text.place(x=251, y=163)

    # ---------- СТАТИСТИКА ----------

    stats_frame = ctk.CTkFrame(
        main_frame,
        width=298,
        height=100,
        corner_radius=14,
        fg_color=CARD_DARK,
        border_width=1,
        border_color=CYAN
    )
    stats_frame.place(x=11, y=218)

    stats = [
        ("3", "Акваріумів"),
        ("12", "Рибок"),
        ("5", "Завдань")
    ]

    for i, (number, caption) in enumerate(stats):

        x = i * 99

        if i > 0:
            separator = ctk.CTkFrame(
                stats_frame,
                width=1,
                height=98,
                fg_color="#91B7C7",
                border_width=0
            )
            separator.place(x=x, y=0)

        number_label = ctk.CTkLabel(
            stats_frame,
            text=number,
            font=("Arial", 19, "bold"),
            text_color=WHITE,
            fg_color="transparent",
            bg_color=CARD_DARK
        )
        number_label.place(
            x=x + 49,
            y=38,
            anchor="center"
        )

        caption_label = ctk.CTkLabel(
            stats_frame,
            text=caption,
            font=("Arial", 12),
            text_color=WHITE,
            fg_color="transparent",
            bg_color=CARD_DARK
        )
        caption_label.place(
            x=x + 49,
            y=67,
            anchor="center"
        )

    # ---------- КНОПКИ ПРОФІЛЮ ----------

    menu_items = [
        ("aquarium.png", "Мої акваріуми", "aquariums"),
        ("favorite.png", "Улюблені рибки", "favorites"),
        ("settings.png", "Налаштування", "settings"),
        ("history.png", "Історія", "history")
    ]

    menu_images = []

    def open_menu(item):

        if item == "aquariums":
            open_home()

        elif item == "favorites":
            messagebox.showinfo(
                "Улюблені рибки",
                "Тут буде список улюблених рибок."
            )

        elif item == "settings":
            messagebox.showinfo(
                "Налаштування",
                "Сторінка налаштувань буде додана пізніше."
            )

        elif item == "history":
            from fish import fish_page
            fish_page(window, aquarium)

    menu_y_positions = [333, 408, 483, 558]

    for index, (icon_file, caption, action) in enumerate(menu_items):

        y = menu_y_positions[index]

        # Картка меню
        menu_button = ctk.CTkButton(
            main_frame,
            text="",
            width=296,
            height=69,
            corner_radius=14,
            fg_color=CARD_COLOR,
            hover_color="#00445C",
            border_width=1,
            border_color=CYAN,
            command=lambda name=action: open_menu(name)
        )
        menu_button.place(x=12, y=y)

        # Іконка всередині картки
        icon_path = os.path.join(
            icons_folder, icon_file
        )

        if os.path.exists(icon_path):
            try:
                icon_original = Image.open(
                    icon_path
                ).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=icon_original,
                    dark_image=icon_original,
                    size=(38, 38)
                )

                menu_images.append(icon_image)

                icon_label = ctk.CTkLabel(
                    menu_button,
                    text="",
                    image=icon_image,
                    fg_color="transparent",
                    bg_color=CARD_COLOR
                )
                icon_label.place(
                    x=18,
                    y=15
                )
                icon_label.image = icon_image

            except Exception:
                pass

        # Текст на фоне карточки, без чёрной подложки
        text_label = ctk.CTkLabel(
            menu_button,
            text=caption,
            font=("Arial", 15, "bold"),
            text_color=WHITE,
            fg_color="transparent",
            bg_color=CARD_COLOR,
            anchor="w",
            width=170
        )
        text_label.place(
            x=76,
            y=0,
            relheight=1
        )

        # Стрелка внутри карточки
        arrow_label = ctk.CTkLabel(
            menu_button,
            text="➜",
            font=("Arial", 27, "bold"),
            text_color=CYAN,
            fg_color="transparent",
            bg_color=CARD_COLOR
        )
        arrow_label.place(
            x=244,
            y=12
        )

    main_frame.menu_images = menu_images

    # ---------- НИЖНЯЯ НАВІГАЦІЯ ----------

    navigation_frame = ctk.CTkFrame(
        main_frame,
        width=296,
        height=64,
        corner_radius=20,
        fg_color=CARD_COLOR,
        border_width=1,
        border_color="#91B7C7"
    )
    navigation_frame.place(x=12, y=643)

    navigation_items = [
        ("home.png", "Головна"),
        ("analysis.png", "Аналіз"),
        ("care.png", "Догляд"),
        ("history.png", "Історія"),
        ("profile.png", "Профіль")
    ]

    navigation_images = []

    def navigate(page_name):

        if page_name == "Головна":
            open_home()

        elif page_name == "Аналіз":
            from analysis import analysis_page
            analysis_page(
                window,
                back_command=open_home,
                aquarium=aquarium
            )

        elif page_name == "Догляд":
            from aquarium import aquarium_page
            aquarium_page(window, aquarium)

        elif page_name == "Історія":
            from fish import fish_page
            fish_page(window, aquarium)

        elif page_name == "Профіль":
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):

        icon_path = os.path.join(
            icons_folder, icon_file
        )

        icon_image = None

        if os.path.exists(icon_path):
            try:
                icon_original = Image.open(
                    icon_path
                ).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=icon_original,
                    dark_image=icon_original,
                    size=(25, 25)
                )

                navigation_images.append(icon_image)

            except Exception:
                pass

        nav_button = ctk.CTkButton(
            navigation_frame,
            text="",
            image=icon_image,
            width=46,
            height=50,
            corner_radius=12,
            fg_color=(
                "#00435A"
                if page_name == "Профіль"
                else "transparent"
            ),
            hover_color="#00506B",
            border_width=0,
            command=lambda name=page_name: navigate(name)
        )
        nav_button.place(x=3 + i * 58, y=5)

    navigation_frame.navigation_images = navigation_images
