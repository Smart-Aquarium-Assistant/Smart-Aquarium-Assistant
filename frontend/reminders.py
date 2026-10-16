import customtkinter as ctk
import os
from PIL import Image


def reminders_page(window, aquarium=None):

    # Очищення поточної сторінки
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    # Шляхи до ресурсів
    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    icons_folder = os.path.join(
        project_folder, "assets", "icons"
    )

    background = "#00121F"
    card_color = "#003047"
    cyan = "#00F8FB"
    white = "#FFFFFF"
    gray = "#A8C4D0"

    # Основний контейнер
    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        corner_radius=0,
        fg_color=background,
        border_width=0
    )
    main_frame.place(x=0, y=0)

    # Стрілка назад
    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=35,
        height=35,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#003047",
        text_color=cyan,
        font=("Arial", 24, "bold"),
        border_width=0,
        command=lambda: go_back()
    )
    back_button.place(x=12, y=10)

    # Повернення на головну сторінку
    def go_back():
        from home import home_page
        home_page(window, aquarium)

    # Заголовок
    title = ctk.CTkLabel(
        main_frame,
        text="Сповіщення",
        font=("Arial", 15, "bold"),
        text_color=white
    )
    title.place(x=104, y=20)

    # Дані сповіщень
    notifications = [
        {
            "category": "Системні",
            "icon": "water.png",
            "title": "Аналіз акваріума завершено",
            "message": "Все в нормі!",
            "time": "09:20",
            "color": "#42C984"
        },
        {
            "category": "Важливі",
            "icon": "care.png",
            "title": "Пора годувати риб",
            "message": "Годування в 18:00",
            "time": "09:20",
            "color": "#20C5C9"
        },
        {
            "category": "Важливі",
            "icon": "water.png",
            "title": "Підміна води",
            "message": "Через 5 днів",
            "time": "09:20",
            "color": "#42C984"
        },
        {
            "category": "Системні",
            "icon": None,
            "title": "Новий вид риб",
            "message": "Додано до каталогу",
            "time": "09:20",
            "color": "#00D8D8"
        }
    ]

    # Фільтри
    selected_filter = ctk.StringVar(value="Всі")

    filter_frame = ctk.CTkFrame(
        main_frame,
        width=270,
        height=35,
        fg_color="transparent",
        corner_radius=0
    )
    filter_frame.place(x=28, y=68)

    filter_buttons = {}

    def select_filter(value):
        selected_filter.set(value)

        for name, button in filter_buttons.items():
            button.configure(
                fg_color=(
                    "#00445C"
                    if name == value
                    else background
                )
            )

        show_notifications()

    for i, name in enumerate(
        ["Всі", "Важливі", "Системні"]
    ):
        button = ctk.CTkButton(
            filter_frame,
            text=name,
            width=72,
            height=33,
            corner_radius=12,
            fg_color=background,
            hover_color="#00445C",
            border_width=1,
            border_color=cyan,
            text_color=white,
            font=("Arial", 10, "bold"),
            command=lambda value=name: select_filter(value)
        )
        button.place(x=i * 86, y=0)
        filter_buttons[name] = button

    # Область сповіщень
    notifications_frame = ctk.CTkFrame(
        main_frame,
        width=300,
        height=440,
        fg_color="transparent",
        corner_radius=0
    )
    notifications_frame.place(x=10, y=126)

    # Зберігаємо зображення, щоб вони не зникали
    notification_images = []

    def show_notifications():

        for widget in notifications_frame.winfo_children():
            widget.destroy()

        notification_images.clear()

        if selected_filter.get() == "Всі":
            visible_notifications = notifications
        else:
            visible_notifications = [
                item for item in notifications
                if item["category"] == selected_filter.get()
            ]

        y = 10

        for item in visible_notifications:

            # Картка іконки
            icon_box = ctk.CTkFrame(
                notifications_frame,
                width=58,
                height=54,
                corner_radius=8,
                fg_color=item["color"],
                border_width=0
            )
            icon_box.place(x=8, y=y + 6)

            icon_file = item["icon"]
            icon_path = (
                os.path.join(icons_folder, icon_file)
                if icon_file else ""
            )

            if icon_path and os.path.exists(icon_path):
                photo = Image.open(icon_path).convert("RGBA")
                icon_image = ctk.CTkImage(
                    light_image=photo,
                    dark_image=photo,
                    size=(35, 35)
                )
                notification_images.append(icon_image)

                icon_label = ctk.CTkLabel(
                    icon_box,
                    text="",
                    image=icon_image,
                    fg_color="transparent"
                )
                icon_label.place(
                    relx=0.5,
                    rely=0.5,
                    anchor="center"
                )
            else:
                icon_label = ctk.CTkLabel(
                    icon_box,
                    text="🐟",
                    font=("Arial", 24),
                    fg_color="transparent"
                )
                icon_label.place(
                    relx=0.5,
                    rely=0.5,
                    anchor="center"
                )

            # Заголовок сповіщення
            notification_title = ctk.CTkLabel(
                notifications_frame,
                text=item["title"],
                font=("Arial", 11, "bold"),
                text_color=white,
                anchor="w",
                justify="left",
                wraplength=198
            )
            notification_title.place(x=76, y=y + 10)

            # Текст сповіщення
            message = ctk.CTkLabel(
                notifications_frame,
                text=item["message"],
                font=("Arial", 12, "bold"),
                text_color=cyan,
                anchor="w"
            )
            message.place(x=76, y=y + 42)

            # Час
            time_label = ctk.CTkLabel(
                notifications_frame,
                text=item["time"],
                font=("Arial", 11, "bold"),
                text_color=white,
                anchor="e"
            )
            time_label.place(x=242, y=y + 62)

            # Роздільна лінія
            divider = ctk.CTkFrame(
                notifications_frame,
                width=246,
                height=4,
                corner_radius=0,
                fg_color="#003047"
            )
            divider.place(x=8, y=y + 80)

            y += 110

        main_frame.notification_images = notification_images

        # Нижня навігація: тільки іконки
        navigation_frame = ctk.CTkFrame(
            main_frame,
            width=304,
            height=65,
            corner_radius=20,
            fg_color="#003047",
            border_width=1,
            border_color="#91B7C7"
        )
        navigation_frame.place(x=8, y=575)

        navigation_items = [
            ("home.png", "Головна"),
            ("analysis.png", "Аналіз"),
            ("care.png", "Догляд"),
            ("history.png", "Історія"),
            ("profile.png", "Профіль")
        ]

        navigation_images = []

        for i in range(len(navigation_items)):
            icon_file, page_name = navigation_items[i]
            icon_path = os.path.join(icons_folder, icon_file)

            icon_image = None

            if os.path.exists(icon_path):
                icon_photo = Image.open(icon_path).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=icon_photo,
                    dark_image=icon_photo,
                    size=(30, 30)
                )
                navigation_images.append(icon_image)

            nav_button = ctk.CTkButton(
                navigation_frame,
                text="",
                image=icon_image,
                width=48,
                height=52,
                corner_radius=12,
                fg_color=(
                    "#00435A" if i == 0 else "transparent"
                ),
                hover_color="#00506B",
                border_width=0,
                command=lambda name=page_name: print(name)
            )

            nav_button.place(
                x=4 + i * 59,
                y=5
            )

    # Показати сповіщення
    select_filter("Всі")
