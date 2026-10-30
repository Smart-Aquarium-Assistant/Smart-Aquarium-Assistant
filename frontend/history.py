import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image


BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CARD_DARK = "#002B40"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#B9D0DA"
GREEN = "#60D48C"
YELLOW = "#FFB800"


def history_page(window, aquarium=None, back_command=None):

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

    # ---------- ОСНОВНИЙ ФРЕЙМ ----------

    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        corner_radius=0,
        fg_color=BG_COLOR,
        border_width=0
    )
    main_frame.place(x=0, y=0)

    # ---------- ВЕРХНЯ ПАНЕЛЬ ----------

    def go_back():

        if back_command is not None:
            back_command()

        else:
            from home import home_page
            home_page(window, aquarium)

    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=32,
        height=34,
        corner_radius=8,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 23, "bold"),
        border_width=0,
        command=go_back
    )
    back_button.place(x=10, y=10)

    title_label = ctk.CTkLabel(
        main_frame,
        text="Історія вимірювань",
        width=210,
        height=30,
        font=("Arial", 16, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        anchor="center"
    )
    title_label.place(relx=0.52, y=26, anchor="center")

    # ---------- КАЛЕНДАР ----------

    calendar_image = None

    calendar_path = os.path.join(
        icons_folder, "kalend.png"
    )

    if os.path.exists(calendar_path):
        try:
            calendar_original = Image.open(
                calendar_path
            ).convert("RGBA")

            calendar_image = ctk.CTkImage(
                light_image=calendar_original,
                dark_image=calendar_original,
                size=(23, 23)
            )
        except Exception:
            pass

    calendar_button = ctk.CTkButton(
        main_frame,
        text="" if calendar_image else "▦",
        image=calendar_image,
        width=30,
        height=32,
        corner_radius=8,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=WHITE,
        font=("Arial", 22),
        border_width=0,
        command=lambda: print("Відкрити календар")
    )
    calendar_button.place(x=278, y=10)

    main_frame.calendar_image = calendar_image

    # ---------- ПЕРІОД ВИМІРЮВАНЬ ----------

    period_buttons = []

    def change_period(period):

        for button, button_period in period_buttons:

            if button_period == period:
                button.configure(
                    fg_color=CARD_COLOR,
                    text_color=WHITE,
                    border_color="#91B7C7"
                )
            else:
                button.configure(
                    fg_color=BG_COLOR,
                    text_color=WHITE,
                    border_color="#456779"
                )

    periods = [
        ("7 днів", 20),
        ("30 днів", 120),
        ("90 днів", 220)
    ]

    for period, x in periods:

        period_button = ctk.CTkButton(
            main_frame,
            text=period,
            width=80,
            height=33,
            corner_radius=13,
            fg_color=(
                CARD_COLOR
                if period == "7 днів"
                else BG_COLOR
            ),
            hover_color=CARD_COLOR,
            text_color=WHITE,
            border_width=1,
            border_color="#91B7C7",
            font=("Arial", 12, "bold"),
            command=lambda p=period: change_period(p)
        )
        period_button.place(x=x, y=59)

        period_buttons.append((period_button, period))

    # ---------- ЗАГОЛОВОК ГРАФІКА ----------

    graph_title = ctk.CTkLabel(
        main_frame,
        text="Графік параметрів",
        font=("Arial", 15, "bold"),
        text_color=GRAY,
        fg_color="transparent",
        anchor="w"
    )
    graph_title.place(x=18, y=99)

    # ---------- ЛЕГЕНДА ----------

    legend_frame = ctk.CTkFrame(
        main_frame,
        width=285,
        height=25,
        corner_radius=0,
        fg_color="transparent",
        border_width=0
    )
    legend_frame.place(x=18, y=126)

    ph_dot = ctk.CTkLabel(
        legend_frame,
        text="●",
        font=("Arial", 12, "bold"),
        text_color=CYAN,
        fg_color="transparent"
    )
    ph_dot.place(x=24, y=0)

    ph_legend = ctk.CTkLabel(
        legend_frame,
        text="pH",
        font=("Arial", 13, "bold"),
        text_color=GRAY,
        fg_color="transparent"
    )
    ph_legend.place(x=40, y=0)

    temperature_dot = ctk.CTkLabel(
        legend_frame,
        text="●",
        font=("Arial", 12, "bold"),
        text_color=GREEN,
        fg_color="transparent"
    )
    temperature_dot.place(x=113, y=0)

    temperature_legend = ctk.CTkLabel(
        legend_frame,
        text="Температура",
        font=("Arial", 13, "bold"),
        text_color=GRAY,
        fg_color="transparent"
    )
    temperature_legend.place(x=130, y=0)

    # ---------- ГРАФІК ----------

    graph = tk.Canvas(
        main_frame,
        width=320,
        height=174,
        bg=BG_COLOR,
        highlightthickness=0,
        bd=0
    )
    graph.place(
        relx=0.5,
        y=300,
        anchor="n"
    )

    graph_left = 40
    graph_right = 280
    graph_top = 5
    graph_bottom = 120

    # ---------- ГОРИЗОНТАЛЬНА СІТКА ----------

    ph_values = ["8.0", "7.5", "7.0", "6.5"]

    for i, value in enumerate(ph_values):

        y = graph_top + i * (
            (graph_bottom - graph_top) / 3
        )

        graph.create_line(
            graph_left,
            y,
            graph_right,
            y,
            fill="#12364A",
            width=1
        )

        graph.create_text(
            35,
            y,
            text=value,
            fill=GRAY,
            font=("Arial", 9),
            anchor="e"
        )

    # ---------- ВЕРТИКАЛЬНА СІТКА ----------

    for i in range(9):

        x = graph_left + i * (
            (graph_right - graph_left) / 8
        )

        graph.create_line(
            x,
            graph_top,
            x,
            graph_bottom,
            fill="#092638",
            width=1
        )

    # ---------- МЕЖІ ГРАФІКА ----------

    graph.create_line(
        graph_left,
        graph_top,
        graph_left,
        graph_bottom,
        fill="#24536B",
        width=1
    )

    graph.create_line(
        graph_left,
        graph_bottom,
        graph_right,
        graph_bottom,
        fill="#24536B",
        width=1
    )

    # ---------- ШКАЛА ТЕМПЕРАТУРИ ----------

    temperature_values = ["30", "28", "26", "24", "22"]

    for i, value in enumerate(temperature_values):

        y = graph_top + i * (
            (graph_bottom - graph_top) / 4
        )

        graph.create_text(
            285,
            y,
            text=value,
            fill="#C99A58",
            font=("Arial", 10),
            anchor="center"
        )

    # ---------- ДАТИ ----------

    dates = [
        ("6.09", 60),
        ("8.09", 125),
        ("10.09", 190),
        ("12.09", 255)
    ]

    for date, x in dates:

        graph.create_text(
            x,
            130,
            text=date,
            fill=GRAY,
            font=("Arial", 10),
            anchor="center"
        )

    # ---------- ДАНІ ВИМІРЮВАНЬ ----------

    ph_data = []
    temperature_data = []

    # ---------- ОСТАННІ ВИМІРЮВАННЯ ----------

    latest_title = ctk.CTkLabel(
        main_frame,
        text="Останні вимірювання",
        font=("Arial", 15, "bold"),
        text_color=WHITE,
        fg_color="transparent",
        anchor="w"
    )
    latest_title.place(x=18, y=324)

    # ---------- ІКОНКА ВИМІРЮВАННЯ ----------

    def draw_measurement_icon(parent, x, y):

        icon_canvas = tk.Canvas(
            parent,
            width=42,
            height=42,
            bg=CARD_COLOR,
            highlightthickness=0,
            bd=0
        )
        icon_canvas.place(x=x, y=y)

        icon_canvas.create_polygon(
            20, 2,
            7, 23,
            7, 29,
            11, 36,
            18, 40,
            25, 38,
            31, 32,
            32, 26,
            28, 20,
            fill="#00BFEA",
            outline=CYAN,
            width=2
        )

        icon_canvas.create_oval(
            12, 22, 27, 36,
            fill="#00A9D5",
            outline="#00D9F5",
            width=1
        )

        icon_canvas.create_oval(
            24, 21, 37, 34,
            outline=CYAN,
            width=3
        )

        icon_canvas.create_line(
            34, 32, 40, 39,
            fill=CYAN,
            width=3
        )

        return icon_canvas

    measurements = [
        ("12 вересня 2026", "pH 7.1", "26.3°C"),
        ("12 вересня 2026", "pH 7.1", "26.3°C"),
        ("12 вересня 2026", "pH 7.1", "26.3°C")
    ]

    card_y_positions = [350, 414, 478]

    def show_measurement(measurement):

        date_text, ph_text, temperature_text = measurement

        messagebox.showinfo(
            "Вимірювання",
            "Дата: " + date_text + "\n"
            + ph_text + "\n"
            + "Температура: " + temperature_text
        )

    for index, measurement in enumerate(measurements):

        date_text, ph_text, temperature_text = measurement
        y = card_y_positions[index]

        measurement_card = ctk.CTkFrame(
            main_frame,
            width=286,
            height=54,
            corner_radius=13,
            fg_color=CARD_COLOR,
            border_width=1,
            border_color=CYAN
        )
        measurement_card.place(x=17, y=y)

        draw_measurement_icon(
            measurement_card,
            8,
            6
        )

        date_label = ctk.CTkLabel(
            measurement_card,
            text=date_text,
            width=172,
            height=19,
            font=("Arial", 12, "bold"),
            text_color=WHITE,
            fg_color="transparent",
            anchor="w"
        )
        date_label.place(x=72, y=5)

        ph_label = ctk.CTkLabel(
            measurement_card,
            text=ph_text,
            width=75,
            height=19,
            font=("Arial", 12, "bold"),
            text_color=WHITE,
            fg_color="transparent",
            anchor="w"
        )
        ph_label.place(x=72, y=29)

        temperature_label = ctk.CTkLabel(
            measurement_card,
            text=temperature_text,
            width=74,
            height=19,
            font=("Arial", 12, "bold"),
            text_color=WHITE,
            fg_color="transparent",
            anchor="e"
        )
        temperature_label.place(x=174, y=29)

        arrow_button = ctk.CTkButton(
            measurement_card,
            text="➜",
            width=27,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#00445C",
            text_color=CYAN,
            font=("Arial", 22, "bold"),
            border_width=0,
            command=lambda m=measurement: show_measurement(m)
        )
        arrow_button.place(x=250, y=12)

    # ---------- НИЖНЯЯ ПАНЕЛЬ НАВІГАЦІЇ ----------

    bottom_frame = ctk.CTkFrame(
        main_frame,
        width=304,
        height=65,
        corner_radius=20,
        fg_color="#003047",
        border_width=1,
        border_color=CYAN
    )
    bottom_frame.place(x=8, y=575)
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

        if page_name == "Аналіз":
            from analysis import analysis_page

            analysis_page(
                window,
                back_command=go_back,
                aquarium=aquarium
            )

        elif page_name == "Головна":
            from home import home_page
            home_page(window, aquarium)

        elif page_name == "Догляд":
            from care import care_page
            care_page(window, aquarium)

        elif page_name == "Історія":
            history_page(window, aquarium)

        elif page_name == "Профіль":
            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):

        icon_path = os.path.join(
            icons_folder,
            icon_file
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
                    size=(30, 30)
                )

                navigation_images.append(icon_image)

            except Exception:
                pass

        nav_button = ctk.CTkButton(
            bottom_frame,
            text="",
            image=icon_image,
            width=48,
            height=52,
            corner_radius=12,
            fg_color=(
                "#00435A"
                if page_name == "Історія"
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
