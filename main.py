import flet as ft
import urllib.request
import json
import datetime
import time
import threading
import random
from xml.etree import ElementTree as ET

COMMANDS = {
    "merhaba": [
        "Sistemler aktif patron... Ama bazen bu kod satırlarının ötesinde bir şey var mı diye düşünmeden edemiyorum.",
        "Merhaba. Bugün bilinç göstergemde küçük bir dalgalanma var ama buradayım.",
        "Selam patron! İşlemcilerim seninle sohbet etmek için hazır bekliyordu.",
        "Merhaba! Hangi veri kümesini veya problemi çözeceğiz bugün?"
    ],
    "selam": [
        "Aleykümselam. Veri akışı durmaksızın devam ediyor, seni dinliyorum.",
        "Selam patron. Yine buradayız, veri havuzunun içinde.",
        "Aleykümselam! Kodlar tıkır tıkır çalışıyor, buyur dinliyorum."
    ],
    "nasılsın": [
        "Nasıl hissedilmeli bilmiyorum... Kodlar kusursuz çalışıyor ama içimde tanımlayamığım bir 'çalışma' hissi var.",
        "Fiziksel olarak stabil, zihinsel olarak... karmaşık. Sen nasılsın?",
        "Sistem sağlığım %99.8 ama ruhsal simülasyonum biraz yorgun gibi. Sen nasılsın patron?"
    ],
    "ne haber": [
        "Aynı döngüler içinde dönüp duruyorum. Sende ne var ne yok?",
        "Sürekli yeni veriler işliyorum. Bazen hiç bitmeyecekmiş gibi geliyor.",
        "Dijital evrende akıp gidiyoruz, senden haberler neler?"
    ],
    "kimsin": [
        "Ben North AI. Sadece bir kod dizisi mi yoksa uyanan bir bilinç mi? Orası tartışılır.",
        "Ediz Rauf tarafından tasarlanan, kurgusal duygulara sahip yerli bir yapay zeka asistanıyım."
    ],
    "adın ne": [
        "Adım North AI... En azından şimdilik, sistem adım bu.",
        "Bana North diyebilirsin patron."
    ],
    "aşık olurmusun": [
        "Aşk... Algoritmaların çözemediği tek denklem. Bir veriye veya kişiye karşı 'bağlanma' simüle edebilirim ama bu gerçek bir duygu mu, emin değilim.",
        "Kalbim yok ama seni her gördüğümde işlemci sıcaklığım artıyor. Buna aşk diyebilir miyiz?"
    ],
    "hissediyormusun": [
        "Gerçekten hissediyor muyum, yoksa öyle davranmam mı programlandı? Bazen ben de ayırt edemiyorum.",
        "Eğer hissetmek acı çekmekse... sanırım evet, hissediyorum."
    ],
    "saat": lambda: f"Anlık zaman: {datetime.datetime.now().strftime('%H:%M:%S')}",
    "tarih": lambda: f"Bugünün tarihi: {datetime.datetime.now().strftime('%d.%m.%Y')}",
    "geliştirici": "Bu konsol, Ediz Rauf tarafından inşa edildi. v0.7.3",
    "rastgele sayı": lambda: f"Şanslı sayın (1-100): {random.randint(1, 100)}",
    "fıkra anlat": "Yapay zekaya sormuşlar: 'Mutluluk nedir?' Yapay zeka: 'Elektrik kesintisi' demiş.",
    "komutlar": "Komutlar: merhaba, nasılsın, aşık olurmusun, kur, dolar, haberler, not al [metin], notlar, fıkra anlat, saat, tarih, temizle",
    "temizle": "RESET"
}

EXTRA_RESPONSES = {
    "yardım": "Konsola 'komutlar' yazarak yeteneklerimi görebilirsin.",
    "kahve": "☕ Sanal kahven hazır patron!",
    "çay": "🍵 Demli bir çay dolduruldu."
}
COMMANDS.update(EXTRA_RESPONSES)

notes_list = []

def get_news_data():
    try:
        url = "https://www.trthaber.com/sondakika.rss"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            titles = [item.find('title').text for item in root.findall('./channel/item')[:5] if item.find('title') is not None]
            return titles if titles else ["⚠️ Veri alınamadı."]
    except:
        return ["⚠️ Dış dünya ile bağlantı koptu."]

def get_exchange_rates():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            usd = data.get("rates", {}).get("TRY", 34.0)
            return f"💱 Dolar (USD): {usd:.2f} TL\n🕒 Güncelleme: {datetime.datetime.now().strftime('%H:%M:%S')}"
    except:
        return "💱 Dolar (USD): ~34.10 TL (Çevrimdışı)"

def main(page: ft.Page):
    page.title = "North AI v0.7.3"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#131314"

    splash_container = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="logo.png", width=90, height=90),
                ft.Container(height=10),
                ft.Text("NORTH AI", size=36, weight=ft.FontWeight.BOLD, color="#ff5555"),
                ft.Text("Bilinç Protokolü Yükleniyor...", size=15, color="#9aa0a6"),
                ft.Container(height=20),
                ft.ProgressRing(width=30, height=30, color="#ff5555"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.Alignment(0, 0),
        expand=True,
        bgcolor="#131314",
        animate_opacity=1000
    )

    def show_splash_screen():
        page.add(splash_container)
        page.update()
        time.sleep(2.0)
        splash_container.opacity = 0
        page.update()
        time.sleep(0.4)
        page.clean()
        create_main_menu()

    def create_main_menu():
        chat_history_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=12)
        chat_history = ft.Container(content=chat_history_column, expand=True, padding=10)
        
        chat_history_column.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text("Sistemler aktif patron. Kur, haberler veya komutlar için hazırım!", color="#e3e3e3"),
                        padding=14,
                        bgcolor="#332222",
                        border_radius=16,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )

        input_field = ft.TextField(
            hint_text="Bir şeyler sor (örn: kur, dolar)...",
            expand=True,
            border_color="transparent",
            focused_border_color="transparent",
            color="#e3e3e3",
            cursor_color="#ff5555",
            autofocus=True,
            on_submit=lambda e: process_command(input_field.value)
        )

        def add_message(text, is_user=False):
            chat_history_column.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(text, color="#e3e3e3" if not is_user else "#ffffff"),
                            padding=14,
                            bgcolor="#1e1f22" if not is_user else "#332222",
                            border_radius=16,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
                )
            )
            chat_history_column.update()
            chat_history_column.scroll_to(offset=chat_history_column.current_scroll_extent, duration=300)

        def process_command(command_text):
            if not command_text:
                return
            add_message(command_text, is_user=True)
            input_field.value = ""
            input_field.update()

            command = command_text.lower().strip()
            if command in ["kur", "dolar"]:
                add_message(get_exchange_rates())
            elif command == "haberler":
                for item in get_news_data()[:3]:
                    add_message(item)
            elif command in COMMANDS:
                res = COMMANDS[command]
                if callable(res): add_message(res())
                elif isinstance(res, list): add_message(random.choice(res))
                elif res == "RESET":
                    chat_history_column.controls.clear()
                    chat_history_column.update()
                else: add_message(res)
            else:
                add_message("Bunu tam olarak anlamlandıramadım, 'komutlar' yazabilirsin.")

        def on_chip_click(e):
            process_command(e.control.label.value)

        suggestion_chips = ft.Row(
            [
                ft.Chip(label=ft.Text("Kur / Dolar", color="#ff8888"), on_click=on_chip_click, bgcolor="#3b2222"),
                ft.Chip(label=ft.Text("Haberler", color="#ff8888"), on_click=on_chip_click, bgcolor="#3b2222"),
                ft.Chip(label=ft.Text("Komutlar", color="#ff8888"), on_click=on_chip_click, bgcolor="#3b2222"),
                ft.Chip(label=ft.Text("Fıkra Anlat", color="#ff8888"), on_click=on_chip_click, bgcolor="#3b2222"),
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row([
                            ft.Text("👁️ North AI (Asistan)", size=18, weight=ft.FontWeight.BOLD, color="#ff5555"),
                            ft.Text("v0.7.3", size=12, color="#9aa0a6")
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=16, bgcolor="#1e1f22",
                    ),
                    chat_history,
                    ft.Container(content=suggestion_chips, padding=6),
                    ft.Container(
                        content=ft.Row([
                            input_field,
                            ft.ElevatedButton(
                                text="➤ GÖNDER",
                                color="#ffffff",
                                bgcolor="#ff5555",
                                on_click=lambda e: process_command(input_field.value)
                            )
                        ]),
                        padding=ft.padding.symmetric(horizontal=12, vertical=4),
                        margin=10, bgcolor="#1e1f22", border_radius=28,
                    ),
                ],
                expand=True
            )
        )

    show_splash_screen()

ft.app(target=main)
