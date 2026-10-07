import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


window = ctk.CTk()

window.title("Smart Aquarium Assistant")
window.geometry("320x650")
window.resizable(False, False)

background_color = "#001B2E"
field_color = "#003B55"
cyan_color = "#00F8FB"
green_color = "#60D48C"
white_color = "#FFFFFF"
gray_color = "#A8B8C0"
error_color = "#FF7070"

window.configure(
    fg_color=background_color
)

back_button = ctk.CTkButton(
    window,
    text="←",
    width=35,
    height=35,
    font=("Arial", 22),
    fg_color="transparent",
    hover_color="#003047",
    text_color=cyan_color,
    corner_radius=10
)

back_button.place(
    x=15,
    y=15
)

title = ctk.CTkLabel(
    window,
    text="Реєстрація",
    font=("Arial", 22, "bold"),
    text_color=white_color
)

title.place(
    x=35,
    y=70
)

subtitle = ctk.CTkLabel(
    window,
    text="Створіть акаунт для керування акваріумом",
    font=("Arial", 9),
    text_color=gray_color
)

subtitle.place(
    x=35,
    y=105
)

def create_field(y, text, placeholder, show=None):

    label = ctk.CTkLabel(
        window,
        text=text,
        font=("Arial", 9),
        text_color=white_color
    )

    label.place(
        x=35,
        y=y
    )

    entry = ctk.CTkEntry(
        window,
        width=250,
        height=40,
        corner_radius=10,
        border_width=1,
        border_color="#00516D",
        fg_color=field_color,
        text_color=white_color,
        placeholder_text=placeholder,
        placeholder_text_color="#76939F",
        font=("Arial", 10),
        show=show
    )

    entry.place(
        x=35,
        y=y + 20
    )

    return entry

name_entry = create_field(
    130,
    "Ім'я",
    "Введіть ваше ім'я"
)


email_entry = create_field(
    205,
    "Email",
    "Введіть Email"
)


password_entry = create_field(
    280,
    "Пароль",
    "Введіть пароль",
    "*"
)


confirm_password_entry = create_field(
    355,
    "Підтвердіть пароль",
    "Повторіть пароль",
    "*"
)

message = ctk.CTkLabel(
    window,
    text="",
    font=("Arial", 8),
    text_color=cyan_color,
    anchor="w"
)

message.place(
    x=35,
    y=405
)

def register():

    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if name == "":
        message.configure(
            text="Введіть ім'я",
            text_color=error_color
        )
        return

    if email == "":
        message.configure(
            text="Введіть Email",
            text_color=error_color
        )
        return

    if password == "":
        message.configure(
            text="Введіть пароль",
            text_color=error_color
        )
        return

    if confirm_password == "":
        message.configure(
            text="Підтвердіть пароль",
            text_color=error_color
        )
        return

    if password != confirm_password:
        message.configure(
            text="Паролі не співпадають",
            text_color=error_color
        )
        return

    message.configure(
        text="Реєстрація успішна!",
        text_color=green_color
    )

register_button = ctk.CTkButton(
    window,
    text="Зареєструватися",
    width=250,
    height=45,
    corner_radius=12,
    fg_color=cyan_color,
    hover_color="#4FFFFF",
    text_color=background_color,
    font=("Arial", 10, "bold"),
    command=register
)

register_button.place(
    x=35,
    y=440
)

account_frame = ctk.CTkFrame(
    window,
    width=250,
    height=30,
    fg_color="transparent"
)

account_frame.place(
    x=35,
    y=505
)


question = ctk.CTkLabel(
    account_frame,
    text="Вже маєте акаунт?",
    font=("Arial", 9),
    text_color=gray_color
)

question.pack(
    side="left"
)

def open_login():

    message.configure(
        text="Відкриття сторінки входу...",
        text_color=cyan_color
    )


login_button = ctk.CTkButton(
    account_frame,
    text="Увійти",
    width=45,
    height=25,
    fg_color="transparent",
    hover_color="#003047",
    text_color=cyan_color,
    font=("Arial", 9, "bold"),
    corner_radius=6,
    command=open_login
)

login_button.pack(
    side="left",
    padx=(5, 0)
)

window.mainloop()