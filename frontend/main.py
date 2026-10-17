import customtkinter as ctk
from welcome import welcome_page

# Настройки оформления
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Создание главного окна
window = ctk.CTk()
window.title("Smart Aquarium Assistant")
window.geometry("320x650")
window.resizable(False, False)
window.configure(fg_color="#001B2E")


# Запуск стартовой страницы
welcome_page(window)


# Запуск приложения
window.mainloop()