import customtkinter as ctk
import os
import json
import urllib.request
import urllib.parse
import urllib.error
import threading
import time
import random

from PIL import Image, ImageOps
from io import BytesIO


# Фотографії перевіряються лише один раз за запуск програми.
FISH_IMAGE_CHECK_STARTED = False


def fish_page(window, aquarium=None, back_command=None):

    for widget in window.winfo_children():
        widget.destroy()

    window.unbind("<Configure>")
    window.geometry("320x650")
    window.resizable(False, False)
    window.configure(fg_color="#00121F")

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    icons_folder = os.path.join(
        project_folder, "assets", "icons"
    )

    fish_folder = os.path.join(
        project_folder, "assets", "images", "fish"
    )

    os.makedirs(fish_folder, exist_ok=True)

    background_color = "#00121F"
    cyan_color = "#00F8FB"
    text_color = "#FFFFFF"

    fish_list = [

        # ПРЕСНОВОДНЫЕ

        {
            "name": "Неон",
            "latin": "Paracheirodon innesi",
            "type": "Прісновод",
            "search": "Neon tetra"
        },
        {
            "name": "Гуппі",
            "latin": "Poecilia reticulata",
            "type": "Прісновод",
            "search": "Guppy"
        },
        {
            "name": "Скалярія",
            "latin": "Pterophyllum scalare",
            "type": "Прісновод",
            "search": "Freshwater angelfish"
        },
        {
            "name": "Моллі",
            "latin": "Poecilia sphenops",
            "type": "Прісновод",
            "search": "Molly fish"
        },
        {
            "name": "Пецилія",
            "latin": "Xiphophorus maculatus",
            "type": "Прісновод",
            "search": "Platy fish"
        },
        {
            "name": "Мечоносець",
            "latin": "Xiphophorus hellerii",
            "type": "Прісновод",
            "search": "Swordtail fish"
        },
        {
            "name": "Даніо-реріо",
            "latin": "Danio rerio",
            "type": "Прісновод",
            "search": "Zebra danio"
        },
        {
            "name": "Барбус суматранський",
            "latin": "Puntigrus tetrazona",
            "type": "Прісновод",
            "search": "Tiger barb"
        },
        {
            "name": "Півник",
            "latin": "Betta splendens",
            "type": "Прісновод",
            "search": "Betta fish"
        },
        {
            "name": "Золота рибка",
            "latin": "Carassius auratus",
            "type": "Прісновод",
            "search": "Goldfish"
        },
        {
            "name": "Анциструс",
            "latin": "Ancistrus cirrhosus",
            "type": "Прісновод",
            "search": "Bristlenose pleco"
        },
        {
            "name": "Расбора",
            "latin": "Trigonostigma heteromorpha",
            "type": "Прісновод",
            "search": "Harlequin rasbora"
        },
        {
            "name": "Ляліус",
            "latin": "Trichogaster lalius",
            "type": "Прісновод",
            "search": "Dwarf gourami"
        },
        {
            "name": "Перлинний гурамі",
            "latin": "Trichopodus leerii",
            "type": "Прісновод",
            "search": "Pearl gourami"
        },
        {
            "name": "Дискус",
            "latin": "Symphysodon aequifasciatus",
            "type": "Прісновод",
            "search": "Discus fish"
        },
        {
            "name": "Тетра червононоса",
            "latin": "Hemigrammus rhodostomus",
            "type": "Прісновод",
            "search": "Rummy nose tetra"
        },
        {
            "name": "Кардинал",
            "latin": "Paracheirodon axelrodi",
            "type": "Прісновод",
            "search": "Cardinal tetra"
        },
        {
            "name": "Тернеція",
            "latin": "Gymnocorymbus ternetzi",
            "type": "Прісновод",
            "search": "Black skirt tetra"
        },
        {
            "name": "Барбус вишневий",
            "latin": "Puntius titteya",
            "type": "Прісновод",
            "search": "Cherry barb"
        },
        {
            "name": "Боція-клоун",
            "latin": "Chromobotia macracanthus",
            "type": "Прісновод",
            "search": "Clown loach"
        },
        {
            "name": "Акантофтальмус",
            "latin": "Pangio kuhlii",
            "type": "Прісновод",
            "search": "Kuhli loach"
        },
        {
            "name": "Отоцинклюс",
            "latin": "Otocinclus vittatus",
            "type": "Прісновод",
            "search": "Otocinclus catfish"
        },
        {
            "name": "Рамірезі",
            "latin": "Mikrogeophagus ramirezi",
            "type": "Прісновод",
            "search": "Ram cichlid"
        },
        {
            "name": "Апістограма",
            "latin": "Apistogramma cacatuoides",
            "type": "Прісновод",
            "search": "Cockatoo dwarf cichlid"
        },
        {
            "name": "Крибенсіс",
            "latin": "Pelvicachromis pulcher",
            "type": "Прісновод",
            "search": "Kribensis cichlid"
        },
        {
            "name": "Астронотус",
            "latin": "Astronotus ocellatus",
            "type": "Прісновод",
            "search": "Oscar fish"
        },
        {
            "name": "Северум",
            "latin": "Heros efasciatus",
            "type": "Прісновод",
            "search": "Severum cichlid"
        },
        {
            "name": "Райдужниця",
            "latin": "Melanotaenia boesemani",
            "type": "Прісновод",
            "search": "Boesemani rainbowfish"
        },
        {
            "name": "Кардинал китайський",
            "latin": "Tanichthys albonubes",
            "type": "Прісновод",
            "search": "White cloud mountain minnow"
        },
        {
            "name": "Даніо перлинний",
            "latin": "Danio margaritatus",
            "type": "Прісновод",
            "search": "Celestial pearl danio"
        },
        {
            "name": "Коридорас панда",
            "latin": "Corydoras panda",
            "type": "Прісновод",
            "search": "Panda corydoras"
        },
        {
            "name": "Скляний сом",
            "latin": "Kryptopterus vitreolus",
            "type": "Прісновод",
            "search": "Glass catfish"
        },
        {
            "name": "Метелик африканський",
            "latin": "Pantodon buchholzi",
            "type": "Прісновод",
            "search": "African butterflyfish"
        },
        {
            "name": "Плекостомус",
            "latin": "Pterygoplichthys pardalis",
            "type": "Прісновод",
            "search": "Sailfin pleco"
        },

        # МОРСКИЕ

        {
            "name": "Рибка-клоун",
            "latin": "Amphiprion ocellaris",
            "type": "Морські",
            "search": "Ocellaris clownfish"
        },
        {
            "name": "Хірург синій",
            "latin": "Paracanthurus hepatus",
            "type": "Морські",
            "search": "Blue tang"
        },
        {
            "name": "Хірург жовтий",
            "latin": "Zebrasoma flavescens",
            "type": "Морські",
            "search": "Yellow tang"
        },
        {
            "name": "Мандаринка",
            "latin": "Synchiropus splendidus",
            "type": "Морські",
            "search": "Mandarin dragonet"
        },
        {
            "name": "Крилатка",
            "latin": "Pterois volitans",
            "type": "Морські",
            "search": "Red lionfish"
        },
        {
            "name": "Грамма королівська",
            "latin": "Gramma loreto",
            "type": "Морські",
            "search": "Royal gramma"
        },
        {
            "name": "Кардинал Бангая",
            "latin": "Pterapogon kauderni",
            "type": "Морські",
            "search": "Banggai cardinalfish"
        },
        {
            "name": "Вогняна рибка",
            "latin": "Nemateleotris magnifica",
            "type": "Морські",
            "search": "Firefish goby"
        },
        {
            "name": "Губан шестисмуговий",
            "latin": "Pseudocheilinus hexataenia",
            "type": "Морські",
            "search": "Six line wrasse"
        },
        {
            "name": "Риба-лисиця",
            "latin": "Siganus vulpinus",
            "type": "Морські",
            "search": "Foxface rabbitfish"
        },
        {
            "name": "Риба-метелик",
            "latin": "Chaetodon auriga",
            "type": "Морські",
            "search": "Threadfin butterflyfish"
        },
        {
            "name": "Хроміс зелений",
            "latin": "Chromis viridis",
            "type": "Морські",
            "search": "Blue green chromis"
        },
        {
            "name": "Центропіг вогняний",
            "latin": "Centropyge loricula",
            "type": "Морські",
            "search": "Flame angelfish"
        },
        {
            "name": "Бичок-сторож",
            "latin": "Cryptocentrus cinctus",
            "type": "Морські",
            "search": "Yellow watchman goby"
        },
        {
            "name": "Собачка морська",
            "latin": "Salarias fasciatus",
            "type": "Морські",
            "search": "Lawnmower blenny"
        },
        {
            "name": "Губан-чистильник",
            "latin": "Labroides dimidiatus",
            "type": "Морські",
            "search": "Bluestreak cleaner wrasse"
        }
    ]

    # Завантажуємо вже збережені фотографії з комп'ютера.
    # Вони не завантажуються з інтернету повторно.

    for index, fish in enumerate(fish_list):

        image_path = os.path.join(
            fish_folder,
            f"fish_{index + 1:02d}.jpg"
        )

        if os.path.isfile(image_path):
            fish["image"] = image_path
        else:
            fish["image"] = None

    def download_fish_image(fish, index):

        image_name = f"fish_{index + 1:02d}.jpg"

        image_path = os.path.join(
            fish_folder,
            image_name
        )

        if os.path.exists(image_path):
            return image_path

        search_query = (
            f'"{fish["latin"]}" {fish["search"]} fish'
        )

        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": search_query,
            "gsrnamespace": 6,
            "gsrlimit": 1,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 400,
            "format": "json"
        }

        api_url = (
            "https://commons.wikimedia.org/w/api.php?"
            + urllib.parse.urlencode(params)
        )

        for attempt in range(5):

            try:

                request = urllib.request.Request(
                    api_url,
                    headers={
                        "User-Agent": (
                            "SmartAquariumAssistant/1.0 "
                            "(educational project)"
                        )
                    }
                )

                with urllib.request.urlopen(
                    request,
                    timeout=30
                ) as response:

                    data = json.loads(
                        response.read().decode("utf-8")
                    )

                pages = data.get(
                    "query", {}
                ).get("pages", {})

                if isinstance(pages, dict):
                    pages = list(pages.values())

                if not pages:
                    return None

                image_info = pages[0].get(
                    "imageinfo", []
                )

                if not image_info:
                    return None

                image_url = (
                    image_info[0].get("thumburl")
                    or image_info[0].get("url")
                )

                if not image_url:
                    return None

                image_request = urllib.request.Request(
                    image_url,
                    headers={
                        "User-Agent": (
                            "SmartAquariumAssistant/1.0 "
                            "(educational project)"
                        )
                    }
                )

                with urllib.request.urlopen(
                    image_request,
                    timeout=30
                ) as response:

                    image_data = response.read()

                photo = Image.open(
                    BytesIO(image_data)
                ).convert("RGB")

                photo = ImageOps.fit(
                    photo,
                    (330, 180),
                    method=Image.Resampling.LANCZOS
                )

                photo.save(
                    image_path,
                    "JPEG",
                    quality=90
                )

                print(
                    f"Завантажено: {fish['name']}"
                )

                return image_path

            except urllib.error.HTTPError as error:

                if error.code == 429:

                    retry_after = error.headers.get(
                        "Retry-After"
                    )

                    try:
                        wait_time = float(retry_after)
                    except (TypeError, ValueError):
                        wait_time = min(
                            60 * (2 ** attempt),
                            600
                        )

                    wait_time += random.uniform(2, 8)

                    print(
                        f"HTTP 429 для {fish['name']}. "
                        f"Очікування {int(wait_time)} секунд..."
                    )

                    time.sleep(wait_time)

                elif error.code in (500, 502, 503, 504):

                    wait_time = 10 * (attempt + 1)

                    print(
                        f"Помилка сервера {error.code}. "
                        f"Повтор через {wait_time} секунд."
                    )

                    time.sleep(wait_time)

                else:

                    print(
                        f"Помилка {error.code}: "
                        f"{fish['name']}"
                    )

                    return None

            except Exception as error:

                print(
                    f"Не вдалося завантажити "
                    f"{fish['name']}: {error}"
                )

                return None

        print(
            f"Вичерпано спроби: {fish['name']}"
        )

        return None

    def download_all_images():

        missing_fish = [
            (i, fish)
            for i, fish in enumerate(fish_list)
            if not fish.get("image")
            or not os.path.isfile(fish["image"])
        ]

        if not missing_fish:
            return

        for position, (i, fish) in enumerate(missing_fish):

            image_path = download_fish_image(fish, i)
            fish["image"] = image_path

            try:

                if window.winfo_exists() and main_frame.winfo_exists():
                    window.after(0, update_fish)
                else:
                    break

            except Exception:
                break

            if position < len(missing_fish) - 1:
                time.sleep(random.uniform(5, 8))

    main_frame = ctk.CTkFrame(
        window,
        width=320,
        height=650,
        corner_radius=0,
        fg_color=background_color,
        border_width=0
    )

    main_frame.place(x=0, y=0)

    back_button = ctk.CTkButton(
        main_frame,
        text="←",
        width=35,
        height=35,
        corner_radius=8,
        fg_color="transparent",
        hover_color="#003047",
        text_color=cyan_color,
        font=("Arial", 29, "bold"),
        border_width=0,
        command=lambda: (
            back_command()
            if back_command is not None
            else __import__("home").home_page(
                window, aquarium
            )
        )
    )

    back_button.place(x=19, y=25)

    title = ctk.CTkLabel(
        main_frame,
        text="Рибки",
        font=("Arial", 17, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )

    title.place(
        relx=0.5,
        y=31,
        anchor="center"
    )

    def open_care():

        from care import care_page
        care_page(window, aquarium)

    calendar_path = os.path.join(
        icons_folder,
        "calendar.png"
    )

    if os.path.exists(calendar_path):

        calendar_photo = Image.open(
            calendar_path
        ).convert("RGBA")

        calendar_image = ctk.CTkImage(
            light_image=calendar_photo,
            dark_image=calendar_photo,
            size=(27, 27)
        )

        calendar_button = ctk.CTkButton(
            main_frame,
            text="",
            image=calendar_image,
            width=38,
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#003047",
            border_width=0,
            command=open_care
        )

        calendar_button.place(
            x=268,
            y=23
        )

        main_frame.calendar_image = calendar_image

    search_frame = ctk.CTkFrame(
        main_frame,
        width=284,
        height=43,
        corner_radius=13,
        fg_color="#003047",
        border_width=1,
        border_color=cyan_color
    )

    search_frame.place(
        x=18,
        y=78
    )

    search_icon = ctk.CTkLabel(
        search_frame,
        text="⌕",
        font=("Arial", 32),
        text_color="#C7E1EB",
        fg_color="transparent"
    )

    search_icon.place(
        x=12,
        y=1
    )

    search_entry = ctk.CTkEntry(
        search_frame,
        width=220,
        height=35,
        corner_radius=0,
        fg_color="transparent",
        border_width=0,
        text_color=text_color,
        placeholder_text="Пошук рибки...",
        placeholder_text_color=text_color,
        font=("Arial", 13, "bold")
    )

    search_entry.place(
        x=48,
        y=4
    )

    selected_category = "Усі"

    categories = [
        ("Усі", 94),
        ("Прісновод", 96),
        ("Морські", 94)
    ]

    category_buttons = {}

    def select_category(category):

        nonlocal selected_category

        selected_category = category

        for name, button in category_buttons.items():

            button.configure(
                fg_color=(
                    "#20DCE5"
                    if name == category
                    else background_color
                ),
                text_color=(
                    "#00121F"
                    if name == category
                    else text_color
                )
            )

        update_fish()

    x_positions = [18, 112, 208]

    for i, (category, width) in enumerate(categories):

        button = ctk.CTkButton(
            main_frame,
            text=category,
            width=width,
            height=34,
            corner_radius=13,
            fg_color=(
                "#20DCE5"
                if category == "Усі"
                else background_color
            ),
            hover_color="#00506B",
            border_width=1,
            border_color=cyan_color,
            text_color=(
                "#00121F"
                if category == "Усі"
                else text_color
            ),
            font=("Arial", 12, "bold"),
            command=lambda name=category: select_category(name)
        )

        button.place(
            x=x_positions[i],
            y=137
        )

        category_buttons[category] = button

    fish_scroll = ctk.CTkScrollableFrame(
        main_frame,
        width=286,
        height=350,
        corner_radius=0,
        fg_color="transparent",
        scrollbar_button_color="#00617A",
        scrollbar_button_hover_color=cyan_color
    )

    fish_scroll.place(
        x=12,
        y=194
    )

    fish_images = []

    def update_fish():

        for widget in fish_scroll.winfo_children():
            widget.destroy()

        fish_images.clear()

        search_text = (
            search_entry.get().lower().strip()
        )

        filtered_fish = []

        for fish in fish_list:

            image_path = fish.get("image")

            # Рыбки без фотографий не отображаются.
            if not image_path or not os.path.isfile(image_path):
                continue

            matches_category = (
                selected_category == "Усі"
                or fish["type"] == selected_category
            )

            matches_search = (
                search_text in fish["name"].lower()
                or search_text in fish["latin"].lower()
            )

            if matches_category and matches_search:
                filtered_fish.append(fish)

        if not filtered_fish:

            empty_label = ctk.CTkLabel(
                fish_scroll,
                text="Рибок не знайдено",
                font=("Arial", 13),
                text_color="#A8B8C0"
            )

            empty_label.pack(pady=35)

            return

        for i, fish in enumerate(filtered_fish):

            row = i // 2
            column = i % 2

            card = ctk.CTkFrame(
                fish_scroll,
                width=132,
                height=112,
                corner_radius=17,
                fg_color="#003047",
                border_width=0
            )

            card.grid(
                row=row,
                column=column,
                padx=(3, 8),
                pady=(5, 10),
                sticky="n"
            )

            card.grid_propagate(False)

            # ФОТОГРАФИЯ

            image_path = fish.get("image")

            if image_path and os.path.exists(image_path):

                try:

                    photo = Image.open(
                        image_path
                    ).convert("RGB")

                    fish_image = ctk.CTkImage(
                        light_image=photo,
                        dark_image=photo,
                        size=(110, 60)
                    )

                    fish_images.append(fish_image)

                    image_label = ctk.CTkLabel(
                        card,
                        text="",
                        image=fish_image,
                        fg_color="transparent",
                        corner_radius=9,
                        width=110,
                        height=60
                    )

                except Exception:

                    image_label = ctk.CTkLabel(
                        card,
                        text="🐠",
                        font=("Arial", 30),
                        text_color=cyan_color,
                        fg_color="#00445C",
                        corner_radius=9,
                        width=110,
                        height=60
                    )

            else:

                image_label = ctk.CTkLabel(
                    card,
                    text="🐠",
                    font=("Arial", 30),
                    text_color=cyan_color,
                    fg_color="#00445C",
                    corner_radius=9,
                    width=110,
                    height=60
                )

            image_label.place(
                relx=0.5,
                y=8,
                anchor="n"
            )

            # УКРАИНСКОЕ НАЗВАНИЕ

            name_label = ctk.CTkLabel(
                card,
                text=fish["name"],
                font=("Arial", 12, "bold"),
                text_color=text_color,
                fg_color="transparent",
                anchor="w",
                width=110
            )

            name_label.place(
                x=11,
                y=72
            )

            # ЛАТИНСКОЕ НАЗВАНИЕ

            latin_label = ctk.CTkLabel(
                card,
                text=fish["latin"],
                font=("Arial", 8),
                text_color="#A8B8C0",
                fg_color="transparent",
                anchor="w",
                width=110
            )

            latin_label.place(
                x=11,
                y=92
            )

    # Обновление поиска

    search_entry.bind(
        "<KeyRelease>",
        lambda event: update_fish()
    )

    update_fish()

    navigation_frame = ctk.CTkFrame(
        main_frame,
        width=304,
        height=65,
        corner_radius=20,
        fg_color="#003047",
        border_width=1,
        border_color="#91B7C7"
    )

    navigation_frame.place(
        x=8,
        y=575
    )

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
                back_command=lambda: fish_page(
                    window,
                    aquarium,
                    back_command
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

    for i, (icon_file, page_name) in enumerate(
        navigation_items
    ):

        icon_path = os.path.join(
            icons_folder,
            icon_file
        )

        icon_image = None

        if os.path.exists(icon_path):

            icon_photo = Image.open(
                icon_path
            ).convert("RGBA")

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
                "#00435A"
                if i == 0
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

    main_frame.fish_images = fish_images
    main_frame.navigation_images = navigation_images

    # Проверка фотографий запускается только один раз.
    global FISH_IMAGE_CHECK_STARTED

    missing_images_exist = any(
        not fish.get("image") or not os.path.isfile(fish["image"])
        for fish in fish_list
    )

    if missing_images_exist and not FISH_IMAGE_CHECK_STARTED:

        FISH_IMAGE_CHECK_STARTED = True

        download_thread = threading.Thread(
            target=download_all_images,
            daemon=True
        )

        download_thread.start()