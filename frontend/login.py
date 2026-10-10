import customtkinter as ctk

def login_page(window):

    title = ctk.CTkLabel(
        window,
        text="Вхід",
        font=("Arial", 22, "bold"),
        text_color="#FFFFFF"
    )
    title.place(x=35, y=65)

    subtitle = ctk.CTkLabel(
        window,
        text="Увійдіть до свого акаунта",
        font=("Arial", 12),
        text_color="#A8B8C0"
    )
    subtitle.place(x=35, y=100)

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
    email_entry.place(x=35, y=150)

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
    password_entry.place(x=35, y=205)

    forgot_button = ctk.CTkButton(
        window,
        text="Забули пароль?",
        width=110,
        height=25,
        corner_radius=5,
        fg_color="transparent",
        hover_color="#003047",
        text_color="#00F8FB",
        font=("Arial", 11),
        command=lambda: print("Відновлення пароля")
    )
    forgot_button.place(x=175, y=260)

    message = ctk.CTkLabel(
        window,
        text="",
        font=("Arial", 11),
        text_color="#FF7070"
    )
    message.place(x=35, y=300)


    def back_to_welcome():
        from welcome import welcome_page

        for widget in window.winfo_children():
            widget.destroy()

        welcome_page(window)

    back_button = ctk.CTkButton(
        window,
        text="←",
        width=35,
        height=35,
        corner_radius=10,
        fg_color="transparent",
        hover_color="#003047",
        text_color="#FFFFFF",
        font=("Arial", 24, "bold"),
        command=back_to_welcome
    )
    back_button.place(x=15, y=15)


    def login():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            message.configure(
                text="Заповніть усі поля",
                text_color="#FF7070"
            )
        else:
            message.configure(
                text="Вхід виконано!",
                text_color="#60D48C"
            )

    login_button = ctk.CTkButton(
        window,
        text="Увійти",
        width=250,
        height=45,
        corner_radius=12,
        fg_color="#00F8FB",
        hover_color="#00D5D8",
        text_color="#001B2E",
        font=("Arial", 13, "bold"),
        command=login
    )
    login_button.place(x=35, y=335)

    # Перехід до реєстрації
    register_text = ctk.CTkLabel(
        window,
        text="Ще немаєте акаунта?",
        font=("Arial", 12),
        text_color="#A8B8C0"
    )
    register_text.place(x=45, y=410)

    def open_register():
        from register import register_page

        for widget in window.winfo_children():
            widget.destroy()

        register_page(window)

    register_button = ctk.CTkButton(
        window,
        text="Зареєструватися",
        width=120,
        height=30,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#003047",
        text_color="#00F8FB",
        font=("Arial", 12, "bold"),
        command=open_register
    )
    register_button.place(x=165, y=405)