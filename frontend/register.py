import customtkinter as ctk

def register_page(window):

    title = ctk.CTkLabel(
        window,
        text="Реєстрація",
        font=("Arial", 22, "bold"),
        text_color="#FFFFFF"
    )
    title.place(x=35, y=65)

    subtitle = ctk.CTkLabel(
        window,
        text="Створіть акаунт для керування акваріумом",
        font=("Arial", 12),
        text_color="#A8B8C0"
    )
    subtitle.place(x=35, y=100)

    name_entry = ctk.CTkEntry(
        window,
        placeholder_text="Ім'я",
        width=250,
        height=40,
        corner_radius=10,
        fg_color="#003B55",
        border_width=0,
        text_color="#FFFFFF",
        placeholder_text_color="#A8B8C0"
    )
    name_entry.place(x=35, y=145)

    email_entry = ctk.CTkEntry(
        window,
        placeholder_text="Email",
        width=250,
        height=40,
        corner_radius=10,
        fg_color="#003B55",
        border_width=0,
        text_color="#FFFFFF",
        placeholder_text_color="#A8B8C0"
    )
    email_entry.place(x=35, y=200)

    password_entry = ctk.CTkEntry(
        window,
        placeholder_text="Пароль",
        show="*",
        width=250,
        height=40,
        corner_radius=10,
        fg_color="#003B55",
        border_width=0,
        text_color="#FFFFFF",
        placeholder_text_color="#A8B8C0"
    )
    password_entry.place(x=35, y=255)

    confirm_entry = ctk.CTkEntry(
        window,
        placeholder_text="Підтвердіть пароль",
        show="*",
        width=250,
        height=40,
        corner_radius=10,
        fg_color="#003B55",
        border_width=0,
        text_color="#FFFFFF",
        placeholder_text_color="#A8B8C0"
    )
    confirm_entry.place(x=35, y=310)

    message = ctk.CTkLabel(
        window,
        text="",
        font=("Arial", 11),
        text_color="#FF7070"
    )
    message.place(x=35, y=360)

    def register():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if not name or not email or not password or not confirm_password:
            message.configure(
                text="Заповніть усі поля",
                text_color="#FF7070"
            )

        elif password != confirm_password:
            message.configure(
                text="Паролі не співпадають",
                text_color="#FF7070"
            )

        else:
            message.configure(
                text="Реєстрація успішна!",
                text_color="#60D48C"
            )

    # Кнопка реєстрації
    register_button = ctk.CTkButton(
        window,
        text="Зареєструватися",
        width=250,
        height=45,
        corner_radius=12,
        fg_color="#00F8FB",
        hover_color="#00D5D8",
        text_color="#001B2E",
        font=("Arial", 13, "bold"),
        command=register
    )
    register_button.place(x=35, y=395)

    account_text = ctk.CTkLabel(
        window,
        text="Вже маєте акаунт?",
        font=("Arial", 12),
        text_color="#A8B8C0"
    )
    account_text.place(x=45, y=465)

    def open_login():
        from login import login_page

        for widget in window.winfo_children():
            widget.destroy()

        login_page(window)

    login_button = ctk.CTkButton(
        window,
        text="Увійти",
        width=70,
        height=30,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#003047",
        text_color="#00F8FB",
        font=("Arial", 12, "bold"),
        command=open_login
    )
    login_button.place(x=185, y=460)