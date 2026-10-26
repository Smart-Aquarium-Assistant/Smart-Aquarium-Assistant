import customtkinter as ctk
import os
from PIL import Image


def care_page(window, aquarium=None):

    # ---------- ОЧИЩЕННЯ СТОРІНКИ ----------

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    BG = "#00121F"
    CYAN = "#00EAF5"
    CARD = "#003047"
    WHITE = "#FFFFFF"
    GREEN = "#60D48C"
    GRAY = "#A8C4D0"

    ROOT_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    ICONS_DIR = os.path.join(ROOT_DIR, "assets", "icons")

    task_images = []
    navigation_images = []

    # ---------- ГОЛОВНИЙ ФРЕЙМ ----------

    main_frame = ctk.CTkFrame(
        window,
        fg_color=BG,
        corner_radius=0
    )
    main_frame.pack(fill="both", expand=True)

    # ---------- ВЕРХНЯ ПАНЕЛЬ ----------

    header = ctk.CTkFrame(
        main_frame,
        width=304,
        height=45,
        fg_color="transparent"
    )
    header.place(x=8, y=7)
    header.pack_propagate(False)

    def go_back():
        from home import home_page
        home_page(window, aquarium)

    ctk.CTkButton(
        header,
        text="←",
        width=30,
        height=32,
        font=("Arial", 27, "bold"),
        text_color=CYAN,
        fg_color="transparent",
        hover_color=CARD,
        command=go_back
    ).place(x=0, y=0)

    ctk.CTkLabel(
        header,
        text="Догляд",
        font=("Arial", 18, "bold"),
        text_color=WHITE
    ).place(relx=0.5, y=17, anchor="center")

    # ---------- СПОВІЩЕННЯ ----------

    def open_reminders():
        from reminders import reminders_page
        reminders_page(window, aquarium)

    bell_path = os.path.join(ICONS_DIR, "bell.png")

    if os.path.exists(bell_path):
        try:
            bell_original = Image.open(
                bell_path
            ).convert("RGBA")

            bell_image = ctk.CTkImage(
                light_image=bell_original,
                dark_image=bell_original,
                size=(23, 23)
            )
            task_images.append(bell_image)

            bell_button = ctk.CTkButton(
                header,
                text="",
                image=bell_image,
                width=30,
                height=32,
                fg_color="transparent",
                hover_color=CARD,
                command=open_reminders
            )

        except Exception:
            bell_button = ctk.CTkButton(
                header,
                text="♧",
                width=30,
                height=32,
                font=("Arial", 20),
                text_color=CYAN,
                fg_color="transparent",
                hover_color=CARD,
                command=open_reminders
            )
    else:
        bell_button = ctk.CTkButton(
            header,
            text="♧",
            width=30,
            height=32,
            font=("Arial", 20),
            text_color=CYAN,
            fg_color="transparent",
            hover_color=CARD,
            command=open_reminders
        )

    bell_button.place(x=264, y=0)

    # ---------- КАЛЕНДАР ----------

    calendar_frame = ctk.CTkFrame(
        main_frame,
        width=300,
        height=85,
        fg_color="transparent"
    )
    calendar_frame.place(x=10, y=70)

    week_days = [
        ("Пн", "6"),
        ("Вт", "7"),
        ("Ср", "8"),
        ("Чт", "9"),
        ("Пт", "10"),
        ("Сб", "11"),
        ("Нд", "12")
    ]

    day_buttons = []
    selected_day = [0]

    def select_day(index):
        selected_day[0] = index

        for i, button in enumerate(day_buttons):
            if i == index:
                button.configure(
                    fg_color="#00415C",
                    border_color=CYAN
                )
            else:
                button.configure(
                    fg_color=CARD,
                    border_color="#A8C4D0"
                )

    # Ширина кнопки — 39 px, расстояние между кнопками — 3 px.
    # Общая ширина календаря — 291 px, он расположен по центру.

    button_width = 39
    button_gap = 3
    total_width = len(week_days) * button_width + (
            len(week_days) - 1
    ) * button_gap

    start_x = (300 - total_width) // 2

    for i, (day, number) in enumerate(week_days):
        button = ctk.CTkButton(
            calendar_frame,
            text=day + "\n" + number,
            width=button_width,
            height=85,
            corner_radius=13,
            font=("Arial", 13),
            text_color=WHITE,
            fg_color="#00415C" if i == 0 else CARD,
            hover_color="#00506B",
            border_width=1,
            border_color=CYAN if i == 0 else "#A8C4D0",
            command=lambda index=i: select_day(index)
        )

        button.place(
            x=start_x + i * (button_width + button_gap),
            y=0
        )

        day_buttons.append(button)

    # ---------- ІКОНКИ ЗАВДАНЬ ----------

    def load_icon(file_names, size=(35, 35)):

        for file_name in file_names:
            path = os.path.join(ICONS_DIR, file_name)

            if os.path.exists(path):
                try:
                    original = Image.open(
                        path
                    ).convert("RGBA")

                    image = ctk.CTkImage(
                        light_image=original,
                        dark_image=original,
                        size=size
                    )

                    task_images.append(image)
                    return image

                except Exception:
                    pass

        return None

    water_icon = load_icon(
        ["water.png", "drop.png", "water_drop.png"]
    )

    cleaning_icon = load_icon(
        ["cleaning.png", "clean.png", "calendar.png"]
    )

    filter_icon = load_icon(
        ["filter.png", "calendar_clock.png", "calendar.png"]
    )

    feeding_icon = load_icon(
        ["fish.png", "feeding.png", "food.png"]
    )

    # ---------- ОБЛАСТЬ ЗАВДАНЬ ----------

    content = ctk.CTkFrame(
        main_frame,
        width=296,
        height=415,
        fg_color="transparent",
        corner_radius=0
    )
    content.place(x=12, y=160)

    # ---------- ЗАГОЛОВКИ СЕКЦІЙ ----------

    def section_title(text, y):

        ctk.CTkLabel(
            content,
            text=text,
            width=280,
            height=22,
            font=("Arial", 16, "bold"),
            text_color=WHITE,
            anchor="w"
        ).place(x=9, y=y)

    # ---------- КАРТКА ЗАВДАННЯ ----------

    def create_task_card(
        y,
        title,
        icon,
        fallback,
        completed=False
    ):

        card = ctk.CTkFrame(
            content,
            width=268,
            height=72,
            corner_radius=13,
            fg_color=CARD,
            border_width=1,
            border_color=CYAN
        )
        card.place(x=8, y=y)

        if icon:
            icon_label = ctk.CTkLabel(
                card,
                text="",
                image=icon,
                width=38,
                height=38,
                fg_color="transparent"
            )
        else:
            icon_label = ctk.CTkLabel(
                card,
                text=fallback,
                width=38,
                height=38,
                font=("Arial", 25),
                text_color=CYAN,
                fg_color="transparent"
            )

        icon_label.place(x=10, y=16)

        ctk.CTkLabel(
            card,
            text=title,
            width=166,
            height=23,
            font=("Arial", 14),
            text_color=WHITE,
            anchor="w"
        ).place(x=49, y=13)

        status_label = ctk.CTkLabel(
            card,
            text="Виконано" if completed else "Не виконано",
            width=166,
            height=19,
            font=(
                "Arial",
                12,
                "bold" if completed else "normal"
            ),
            text_color=GREEN if completed else WHITE,
            anchor="w"
        )
        status_label.place(x=49, y=37)

        state = [completed]

        check_button = ctk.CTkButton(
            card,
            text="✓" if completed else "○",
            width=23,
            height=23,
            corner_radius=12,
            font=("Arial", 15, "bold"),
            text_color=WHITE if completed else GRAY,
            fg_color="#35B878" if completed else "transparent",
            hover_color="#168653",
            border_width=0 if completed else 1,
            border_color=GRAY
        )
        check_button.place(x=235, y=24)

        def toggle_task():

            state[0] = not state[0]

            if state[0]:
                check_button.configure(
                    text="✓",
                    fg_color="#35B878",
                    text_color=WHITE,
                    border_width=0
                )

                status_label.configure(
                    text="Виконано",
                    text_color=GREEN,
                    font=("Arial", 12, "bold")
                )

            else:
                check_button.configure(
                    text="○",
                    fg_color="transparent",
                    text_color=GRAY,
                    border_width=1
                )

                status_label.configure(
                    text="Не виконано",
                    text_color=WHITE,
                    font=("Arial", 12)
                )

        check_button.configure(command=toggle_task)

    # ---------- РОЗТАШУВАННЯ ЗАВДАНЬ ----------

    section_title("Сьогодні", 0)

    create_task_card(
        25,
        "Підміна води",
        water_icon,
        "💧",
        True
    )

    create_task_card(
        104,
        "Очищення скла",
        cleaning_icon,
        "▣",
        True
    )

    section_title("Завтра", 183)

    create_task_card(
        208,
        "Перевірка фільтра",
        filter_icon,
        "▣",
        False
    )

    create_task_card(
        287,
        "Годування",
        feeding_icon,
        "🐟",
        False
    )

    section_title("Наступні дні", 366)

    # ---------- ПЛАНОВІ ЗАВДАННЯ ----------

    upcoming_card = ctk.CTkFrame(
        content,
        width=268,
        height=36,
        corner_radius=12,
        fg_color="#002638",
        border_width=1,
        border_color="#07516A"
    )
    upcoming_card.place(x=8, y=391)

    ctk.CTkLabel(
        upcoming_card,
        text="Планові завдання",
        width=246,
        height=30,
        font=("Arial", 12),
        text_color=GRAY,
        anchor="w"
    ).place(x=10, y=2)

    # ---------- НИЖНЯ ПАНЕЛЬ НАВІГАЦІЇ ----------

    navigation_frame = ctk.CTkFrame(
        main_frame,
        width=304,
        height=65,
        corner_radius=20,
        fg_color="#003047",
        border_width=1,
        border_color=CYAN
    )

    navigation_frame.place(
        x=8,
        y=581
    )

    navigation_frame.pack_propagate(False)

    navigation_items = [
        ("home.png", "Головна"),
        ("analysis.png", "Аналіз"),
        ("care.png", "Догляд"),
        ("history1.png", "Історія"),
        ("profile.png", "Профіль")
    ]

    def navigate(page_name):

        if page_name == "Головна":
            from home import home_page
            home_page(window, aquarium)

        elif page_name == "Аналіз":
            from analysis import analysis_page

            analysis_page(
                window,
                back_command=lambda: care_page(window, aquarium),
                aquarium=aquarium
            )

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
            try:
                original = Image.open(
                    icon_path
                ).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=original,
                    dark_image=original,
                    size=(30, 30)
                )

                navigation_images.append(icon_image)

            except Exception:
                pass

        nav_button = ctk.CTkButton(
            navigation_frame,
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

    navigation_frame.navigation_images = navigation_images
    navigation_frame.task_images = task_images
