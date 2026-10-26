
import customtkinter as ctk
import os
from PIL import Image


def care_page(window, aquarium=None):

    # ---------- ОЧИЩЕННЯ ПОТОЧНОЇ СТОРІНКИ ----------

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    CYAN = "#00EAF5"
    CARD_BLUE = "#003047"
    WHITE = "#FFFFFF"
    GREEN = "#60D48C"

    ROOT_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    ICONS_DIR = os.path.join(ROOT_DIR, "assets", "icons")

    navigation_images = []
    task_images = []

    # ---------- ГОЛОВНИЙ ФРЕЙМ ----------

    main_frame = ctk.CTkFrame(
        window,
        fg_color="#00121F",
        corner_radius=0
    )
    main_frame.pack(fill="both", expand=True)

    # ---------- ВЕРХНЯ ПАНЕЛЬ ----------

    header_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent",
        height=48
    )
    header_frame.pack(fill="x", padx=12, pady=(12, 0))
    header_frame.pack_propagate(False)

    def go_back():
        from home import home_page
        home_page(window, aquarium)

    back_button = ctk.CTkButton(
        header_frame,
        text="←",
        width=30,
        height=32,
        font=("Arial", 27, "bold"),
        text_color=CYAN,
        fg_color="transparent",
        hover_color=CARD_BLUE,
        command=go_back
    )
    back_button.place(x=0, y=0)

    title_label = ctk.CTkLabel(
        header_frame,
        text="Догляд",
        font=("Arial", 18, "bold"),
        text_color=WHITE
    )
    title_label.place(relx=0.5, y=15, anchor="center")

    # ---------- ІКОНКА СПОВІЩЕНЬ ----------

    def open_reminders():
        from reminders import reminders_page
        reminders_page(window, aquarium)

    bell_path = os.path.join(ICONS_DIR, "bell.png")

    if os.path.exists(bell_path):

        bell_original = Image.open(
            bell_path
        ).convert("RGBA")

        bell_image = ctk.CTkImage(
            light_image=bell_original,
            dark_image=bell_original,
            size=(24, 24)
        )

        task_images.append(bell_image)

        bell_button = ctk.CTkButton(
            header_frame,
            text="",
            image=bell_image,
            width=30,
            height=32,
            fg_color="transparent",
            hover_color=CARD_BLUE,
            command=open_reminders
        )

    else:

        bell_button = ctk.CTkButton(
            header_frame,
            text="♟",
            width=30,
            height=32,
            font=("Arial", 22),
            text_color=CYAN,
            fg_color="transparent",
            hover_color=CARD_BLUE,
            command=open_reminders
        )

    bell_button.place(x=266, y=0)

    # ---------- КАЛЕНДАР ----------

    calendar_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent",
        height=65
    )
    calendar_frame.pack(fill="x", padx=17, pady=(0, 0))
    calendar_frame.pack_propagate(False)

    week_days = [
        ("Пн", "6"),
        ("Вт", "7"),
        ("Ср", "8"),
        ("Чт", "9"),
        ("Пт", "10"),
        ("Сб", "11"),
        ("Нд", "12")
    ]

    selected_day = [0]
    day_buttons = []

    def select_day(day_index):

        selected_day[0] = day_index

        for i, button in enumerate(day_buttons):

            if i == selected_day[0]:
                button.configure(
                    fg_color="#00415C",
                    border_color=CYAN
                )
            else:
                button.configure(
                    fg_color=CARD_BLUE,
                    border_color="#A8C4D0"
                )

    for i, (day_name, day_number) in enumerate(week_days):

        day_button = ctk.CTkButton(
            calendar_frame,
            text=day_name + "\n\n" + day_number,
            width=42,
            height=65,
            corner_radius=14,
            font=("Arial", 13, "bold"),
            text_color=WHITE,
            fg_color="#00415C" if i == 0 else CARD_BLUE,
            hover_color="#00506B",
            border_width=1,
            border_color=CYAN if i == 0 else "#A8C4D0",
            command=lambda index=i: select_day(index)
        )

        day_button.place(x=i * 45, y=0)
        day_buttons.append(day_button)

    # ---------- ОБЛАСТЬ ЗАВДАНЬ ----------

    content_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    content_frame.pack(
        fill="both",
        expand=True,
        padx=17,
        pady=(10, 0)
    )

    # ---------- ЗАГОЛОВОК СЬОГОДНІ ----------

    today_label = ctk.CTkLabel(
        content_frame,
        text="Сьогодні",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    )
    today_label.place(x=5, y=0)

    # ---------- ЗАВАНТАЖЕННЯ ІКОНОК ----------

    def load_icon(file_names, size=(38, 38)):

        for file_name in file_names:

            icon_path = os.path.join(
                ICONS_DIR,
                file_name
            )

            if os.path.exists(icon_path):

                original_image = Image.open(
                    icon_path
                ).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=original_image,
                    dark_image=original_image,
                    size=size
                )

                task_images.append(icon_image)

                return icon_image

        return None

    water_icon = load_icon(
        ["water.png", "drop.png", "water_drop.png"],
        (38, 38)
    )

    cleaning_icon = load_icon(
        ["cleaning.png", "calendar.png", "clean.png"],
        (38, 38)
    )

    filter_icon = load_icon(
        ["filter.png", "calendar_clock.png", "calendar.png"],
        (38, 38)
    )

    feeding_icon = load_icon(
        ["fish.png", "feeding.png", "food.png"],
        (42, 38)
    )

    # ---------- СТВОРЕННЯ КАРТКИ ЗАВДАННЯ ----------

    def create_task_card(
        y,
        title,
        status,
        icon,
        icon_fallback,
        completed=False
    ):

        card = ctk.CTkFrame(
            content_frame,
            width=302,
            height=76,
            corner_radius=15,
            fg_color=CARD_BLUE,
            border_width=1,
            border_color=CYAN
        )
        card.place(x=0, y=y)

        # ІКОНКА ЗАВДАННЯ

        if icon:

            icon_label = ctk.CTkLabel(
                card,
                text="",
                image=icon,
                width=45,
                height=42,
                fg_color="transparent"
            )

        else:

            icon_label = ctk.CTkLabel(
                card,
                text=icon_fallback,
                width=45,
                height=42,
                font=("Arial", 29),
                text_color=CYAN,
                fg_color="transparent"
            )

        # ВИПРАВЛЕНО: width і height задаються вище,
        # у place залишаються тільки координати.

        icon_label.place(
            x=17,
            y=17
        )

        # НАЗВА ЗАВДАННЯ

        task_title = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16),
            text_color=WHITE,
            anchor="w"
        )
        task_title.place(x=72, y=19)

        # СТАТУС ЗАВДАННЯ

        status_label = ctk.CTkLabel(
            card,
            text=status,
            font=("Arial", 13, "bold" if completed else "normal"),
            text_color=GREEN if completed else WHITE,
            anchor="w"
        )
        status_label.place(x=72, y=45)

        task_state = [completed]

        if completed:
            check_text = "✓"
            check_color = "#35B975"
        else:
            check_text = "○"
            check_color = "transparent"

        def toggle_task():

            task_state[0] = not task_state[0]

            if task_state[0]:

                check_button.configure(
                    text="✓",
                    fg_color="#35B975",
                    text_color=WHITE
                )

                status_label.configure(
                    text="Виконано",
                    text_color=GREEN,
                    font=("Arial", 13, "bold")
                )

            else:

                check_button.configure(
                    text="○",
                    fg_color="transparent",
                    text_color="#D7E9EF"
                )

                status_label.configure(
                    text="Не виконано",
                    text_color=WHITE,
                    font=("Arial", 13)
                )

        check_button = ctk.CTkButton(
            card,
            text=check_text,
            width=25,
            height=25,
            corner_radius=13,
            font=("Arial", 18, "bold"),
            text_color=WHITE if completed else "#D7E9EF",
            fg_color=check_color,
            hover_color="#008F91",
            border_width=0,
            command=toggle_task
        )
        check_button.place(x=266, y=25)

    # ---------- СЬОГОДНІ ----------

    create_task_card(
        30,
        "Підміна води",
        "Виконано",
        water_icon,
        "💧",
        True
    )

    create_task_card(
        118,
        "Очищення скла",
        "Виконано",
        cleaning_icon,
        "▣",
        True
    )

    # ---------- ЗАВТРА ----------

    tomorrow_label = ctk.CTkLabel(
        content_frame,
        text="Завтра",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    )
    tomorrow_label.place(x=0, y=204)

    create_task_card(
        234,
        "Перевірка фільтра",
        "Не виконано",
        filter_icon,
        "▣",
        False
    )

    create_task_card(
        322,
        "Годування",
        "Не виконано",
        feeding_icon,
        "🐟",
        False
    )

    # ---------- НАСТУПНІ ДНІ ----------

    upcoming_label = ctk.CTkLabel(
        content_frame,
        text="Наступні дні",
        font=("Arial", 17, "bold"),
        text_color=WHITE
    )
    upcoming_label.place(x=0, y=410)

    # ---------- НИЖНЯ ПАНЕЛЬ НАВІГАЦІЇ ----------

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

    def navigate(page_name):

        if page_name == "Аналіз":

            from analysis import analysis_page
            analysis_page(
                window,
                back_command=lambda: care_page(window, aquarium),
                aquarium=aquarium
            )

        elif page_name == "Головна":

            from home import home_page
            home_page(window, aquarium)

        elif page_name == "Догляд":

            care_page(window, aquarium)

        elif page_name == "Історія":

            from history import history_page
            history_page(window, aquarium)

        elif page_name == "Профіль":

            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):

        icon_path = os.path.join(
            ICONS_DIR,
            icon_file
        )

        icon_image = None

        if os.path.exists(icon_path):

            icon_original = Image.open(
                icon_path
            ).convert("RGBA")

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
                "#00435A"
                if page_name == "Догляд"
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
    bottom_frame.task_images = task_images
