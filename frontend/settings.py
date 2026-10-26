
import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"
RED = "#FF2020"

# Настройки, сохраняемые при переходах между экранами
CURRENT_THEME = "Темна"
CURRENT_LANGUAGE = "Українська"
CURRENT_UNITS = "°C"
NOTIFICATIONS_ENABLED = True


def settings_page(window, aquarium=None, back_command=None):

    global CURRENT_THEME
    global CURRENT_LANGUAGE
    global CURRENT_UNITS
    global NOTIFICATIONS_ENABLED

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    icons_folder = os.path.join(
        project_folder, "assets", "icons"
    )

    # ---------- ЦВЕТА ТЕМЫ ----------

    is_light = CURRENT_THEME == "Світла"

    bg = "#F4FAFE" if is_light else BG_COLOR
    card = "#D3EAF7" if is_light else CARD_COLOR
    text_color = "#003047" if is_light else WHITE
    secondary_color = "#526B78" if is_light else GRAY

    border_color = "#00BFD0" if is_light else CYAN
    hover_card = "#BBDFF0" if is_light else "#00445C"
    icon_bg = "#EAF6FC" if is_light else BG_COLOR

    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        corner_radius=0,
        fg_color=bg,
        border_width=0
    )
    main_frame.place(x=0, y=0)

    # ---------- ДОПОМІЖНІ ФУНКЦІЇ ----------

    def return_to_profile():

        if back_command:
            back_command()
        else:
            from profile import profile_page
            profile_page(window, aquarium)

    def show_dialog(title, height=220):

        dialog = ctk.CTkToplevel(window)
        dialog.title(title)
        dialog.geometry(f"280x{height}")
        dialog.resizable(False, False)
        dialog.configure(fg_color=bg)
        dialog.transient(window)
        dialog.grab_set()

        dialog.update_idletasks()

        x = window.winfo_rootx() + 20
        y = window.winfo_rooty() + (650 - height) // 2

        dialog.geometry(
            f"280x{height}+{x}+{y}"
        )

        return dialog

    def dialog_title(dialog, title):

        ctk.CTkLabel(
            dialog,
            text=title,
            font=("Arial", 17, "bold"),
            text_color=text_color,
            fg_color="transparent"
        ).pack(pady=(20, 12))

    def dialog_button(parent, title, command):

        return ctk.CTkButton(
            parent,
            text=title,
            height=36,
            corner_radius=10,
            fg_color=card,
            hover_color=hover_card,
            border_width=1,
            border_color=border_color,
            text_color=text_color,
            font=("Arial", 12),
            command=command
        )

    # ---------- ВЕРХНЯ ПАНЕЛЬ ----------

    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=35,
        height=35,
        corner_radius=10,
        fg_color="transparent",
        hover_color=card,
        text_color=border_color,
        font=("Arial", 29, "bold"),
        border_width=0,
        command=return_to_profile
    )
    back_button.place(x=12, y=7)

    title_label = ctk.CTkLabel(
        main_frame,
        text=(
            "Налаштування"
            if CURRENT_LANGUAGE == "Українська"
            else "Settings"
        ),
        font=("Arial", 19, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )
    title_label.place(
        relx=0.5,
        y=25,
        anchor="center"
    )

    # ---------- СПОВІЩЕННЯ ----------

    def open_notifications():

        dialog = show_dialog("Сповіщення", 230)

        dialog_title(dialog, "Сповіщення")

        status = ctk.CTkLabel(
            dialog,
            text=(
                "Увімкнені"
                if NOTIFICATIONS_ENABLED
                else "Вимкнені"
            ),
            font=("Arial", 13),
            text_color=secondary_color
        )
        status.pack(pady=(0, 12))

        def toggle_notifications():

            global NOTIFICATIONS_ENABLED

            NOTIFICATIONS_ENABLED = not NOTIFICATIONS_ENABLED

            status.configure(
                text=(
                    "Увімкнені"
                    if NOTIFICATIONS_ENABLED
                    else "Вимкнені"
                )
            )

            toggle_button.configure(
                text=(
                    "Вимкнути сповіщення"
                    if NOTIFICATIONS_ENABLED
                    else "Увімкнути сповіщення"
                )
            )

        toggle_button = dialog_button(
            dialog,
            (
                "Вимкнути сповіщення"
                if NOTIFICATIONS_ENABLED
                else "Увімкнути сповіщення"
            ),
            toggle_notifications
        )
        toggle_button.pack(
            padx=20,
            fill="x",
            pady=5
        )

        dialog_button(
            dialog,
            "Готово",
            dialog.destroy
        ).pack(
            padx=20,
            fill="x",
            pady=5
        )

    # ---------- ОДИНИЦІ ВИМІРЮВАННЯ ----------

    def open_units():

        dialog = show_dialog(
            "Одиниці вимірювання",
            285
        )

        dialog_title(
            dialog,
            "Одиниці вимірювання"
        )

        ctk.CTkLabel(
            dialog,
            text="Оберіть одиницю температури:",
            font=("Arial", 12),
            text_color=secondary_color
        ).pack(pady=(0, 12))

        def choose_unit(unit):

            global CURRENT_UNITS

            CURRENT_UNITS = unit
            dialog.destroy()

            settings_page(
                window,
                aquarium,
                back_command
            )

        for unit in ("°C", "°F"):

            button = dialog_button(
                dialog,
                (
                    f"✓  {unit}"
                    if CURRENT_UNITS == unit
                    else unit
                ),
                lambda value=unit: choose_unit(value)
            )

            button.pack(
                padx=25,
                fill="x",
                pady=5
            )

        dialog_button(
            dialog,
            "Назад",
            dialog.destroy
        ).pack(
            padx=25,
            fill="x",
            pady=(10, 5)
        )

    # ---------- ТЕМА ----------

    def change_theme():

        global CURRENT_THEME

        CURRENT_THEME = (
            "Світла"
            if CURRENT_THEME == "Темна"
            else "Темна"
        )

        settings_page(
            window,
            aquarium,
            back_command
        )

    # ---------- МОВА ----------

    def change_language():

        global CURRENT_LANGUAGE

        CURRENT_LANGUAGE = (
            "English"
            if CURRENT_LANGUAGE == "Українська"
            else "Українська"
        )

        settings_page(
            window,
            aquarium,
            back_command
        )

    # ---------- ДОПОМОГА ----------

    def open_support():

        dialog = show_dialog(
            "Допомога та підтримка",
            260
        )

        dialog_title(
            dialog,
            "Допомога та підтримка"
        )

        ctk.CTkLabel(
            dialog,
            text=(
                "Маєте запитання щодо роботи\n"
                "Smart Aquarium Assistant?\n\n"
                "Тут буде доступна інформація\n"
                "для допомоги користувачам."
            ),
            font=("Arial", 12),
            text_color=text_color,
            justify="center"
        ).pack(
            padx=12,
            pady=5
        )

        dialog_button(
            dialog,
            "Закрити",
            dialog.destroy
        ).pack(
            padx=25,
            fill="x",
            pady=12
        )

    # ---------- ПРО ДОДАТОК ----------

    def open_about():

        dialog = show_dialog(
            "Про додаток",
            255
        )

        dialog_title(
            dialog,
            "Smart Aquarium Assistant"
        )

        ctk.CTkLabel(
            dialog,
            text=(
                "AI-платформа для розумного\n"
                "керування акваріумом.\n\n"
                "Допомагає стежити за станом\n"
                "води, рибками та доглядом.\n\n"
                "Версія 1.0.0"
            ),
            font=("Arial", 12),
            text_color=text_color,
            justify="center"
        ).pack(
            padx=10,
            pady=5
        )

        dialog_button(
            dialog,
            "Закрити",
            dialog.destroy
        ).pack(
            padx=25,
            fill="x",
            pady=10
        )

    # ---------- ВИХІД З АКАУНТА ----------

    def logout():

        answer = messagebox.askyesno(
            "Вийти з акаунта",
            "Ви дійсно хочете вийти з акаунта?",
            parent=window
        )

        if not answer:
            return

        try:
            from welcome import welcome_page
            welcome_page(window)

        except Exception as error:
            messagebox.showinfo(
                "Вихід",
                "Підтверджено вихід з акаунта.\n"
                "Підключіть перехід до екрана входу.",
                parent=window
            )
            print(f"Помилка переходу: {error}")

    # ---------- ЗАВАНТАЖЕННЯ ІКОНОК ----------

    def load_icon(filename, size=(34, 34)):

        path = os.path.join(
            icons_folder,
            filename
        )

        if not os.path.exists(path):
            return None

        try:
            original = Image.open(path).convert("RGBA")

            return ctk.CTkImage(
                light_image=original,
                dark_image=original,
                size=size
            )

        except Exception as error:
            print(
                f"Помилка завантаження {filename}: {error}"
            )
            return None

    # ---------- КАРТКИ НАЛАШТУВАНЬ ----------

    menu_items = [
        (
            "bell.png",
            "♧",
            "Сповіщення",
            "",
            open_notifications
        ),
        (
            "units.png",
            "▤",
            "Одиниці вимірювання",
            "",
            open_units
        ),
        (
            "theme.png",
            "◕",
            "Тема",
            CURRENT_THEME,
            change_theme
        ),
        (
            "language.png",
            "◎",
            "Мова",
            CURRENT_LANGUAGE,
            change_language
        )
    ]

    def make_card(
        y,
        icon_file,
        fallback_icon,
        caption,
        value,
        command,
        height=59,
        font_size=15
    ):

        card_button = ctk.CTkButton(
            main_frame,
            text="",
            width=284,
            height=height,
            corner_radius=17,
            fg_color=card,
            hover_color=hover_card,
            border_width=1,
            border_color=border_color,
            command=command
        )

        # Карточка по центру окна 320 px
        card_button.place(
            x=18,
            y=y
        )

        # Рамка иконки
        icon_frame = ctk.CTkFrame(
            card_button,
            width=44,
            height=44,
            corner_radius=12,
            fg_color=icon_bg,
            border_width=2,
            border_color=border_color
        )

        icon_frame.place(
            x=14,
            rely=0.5,
            anchor="w"
        )

        icon_image = load_icon(
            icon_file,
            (31, 31)
        )

        if icon_image:

            icon_label = ctk.CTkLabel(
                icon_frame,
                text="",
                image=icon_image,
                fg_color="transparent"
            )

            icon_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

            icon_frame.icon_image = icon_image

        else:

            icon_label = ctk.CTkLabel(
                icon_frame,
                text=fallback_icon,
                font=("Arial", 27, "bold"),
                text_color=border_color,
                fg_color="transparent"
            )

            icon_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

        # Название пункта
        caption_label = ctk.CTkLabel(
            card_button,
            text=caption,
            font=("Arial", font_size),
            text_color=text_color,
            fg_color="transparent",
            anchor="w"
        )

        caption_label.place(
            x=70,
            rely=0.5,
            anchor="w"
        )

        # Значение темы или языка
        if value:

            value_label = ctk.CTkLabel(
                card_button,
                text=value,
                font=("Arial", 10),
                text_color=border_color,
                fg_color="transparent"
            )

            value_label.place(
                relx=1.0,
                x=-36,
                rely=0.5,
                anchor="e"
            )

        # Стрелка
        arrow_label = ctk.CTkLabel(
            card_button,
            text="➜",
            font=("Arial", 23, "bold"),
            text_color=border_color,
            fg_color="transparent",
            width=23
        )

        arrow_label.place(
            relx=1.0,
            x=-5,
            rely=0.5,
            anchor="e"
        )

        # Клик по содержимому карточки
        for widget in (
            icon_frame,
            icon_label,
            caption_label,
            arrow_label
        ):

            widget.bind(
                "<Button-1>",
                lambda event, action=command: action()
            )

        if value:

            value_label.bind(
                "<Button-1>",
                lambda event, action=command: action()
            )

    # Четыре основные карточки
    for y, item in zip(
        (90, 170, 250, 330),
        menu_items
    ):

        icon_file, fallback, caption, value, command = item

        make_card(
            y,
            icon_file,
            fallback,
            caption,
            value,
            command,
            height=59,
            font_size=(
                12
                if caption == "Одиниці вимірювання"
                else 15
            )
        )

    # ---------- ДОПОЛНИТЕЛЬНЫЕ ПУНКТЫ ----------

    make_card(
        430,
        "help.png",
        "?",
        "Допомога та підтримка",
        "",
        open_support,
        height=59,
        font_size=12
    )

    make_card(
        505,
        "info.png",
        "i",
        "Про додаток",
        "",
        open_about,
        height=59,
        font_size=13
    )

    # ---------- КНОПКА ВЫХОДА ----------

    logout_button = ctk.CTkButton(
        main_frame,
        text="Вийти з акаунта",
        width=264,
        height=44,
        corner_radius=25,
        fg_color="#FBE5E8" if is_light else "#35070D",
        hover_color="#F5CDD3" if is_light else "#570B14",
        border_width=1,
        border_color="#E53950" if is_light else RED,
        text_color="#D82038" if is_light else RED,
        font=("Arial", 15),
        command=logout
    )

    logout_button.place(
        x=28,
        y=578
    )

    # Сохраняем ссылки на элементы и изображения
    main_frame.settings_icons = menu_items
