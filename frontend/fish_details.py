import os
import json
import customtkinter as ctk
from PIL import Image, ImageOps

from fish_data import FISH_INFO


def fish_details_page(window, fish, aquarium=None, back_command=None, project_folder=None, icons_folder=None):
    """Показує детальну інформацію та дозволяє додати рибку до вибраного акваріума."""
    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    bg = "#00121F"
    card = "#003047"
    cyan = "#00F8FB"
    white = "#FFFFFF"
    muted = "#A8B8C0"

    if project_folder is None:
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if icons_folder is None:
        icons_folder = os.path.join(project_folder, "assets", "icons")

    info = FISH_INFO.get(fish["latin"], {})
    display_name = info.get("display_name", fish["name"])
    temperament = info.get("temperament", "Залежить від виду")
    size = info.get("size", "Залежить від виду")
    lifespan = info.get("lifespan", "Залежить від умов утримання")
    temperature = info.get("temperature", "Залежить від виду")

    description = info.get(
        "description",
        f"{display_name} ({fish['latin']}) — представник групи "
        f"{'морських' if fish['type'] == 'Морські' else 'прісноводних'} риб. "
        "Перед поселенням перевірте параметри води та переконайтеся, що умови "
        "акваріума відповідають потребам цього виду."
    )

    compatibility = info.get(
        "compatibility",
        "Підбирайте сусідів з урахуванням розміру, темпераменту та однакових "
        "вимог до води. Не поєднуйте маленьких риб із великими хижаками."
    )

    care = info.get(
        "care",
        "Підтримуйте стабільну температуру, якісну фільтрацію та регулярну "
        "підміну води. Годуйте відповідним кормом невеликими порціями й "
        "не перенаселяйте акваріум."
    )

    root = ctk.CTkFrame(window, fg_color=bg, corner_radius=0)
    root.place(x=0, y=0, relwidth=1, relheight=1)

    def go_back():
        if back_command is not None:
            back_command()
        else:
            from fish import fish_page
            fish_page(window, aquarium)

    back_button = ctk.CTkButton(
        root,
        text="←",
        width=38,
        height=38,
        corner_radius=9,
        fg_color="transparent",
        hover_color=card,
        text_color=cyan,
        font=("Arial", 29, "bold"),
        command=go_back
    )
    back_button.place(x=18, y=17)

    title = ctk.CTkLabel(
        root,
        text="Деталі рибки",
        font=("Arial", 18, "bold"),
        text_color=white
    )
    title.place(relx=0.5, y=31, anchor="center")

    content = ctk.CTkScrollableFrame(
        root,
        width=294,
        height=435,
        corner_radius=0,
        fg_color="transparent",
        scrollbar_button_color="#00617A",
        scrollbar_button_hover_color=cyan
    )
    content.place(x=13, y=62)

    photo_frame = ctk.CTkFrame(
        content,
        width=280,
        height=164,
        corner_radius=12,
        fg_color=card,
        border_width=2,
        border_color=cyan
    )
    photo_frame.pack(pady=(3, 10))
    photo_frame.pack_propagate(False)

    photo_label = ctk.CTkLabel(
        photo_frame,
        text="🐠",
        font=("Arial", 48),
        text_color=cyan
    )
    photo_label.place(relx=0.5, rely=0.5, anchor="center")

    image_path = fish.get("image")

    if image_path and os.path.isfile(image_path):
        try:
            photo = Image.open(image_path).convert("RGB")
            photo = ImageOps.fit(
                photo,
                (276, 160),
                method=Image.Resampling.LANCZOS
            )

            detail_image = ctk.CTkImage(
                light_image=photo,
                dark_image=photo,
                size=(276, 160)
            )

            photo_label.configure(image=detail_image, text="")
            photo_frame.detail_image = detail_image

        except Exception:
            pass

    name_label = ctk.CTkLabel(
        content,
        text=display_name,
        font=("Arial", 18, "bold"),
        text_color=white,
        anchor="w"
    )
    name_label.pack(fill="x", padx=7)

    latin_label = ctk.CTkLabel(
        content,
        text=fish["latin"],
        font=("Arial", 12),
        text_color=muted,
        anchor="w"
    )
    latin_label.pack(fill="x", padx=7, pady=(0, 8))

    tags = ctk.CTkFrame(content, fg_color="transparent")
    tags.pack(fill="x", padx=5, pady=(0, 12))

    type_badge = ctk.CTkLabel(
        tags,
        text=temperament,
        fg_color="#20DCE5",
        text_color=bg,
        corner_radius=16,
        font=("Arial", 12, "bold"),
        padx=13,
        pady=5
    )
    type_badge.pack(side="left")

    size_badge = ctk.CTkLabel(
        tags,
        text=size,
        text_color=white,
        font=("Arial", 13)
    )
    size_badge.pack(side="left", padx=13)

    tabs = ctk.CTkFrame(content, fg_color="transparent")
    tabs.pack(fill="x", padx=1, pady=(0, 12))

    tab_content = ctk.CTkFrame(
        content,
        fg_color="transparent",
        corner_radius=0
    )
    tab_content.pack(fill="x", padx=6, pady=(0, 10))

    tab_text = {
        "Опис": description,
        "Сумісність": compatibility,
        "Догляд": care
    }

    tab_buttons = {}

    def show_tab(tab_name):
        for name, button in tab_buttons.items():
            button.configure(
                fg_color=cyan if name == tab_name else card,
                text_color=bg if name == tab_name else white
            )

        for widget in tab_content.winfo_children():
            widget.destroy()

        text_label = ctk.CTkLabel(
            tab_content,
            text=tab_text[tab_name],
            font=("Arial", 13, "bold"),
            text_color=white,
            justify="left",
            anchor="w",
            wraplength=270
        )
        text_label.pack(fill="x", pady=(2, 12))

    for tab_name in ("Опис", "Сумісність", "Догляд"):
        button = ctk.CTkButton(
            tabs,
            text=tab_name,
            width=91,
            height=37,
            corner_radius=14,
            fg_color=card,
            hover_color="#00506B",
            border_width=1,
            border_color=cyan,
            text_color=white,
            font=("Arial", 12, "bold"),
            command=lambda name=tab_name: show_tab(name)
        )
        button.pack(side="left", padx=(0, 5))
        tab_buttons[tab_name] = button

    show_tab("Опис")

    facts = [
        ("Темперамент", temperament),
        ("Розмір", size),
        ("Тривалість життя", lifespan),
        ("Температура", temperature)
    ]

    for label_text, value_text in facts:
        row = ctk.CTkFrame(
            content,
            height=43,
            corner_radius=15,
            fg_color=card,
            border_width=1,
            border_color=cyan
        )
        row.pack(fill="x", padx=1, pady=2)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=label_text,
            font=("Arial", 13, "bold"),
            text_color=white,
            anchor="w"
        ).place(x=13, rely=0.5, anchor="w")

        ctk.CTkLabel(
            row,
            text=value_text,
            font=("Arial", 12, "bold"),
            text_color=white,
            anchor="e"
        ).place(relx=0.97, rely=0.5, anchor="e")

    def add_to_aquarium():
        data_folder = os.path.join(project_folder, "assets", "data")
        os.makedirs(data_folder, exist_ok=True)

        data_path = os.path.join(data_folder, "aquarium_fish.json")

        aquarium_key = "default"
        aquarium_name = "Мій акваріум"

        if isinstance(aquarium, dict):
            aquarium_key = str(
                aquarium.get("id")
                or aquarium.get("name")
                or aquarium.get("title")
                or "default"
            )

            aquarium_name = str(
                aquarium.get("name")
                or aquarium.get("title")
                or aquarium_name
            )

        elif isinstance(aquarium, str) and aquarium:
            aquarium_key = aquarium
            aquarium_name = aquarium

        saved_data = {}

        if os.path.isfile(data_path):
            try:
                with open(data_path, "r", encoding="utf-8") as file:
                    saved_data = json.load(file)

                if not isinstance(saved_data, dict):
                    saved_data = {}

            except (OSError, json.JSONDecodeError):
                saved_data = {}

        fish_in_aquarium = saved_data.get(aquarium_key, [])

        if not isinstance(fish_in_aquarium, list):
            fish_in_aquarium = []

        existing = None

        for saved_fish in fish_in_aquarium:
            if saved_fish.get("latin") == fish["latin"]:
                existing = saved_fish
                break

        if existing is not None:
            existing["count"] = int(existing.get("count", 1)) + 1

        else:
            fish_in_aquarium.append({
                "name": display_name,
                "latin": fish["latin"],
                "type": fish["type"],
                "image": image_path if image_path and os.path.isfile(image_path) else "",
                "count": 1
            })

        saved_data[aquarium_key] = fish_in_aquarium

        with open(data_path, "w", encoding="utf-8") as file:
            json.dump(
                saved_data,
                file,
                ensure_ascii=False,
                indent=4
            )

        if isinstance(aquarium, dict):
            aquarium["fish"] = fish_in_aquarium

        add_button.configure(
            text=f"Додано до «{aquarium_name}» ✓",
            fg_color="#20DCE5"
        )

    add_button = ctk.CTkButton(
        root,
        text="Додати до акваріума",
        width=284,
        height=49,
        corner_radius=17,
        fg_color="#20DCE5",
        hover_color="#12C8D2",
        text_color=bg,
        font=("Arial", 15, "bold"),
        command=add_to_aquarium
    )
    add_button.place(x=18, y=510)

    navigation_frame = ctk.CTkFrame(
        root,
        width=304,
        height=65,
        corner_radius=20,
        fg_color=card,
        border_width=1,
        border_color="#91B7C7"
    )
    navigation_frame.place(x=8, y=575)

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
                back_command=lambda: fish_details_page(
                    window,
                    fish,
                    aquarium,
                    back_command,
                    project_folder,
                    icons_folder
                ),
                aquarium=aquarium
            )

        elif page_name == "Головна":
            from home import home_page
            home_page(window, aquarium)

        elif page_name == "Догляд":
            from care import care_page
            care_page(window, aquarium)

        elif page_name == "Історія":
            from history import history_page
            history_page(window, aquarium)

        elif page_name == "Профіль":
            from profile import profile_page
            profile_page(window, aquarium)

    for i, (icon_file, page_name) in enumerate(navigation_items):
        icon_path = os.path.join(icons_folder, icon_file)
        icon_image = None

        if os.path.isfile(icon_path):
            try:
                icon_photo = Image.open(icon_path).convert("RGBA")

                icon_image = ctk.CTkImage(
                    light_image=icon_photo,
                    dark_image=icon_photo,
                    size=(30, 30)
                )

                navigation_images.append(icon_image)

            except Exception:
                pass

        nav_button = ctk.CTkButton(
            navigation_frame,
            text="",
            image=icon_image,
            width=48,
            height=52,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#00506B",
            border_width=0,
            command=lambda name=page_name: navigate(name)
        )

        nav_button.place(x=4 + i * 59, y=5)

    root.navigation_images = navigation_images


__all__ = ["fish_details_page"]