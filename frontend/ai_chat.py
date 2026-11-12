
import os
import customtkinter as ctk

from tkinter import filedialog
from PIL import Image

from ai_mock_data import get_ai_response


BG_COLOR = "#00121F"
CARD_COLOR = "#003047"
CARD_DARK = "#002B40"
CYAN = "#00F8FB"
WHITE = "#FFFFFF"
GRAY = "#A8B8C0"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_DIR = os.path.join(BASE_DIR, "assets", "icons")


def ai_chat_page(window, aquarium=None, image_path=None):

    # ---------- ОЧИЩЕНИЕ ПРЕДЫДУЩЕЙ СТРАНИЦЫ ----------

    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("320x650")
    window.configure(fg_color=BG_COLOR)
    window.resizable(False, False)

    selected_image = {"path": None}
    chat_images = []

    # Проверка, открыта ли ещё страница чата
    page_state = {"active": True}

    # ---------- ОСНОВНОЙ КОНТЕЙНЕР ----------

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
        height=52
    )

    header.pack(fill="x", padx=12, pady=(5, 5))
    header.pack_propagate(False)

    def go_back():

        page_state["active"] = False

        from analysis import analysis_page
        analysis_page(window, aquarium=aquarium)

    back_button = ctk.CTkButton(
        header,
        text="←",
        width=30,
        height=34,
        fg_color="transparent",
        hover_color=CARD_COLOR,
        text_color=CYAN,
        font=("Arial", 27, "bold"),
        command=go_back
    )

    back_button.pack(side="left")

    title_label = ctk.CTkLabel(
        header,
        text="AI Асистент",
        font=("Arial", 18, "bold"),
        text_color=WHITE
    )

    title_label.place(
        relx=0.52,
        rely=0.5,
        anchor="center"
    )

    # ---------- КОЛОКОЛЬЧИК ----------

    def open_reminders():

        page_state["active"] = False

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

    # ---------- ОБЛАСТЬ ПЕРЕПИСКИ ----------

    chat_frame = ctk.CTkScrollableFrame(
        main_frame,
        fg_color=BG_COLOR,
        corner_radius=0,
        scrollbar_button_color=CARD_COLOR,
        scrollbar_button_hover_color=CYAN
    )

    chat_frame.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=(0, 4)
    )

    # ---------- ПРОКРУТКА ВНИЗ ----------

    def scroll_to_bottom():

        if not page_state["active"]:
            return

        if not chat_frame.winfo_exists():
            return

        chat_frame.update_idletasks()
        chat_frame._parent_canvas.yview_moveto(1.0)

    # ---------- ДОБАВЛЕНИЕ СООБЩЕНИЯ ----------

    def add_message(message, sender, photo=None):

        if not page_state["active"]:
            return

        if not chat_frame.winfo_exists():
            return

        message_row = ctk.CTkFrame(
            chat_frame,
            fg_color="transparent"
        )

        message_row.pack(
            fill="x",
            padx=3,
            pady=6
        )

        if sender == "assistant":

            avatar = ctk.CTkLabel(
                message_row,
                text="AI",
                font=("Arial", 12, "bold"),
                text_color=BG_COLOR,
                fg_color=CYAN,
                width=36,
                height=36,
                corner_radius=18
            )

            avatar.pack(
                side="left",
                anchor="n",
                padx=(0, 6)
            )

            bubble = ctk.CTkFrame(
                message_row,
                fg_color=CARD_COLOR,
                border_color=CYAN,
                border_width=1,
                corner_radius=15
            )

            bubble.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(0, 5)
            )

            text_color = WHITE

        else:

            bubble = ctk.CTkFrame(
                message_row,
                fg_color=CYAN,
                corner_radius=15
            )

            bubble.pack(
                side="right",
                padx=(35, 2)
            )

            text_color = BG_COLOR

        # ---------- ФОТО В СООБЩЕНИИ ----------

        if photo:

            original = Image.open(photo).convert("RGB")
            original.thumbnail((175, 130))

            photo_image = ctk.CTkImage(
                light_image=original,
                dark_image=original,
                size=original.size
            )

            chat_images.append(photo_image)

            photo_label = ctk.CTkLabel(
                bubble,
                text="",
                image=photo_image
            )

            photo_label.pack(
                padx=8,
                pady=(8, 3)
            )

        # ---------- ТЕКСТ СООБЩЕНИЯ ----------

        if message:

            text_label = ctk.CTkLabel(
                bubble,
                text=message,
                font=("Arial", 12),
                text_color=text_color,
                justify="left",
                anchor="w",
                wraplength=195
            )

            text_label.pack(
                padx=10,
                pady=9
            )

        scroll_to_bottom()

    # ---------- ОТПРАВКА СООБЩЕНИЯ ----------

    busy = {"value": False}

    def start_request(message, photo=None):

        if not page_state["active"]:
            return

        if busy["value"]:
            return

        if not message and not photo:
            return

        # Показываем сообщение пользователя

        add_message(
            message,
            "user",
            photo
        )

        busy["value"] = True

        send_button.configure(
            state="disabled"
        )

        attach_button.configure(
            state="disabled"
        )

        entry.configure(
            state="disabled"
        )

        status_label.configure(
            text="AI аналізує...",
            text_color=CYAN
        )


        def show_answer():


            if not page_state["active"]:
                return

            if not chat_frame.winfo_exists():
                return

            # Получаем ответ AI

            answer = get_ai_response(
                message,
                photo
            )

            # Повторная проверка перед добавлением

            if not page_state["active"]:
                return

            if not chat_frame.winfo_exists():
                return

            add_message(
                answer,
                "assistant"
            )

            busy["value"] = False

            send_button.configure(
                state="normal"
            )

            attach_button.configure(
                state="normal"
            )

            entry.configure(
                state="normal"
            )

            status_label.configure(
                text="AI готовий до спілкування",
                text_color=GRAY
            )

            entry.focus()

        window.after(1200, show_answer)


    def attach_photo():

        if not page_state["active"]:
            return

        if busy["value"]:
            return

        path = filedialog.askopenfilename(
            title="Виберіть фото",
            filetypes=[
                ("Зображення", "*.png *.jpg *.jpeg *.webp")
            ]
        )

        if path:

            Image.open(path).verify()

            selected_image["path"] = path

            status_label.configure(
                text="Фото прикріплено: "
                + os.path.basename(path),
                text_color=CYAN
            )


    input_frame = ctk.CTkFrame(
        main_frame,
        fg_color=CARD_COLOR,
        corner_radius=14,
        height=53,
        border_width=1,
        border_color=CYAN
    )

    input_frame.pack(
        side="bottom",
        fill="x",
        padx=9,
        pady=(2, 4)
    )

    input_frame.pack_propagate(False)

    attach_button = ctk.CTkButton(
        input_frame,
        text="＋",
        width=34,
        height=42,
        fg_color="transparent",
        hover_color=CARD_DARK,
        text_color=CYAN,
        font=("Arial", 24, "bold"),
        command=attach_photo
    )

    attach_button.pack(
        side="left",
        padx=(3, 0)
    )

    entry = ctk.CTkEntry(
        input_frame,
        placeholder_text="Написати повідомлення...",
        font=("Arial", 12),
        fg_color=CARD_DARK,
        text_color=WHITE,
        border_width=0,
        corner_radius=8,
        height=39
    )

    entry.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3,
        pady=5
    )


    def send_message():

        if not page_state["active"]:
            return

        if busy["value"]:
            return

        message = entry.get().strip()
        photo = selected_image["path"]

        if not message and not photo:
            return

        entry.delete(0, "end")

        selected_image["path"] = None

        if photo and not message:

            message = (
                "Проаналізуй, будь ласка, "
                "це фото мого акваріума."
            )

        start_request(
            message,
            photo
        )

    send_button = ctk.CTkButton(
        input_frame,
        text="➤",
        width=38,
        height=42,
        fg_color="transparent",
        hover_color=CARD_DARK,
        text_color=CYAN,
        font=("Arial", 23, "bold"),
        command=send_message
    )

    send_button.pack(
        side="right",
        padx=(0, 3)
    )

    entry.bind(
        "<Return>",
        lambda event: send_message()
    )


    quick_frame = ctk.CTkFrame(
        main_frame,
        fg_color=BG_COLOR,
        height=38
    )

    quick_frame.pack(
        side="bottom",
        fill="x",
        padx=5,
        pady=(0, 2),
        before=input_frame
    )

    quick_frame.pack_propagate(False)

    quick_questions = [
        "Діагноз",
        "Сумісність",
        "Мутна вода?"
    ]

    for question in quick_questions:

        quick_button = ctk.CTkButton(
            quick_frame,
            text=question,
            font=("Arial", 9, "bold"),
            text_color=WHITE,
            fg_color=CARD_COLOR,
            hover_color="#00506B",
            corner_radius=10,
            height=30,
            width=96,
            command=lambda q=question: start_request(q)
        )

        quick_button.pack(
            side="left",
            padx=2,
            expand=True
        )


    status_label = ctk.CTkLabel(
        main_frame,
        text="AI готовий до спілкування",
        font=("Arial", 10),
        text_color=GRAY
    )

    status_label.pack(
        side="bottom",
        pady=(0, 2),
        before=quick_frame
    )

    add_message(
        "Привіт! 🐠\n\n"
        "Я AI-асистент Smart Aquarium Assistant.\n\n"
        "Допоможу тобі з доглядом за акваріумом, "
        "рибками, рослинами та якістю води.\n\n"
        "Що тебе цікавить?",
        "assistant"
    )


    if image_path:

        if os.path.exists(image_path):

            selected_image["path"] = image_path

            start_request(
                "Проаналізуй, будь ласка, "
                "це фото мого акваріума.",
                image_path
            )
