import tkinter as tk

window = tk.Tk()
window.title("Smart Aquarium Assistant")
window.geometry("320x650")
window.resizable(False, False)

background_color = "#001B2E"
field_color = "#003B55"
cyan_color = "#00F8FB"
green_color = "#60D48C"
white_color = "#FFFFFF"
gray_color = "#A8B8C0"

window.configure(bg=background_color)

back_button = tk.Button(
    window,
    text="←",
    font=("Arial", 18),
    bg=background_color,
    fg=cyan_color,
    activebackground=background_color,
    activeforeground=white_color,
    relief="flat",
    bd=0,
    cursor="hand2"
)

back_button.place(
    x=18,
    y=18,
    width=35,
    height=35
)

title = tk.Label(
    window,
    text="Реєстрація",
    font=("Arial", 20, "bold"),
    bg=background_color,
    fg=white_color
)

title.place(
    x=35,
    y=70
)

def create_field(y, text, show=""):

    label = tk.Label(
        window,
        text=text,
        font=("Arial", 9),
        bg=background_color,
        fg=white_color
    )

    label.place(
        x=35,
        y=y
    )

    entry = tk.Entry(
        window,
        font=("Arial", 10),
        bg=field_color,
        fg=white_color,
        insertbackground=white_color,
        relief="flat",
        bd=0,
        show=show
    )

    entry.place(
        x=35,
        y=y + 20,
        width=250,
        height=36
    )

    return entry

name_entry = create_field(
    125,
    "Ім'я"
)

email_entry = create_field(
    200,
    "Email"
)

password_entry = create_field(
    275,
    "Пароль",
    "*"
)

confirm_password_entry = create_field(
    350,
    "Підтвердіть пароль",
    "*"
)


window.mainloop()