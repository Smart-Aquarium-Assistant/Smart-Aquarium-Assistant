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
    gray = "#A8B8C0"

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

    # Повернення на головну сторінку
    def go_back():
        from home import home_page
        home_page(window, aquarium)

    # Стрілка назад
    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=35,
        height=35,
        corner_radius=8,
        fg_color="transparent",
        hover_color=card_color,
        text_color=cyan,
        font=("Arial", 24, "bold"),
        border_width=0,
        command=go_back
    )
    back_button.place(x=12, y=8)

    # Заголовок
    title = ctk.CTkLabel(
        main_frame,
        text="Сповіщення",
        font=("Arial", 19, "bold"),
        text_color=white
    )
    title.place(relx=0.5, y=25, anchor="center")

    # Підзаголовок
    subtitle = ctk.CTkLabel(
        main_frame,
        text="Ваші сповіщення",
        font=("Arial", 15, "bold"),
        text_color=white,
        anchor="w"
    )
    subtitle.place(x=18, y=73)

    # Картка порожніх сповіщень
    empty_card = ctk.CTkFrame(
        main_frame,
        width=284,
        height=220,
        fg_color=card_color,
        corner_radius=16,
        border_width=1,
        border_color="#06465A"
    )
    empty_card.place(x=18, y=125)

    # Іконка сповіщень
    bell_path = os.path.join(
        icons_folder,
        "bell.png"
    )

    bell_image = None

    if os.path.exists(bell_path):
        try:
            with Image.open(bell_path) as source:
                bell_photo = source.convert("RGBA")

            bell_image = ctk.CTkImage(
                light_image=bell_photo,
                dark_image=bell_photo,
                size=(42, 42)
            )
        except Exception as error:
            print(f"Помилка іконки дзвоника: {error}")

    if bell_image:
        icon_label = ctk.CTkLabel(
            empty_card,
            text="",
            image=bell_image,
            fg_color="transparent"
        )
        icon_label.place(
            relx=0.5,
            y=43,
            anchor="center"
        )
        empty_card.bell_image = bell_image
    else:
        icon_label = ctk.CTkLabel(
            empty_card,
            text="♧",
            font=("Arial", 42),
            text_color=cyan,
            fg_color="transparent"
        )
        icon_label.place(
            relx=0.5,
            y=43,
            anchor="center"
        )

    # Заголовок порожнього стану
    empty_title = ctk.CTkLabel(
        empty_card,
        text="Поки немає сповіщень",
        font=("Arial", 15, "bold"),
        text_color=white
    )
    empty_title.place(
        relx=0.5,
        y=99,
        anchor="center"
    )

    # Пояснення
    empty_message = ctk.CTkLabel(
        empty_card,
        text=(
            "Тут з'являтимуться повідомлення\n"
            "про стан води, догляд та інші\n"
            "важливі події у твоїх акваріумах."
        ),
        font=("Arial", 11),
        text_color=gray,
        justify="center"
    )
    empty_message.place(
        relx=0.5,
        y=153,
        anchor="center"
    )

    # Кнопка повернення
    back_to_aquariums = ctk.CTkButton(
        main_frame,
        text="На головну",
        width=220,
        height=40,
        fg_color=card_color,
        hover_color="#00506B",
        border_width=1,
        border_color=cyan,
        corner_radius=12,
        text_color=white,
        font=("Arial", 12, "bold"),
        command=go_back
    )
    back_to_aquariums.place(
        relx=0.5,
        y=390,
        anchor="center"
    )

    # Нижня навігація
    navigation_frame = ctk.CTkFrame(
        main_frame,
        width=304,
        height=65,
        corner_radius=20,
        fg_color=card_color,
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

        icon_path = os.path.join(
            icons_folder,
            icon_file
        )

        icon_image = None

        if os.path.exists(icon_path):
            try:
                with Image.open(icon_path) as source:
                    icon_photo = source.convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=icon_photo,
                    dark_image=icon_photo,
                    size=(30, 30)
                )

                navigation_images.append(icon_image)

            except Exception as error:
                print(
                    f"Помилка іконки {icon_file}: {error}"
                )

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

    navigation_frame.navigation_images = navigation_images
