import customtkinter as ctk
import os
from PIL import Image


def home_page(window, aquarium=None):

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    images_folder = os.path.join(project_folder, "assets", "images")
    icons_folder = os.path.join(project_folder, "assets", "icons")

    background_color = "#00121F"
    cyan_color = "#00F8FB"
    text_color = "#FFFFFF"
    green_color = "#60D48C"

    # Основна область
    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        corner_radius=0,
        fg_color=background_color,
        border_width=0
    )
    main_frame.place(x=0, y=0)

    # Заголовок
    title = ctk.CTkLabel(
        main_frame,
        text="Привіт,\nакваріумісте!",
        font=("Arial", 19, "bold"),
        text_color=cyan_color,
        justify="left",
        anchor="w",
        fg_color="transparent"
    )
    title.place(x=25, y=14)

    # Іконка сповіщень
    bell_path = os.path.join(icons_folder, "bell.png")

    def open_reminders():
        from reminders import reminders_page
        reminders_page(window, aquarium)

    if os.path.exists(bell_path):
        bell_photo = Image.open(bell_path).convert("RGBA")

        bell_image = ctk.CTkImage(
            light_image=bell_photo,
            dark_image=bell_photo,
            size=(27, 27)
        )

        bell_button = ctk.CTkButton(
            main_frame,
            text="",
            image=bell_image,
            width=38,
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#003047",
            border_width=0,
            command=open_reminders
        )
        bell_button.place(x=270, y=15)

        main_frame.bell_image = bell_image

    # Картка акваріума
    aquarium_frame = ctk.CTkFrame(
        main_frame,
        width=300,
        height=130,
        corner_radius=14,
        fg_color="#003047",
        border_width=1,
        border_color=cyan_color
    )
    aquarium_frame.place(x=10, y=75)

    if aquarium is not None:

        aquarium_name = ctk.CTkLabel(
            aquarium_frame,
            text=aquarium["name"],
            font=("Arial", 12, "bold"),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )
        aquarium_name.place(x=12, y=85)

        next_button = ctk.CTkButton(
            aquarium_frame,
            text="➜",
            width=34,
            height=34,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#00445C",
            text_color=cyan_color,
            font=("Arial", 24, "bold"),
            border_width=0,
            command=lambda: open_add_aquarium()
        )
        next_button.place(x=255, y=85)

    else:

        empty_label = ctk.CTkLabel(
            aquarium_frame,
            text="Акваріум ще не додано",
            font=("Arial", 13),
            text_color="#A8C4D0",
            fg_color="transparent"
        )
        empty_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

    # Повідомлення про параметри води
    status_frame = ctk.CTkFrame(
        main_frame,
        width=300,
        height=55,
        corner_radius=13,
        fg_color="#002B40",
        border_width=1,
        border_color=cyan_color
    )
    status_frame.place(x=10, y=220)

    status_label = ctk.CTkLabel(
        status_frame,
        text="Параметри води згодом",
        font=("Arial", 12),
        text_color=text_color,
        fg_color="transparent"
    )
    status_label.place(relx=0.5, rely=0.5, anchor="center")

    # Заголовок параметрів
    parameters_title = ctk.CTkLabel(
        main_frame,
        text="Параметри води",
        font=("Arial", 15, "bold"),
        text_color=text_color,
        fg_color="transparent",
        anchor="w"
    )
    parameters_title.place(x=20, y=281)

    # Картки параметрів
    parameters = [
        ("water.png", "pH"),
        ("temperature.png", "Температура"),
        ("water.png", "NO3"),
        ("nh3.png", "NH3")
    ]

    positions = [
        (10, 307),
        (170, 307),
        (10, 394),
        (170, 394)
    ]

    parameter_images = []

    for i in range(len(parameters)):
        icon_file, parameter_name = parameters[i]
        x, y = positions[i]

        parameter_frame = ctk.CTkFrame(
            main_frame,
            width=140,
            height=78,
            corner_radius=12,
            fg_color="#003047",
            border_width=1,
            border_color="#91B7C7"
        )
        parameter_frame.place(x=x, y=y)

        icon_path = os.path.join(icons_folder, icon_file)

        if os.path.exists(icon_path):
            photo = Image.open(icon_path).convert("RGBA")

            icon_image = ctk.CTkImage(
                light_image=photo,
                dark_image=photo,
                size=(34, 38)
            )
            parameter_images.append(icon_image)

            icon_label = ctk.CTkLabel(
                parameter_frame,
                text="",
                image=icon_image,
                fg_color="transparent"
            )
            icon_label.image = icon_image
            icon_label.place(x=8, y=20)

        else:
            fallback_text = "♨" if i == 1 else "●"

            icon_label = ctk.CTkLabel(
                parameter_frame,
                text=fallback_text,
                font=("Arial", 25, "bold"),
                text_color=cyan_color,
                fg_color="transparent"
            )
            icon_label.place(x=8, y=20)

        name_label = ctk.CTkLabel(
            parameter_frame,
            text=parameter_name,
            font=("Arial", 9),
            text_color=text_color,
            fg_color="transparent",
            anchor="w",
            width=83
        )
        name_label.place(x=48, y=13)

        state_label = ctk.CTkLabel(
            parameter_frame,
            text="Немає\nакваріума",
            font=("Arial", 9, "bold"),
            text_color=green_color,
            fg_color="transparent",
            anchor="w",
            justify="left",
            width=83
        )
        state_label.place(x=48, y=34)

    # Форма додавання акваріума
    def open_add_aquarium():

        for widget in window.winfo_children():
            widget.destroy()

        window.configure(fg_color=background_color)

        form_frame = ctk.CTkFrame(
            window,
            width=320,
            height=650,
            corner_radius=0,
            fg_color=background_color,
            border_width=0
        )
        form_frame.place(x=0, y=0)

        # Стрілка назад
        back_button = ctk.CTkButton(
            form_frame,
            text="←",
            width=35,
            height=35,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#003047",
            text_color=cyan_color,
            font=("Arial", 22, "bold"),
            border_width=0,
            command=lambda: home_page(window, aquarium)
        )
        back_button.place(x=14, y=15)

        form_title = ctk.CTkLabel(
            form_frame,
            text="Додати/Редагувати",
            font=("Arial", 16, "bold"),
            text_color=text_color,
            fg_color="transparent"
        )
        form_title.place(x=90, y=20)

        # Фото акваріума
        photo_box = ctk.CTkFrame(
            form_frame,
            width=110,
            height=110,
            corner_radius=0,
            fg_color="#34434A",
            border_width=0
        )
        photo_box.place(x=18, y=88)

        photo_label = ctk.CTkLabel(
            photo_box,
            text="📷",
            font=("Arial", 38),
            text_color="#A8B8C0",
            fg_color="transparent"
        )
        photo_label.place(relx=0.5, rely=0.5, anchor="center")

        photo_title = ctk.CTkLabel(
            form_frame,
            text="Додати фото\nакваріума",
            font=("Arial", 16, "bold"),
            text_color=text_color,
            justify="left",
            anchor="w",
            fg_color="transparent"
        )
        photo_title.place(x=138, y=98)

        upload_button = ctk.CTkButton(
            form_frame,
            text="Завантажити",
            width=135,
            height=42,
            corner_radius=13,
            fg_color="#00E8ED",
            hover_color="#00C7D0",
            text_color="#00121F",
            font=("Arial", 13, "bold"),
            border_width=0,
            command=lambda: print("Вибрати фото акваріума")
        )
        upload_button.place(x=138, y=155)

        # Назва акваріума
        name_label = ctk.CTkLabel(
            form_frame,
            text="Назва акваріума",
            font=("Arial", 15, "bold"),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )
        name_label.place(x=18, y=213)

        name_entry = ctk.CTkEntry(
            form_frame,
            width=284,
            height=40,
            corner_radius=13,
            fg_color="#003047",
            border_width=1,
            border_color=cyan_color,
            text_color=text_color,
            placeholder_text="Назва акваріума",
            placeholder_text_color="#A8C4D0",
            font=("Arial", 13)
        )
        name_entry.place(x=10, y=240)

        if aquarium is not None:
            name_entry.insert(0, aquarium["name"])
        else:
            name_entry.insert(0, "Мій Травник")

        # Тип акваріума
        type_label = ctk.CTkLabel(
            form_frame,
            text="Тип акваріума",
            font=("Arial", 15, "bold"),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )
        type_label.place(x=18, y=278)

        selected_type = ctk.StringVar(
            value=(
                aquarium["type"]
                if aquarium is not None
                else "Прісноводний"
            )
        )

        def select_type(value):
            selected_type.set(value)

            freshwater_button.configure(
                fg_color=(
                    "#003047"
                    if value == "Прісноводний"
                    else background_color
                )
            )

            marine_button.configure(
                fg_color=(
                    "#003047"
                    if value == "Морський"
                    else background_color
                )
            )

        freshwater_button = ctk.CTkButton(
            form_frame,
            text="Прісноводний",
            width=284,
            height=40,
            corner_radius=12,
            fg_color="#003047",
            hover_color="#00445C",
            border_width=1,
            border_color=cyan_color,
            text_color=text_color,
            font=("Arial", 13),
            anchor="w",
            command=lambda: select_type("Прісноводний")
        )
        freshwater_button.place(x=10, y=305)

        marine_button = ctk.CTkButton(
            form_frame,
            text="Морський",
            width=284,
            height=40,
            corner_radius=12,
            fg_color=background_color,
            hover_color="#003047",
            border_width=1,
            border_color=cyan_color,
            text_color=text_color,
            font=("Arial", 13),
            anchor="w",
            command=lambda: select_type("Морський")
        )
        marine_button.place(x=10, y=344)

        select_type(selected_type.get())

        # Об'єм води
        volume_label = ctk.CTkLabel(
            form_frame,
            text="Об’єм води (л)",
            font=("Arial", 15, "bold"),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )
        volume_label.place(x=18, y=397)

        volume_entry = ctk.CTkEntry(
            form_frame,
            width=284,
            height=38,
            corner_radius=12,
            fg_color="#003047",
            border_width=1,
            border_color=cyan_color,
            text_color=text_color,
            placeholder_text="Об'єм у літрах",
            placeholder_text_color="#A8C4D0",
            font=("Arial", 13)
        )
        volume_entry.place(x=10, y=423)

        if aquarium is not None:
            volume_entry.insert(0, str(aquarium["volume"]))

        # Мешканці
        residents_label = ctk.CTkLabel(
            form_frame,
            text="Мешканці",
            font=("Arial", 15, "bold"),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )
        residents_label.place(x=18, y=469)

        for x in [18, 93, 168, 243]:
            resident_box = ctk.CTkFrame(
                form_frame,
                width=45,
                height=45,
                corner_radius=0,
                fg_color="#34434A",
                border_width=0
            )
            resident_box.place(x=x, y=497)

            resident_icon = ctk.CTkLabel(
                resident_box,
                text="📷",
                font=("Arial", 21),
                text_color="#A8B8C0",
                fg_color="transparent"
            )
            resident_icon.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

        message = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Arial", 10),
            text_color="#FF8080",
            fg_color="transparent"
        )
        message.place(x=15, y=545)

        # Збереження акваріума
        def save_aquarium():
            new_name = name_entry.get().strip()
            volume = volume_entry.get().strip()

            if not new_name or not volume:
                message.configure(text="Заповніть усі поля")
                return

            if not volume.isdigit() or int(volume) <= 0:
                message.configure(text="Введіть правильний об'єм")
                return

            new_aquarium = {
                "name": new_name,
                "volume": int(volume),
                "type": selected_type.get()
            }

            home_page(window, new_aquarium)

        save_button = ctk.CTkButton(
            form_frame,
            text="Створити",
            width=270,
            height=45,
            corner_radius=20,
            fg_color="#30E5ED",
            hover_color="#00C9D5",
            text_color="#001B2E",
            font=("Arial", 15, "bold"),
            border_width=0,
            command=save_aquarium
        )
        save_button.place(x=25, y=580)

    # Кнопка додавання акваріума
    add_button = ctk.CTkButton(
        main_frame,
        text="Додати акваріум",
        width=300,
        height=50,
        corner_radius=13,
        fg_color="#003047",
        hover_color="#00445C",
        border_width=1,
        border_color=cyan_color,
        text_color=text_color,
        font=("Arial", 15, "bold"),
        anchor="center",
        command=open_add_aquarium
    )
    add_button.place(x=10, y=493)


    # Нижня навігація
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

    def navigate(page_name):
        if page_name == "Аналіз":
            from analysis import analysis_page
            analysis_page(
                window,
                back_command=lambda: home_page(window, aquarium),
                aquarium=aquarium
            )

        elif page_name == "Головна":
            home_page(window, aquarium)

        elif page_name == "Догляд":
            from aquarium import aquarium_page
            aquarium_page(window, aquarium)

        elif page_name == "Історія":
            from fish import fish_page
            fish_page(window, aquarium)

        elif page_name == "Профіль":
            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):
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
            command=lambda name=page_name: navigate(name)
        )

        nav_button.place(
            x=4 + i * 59,
            y=5
        )

    # Сохраняем ссылки на изображения
    main_frame.parameter_images = parameter_images
    main_frame.navigation_images = navigation_images


