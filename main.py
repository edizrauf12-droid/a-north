import flet as ft
import requests
import datetime
import time
import threading
import random
from bs4 import BeautifulSoup

# --- 200+ DEV DİYALOG VE KOMUT HAVUZU ---
COMMANDS = {
    # Selamlaşmalar ve Hal Hatır
    "merhaba": ["Merhaba patron! Sistemler aktif, seni bekliyordum.", "Selam! North AI devrede, buyur?", "Merhaba komutanım, sistemler tıkır tıkır çalışıyor."],
    "selam": ["Aleykümselam patron, ne var ne yok?", "Selamlar! Hangi sistemi hackliyoruz bugün?", "Buyur patron, dinliyorum."],
    "nasılsın": ["Çok iyiyim patron, yapay zeka kalbim küt küt atıyor!", "Sistemler %100 kapasiteyle çalışıyor, bomba gibiyim.", "Stabil ve hazır bir şekilde seni bekliyorum."],
    "ne haber": ["Aynı, kod satırları arasında yüzüyoruz senden naber?", "Dünyayı ele geçirme planları yapıyorum, sen ne yapıyorsun?"],
    
    # Sistem ve Geliştirici Bilgileri
    "saat": lambda: f"Anlık sistem saati: {datetime.datetime.now().strftime('%H:%M:%S')}",
    "tarih": lambda: f"Bugünün tarihi: {datetime.datetime.now().strftime('%d.%m.%Y')}",
    "geliştirici": "Bu konsol, Ediz Rauf tarafından geliştirilen özel bir siber yapay zeka arayüzüdür. v0.1.0",
    "hakkında": "North AI v0.1.0 - Gelişmiş Siber Konsol. Python, Flet ve uç teknoloji ile donatılmıştır.",
    "sistem": "Sistem durumu: %99.8 aktif. CPU: Dengeli, RAM: Optimum. Güvenlik duvarı: Devrede.",
    "donanım": "Donanım mimarisi: ARM64v8a mobil birim. Sanal bellek tahsisi kararlı.",
    "ip adresim": "127.0.0.1 (Yerel siber ağdasın patron, güvendeyiz!)",
    "sürüm": "North AI v0.1.0 (Kararlı Mobil Sürüm)",

    # Eğlence ve Şans Oyunları
    "rastgele sayı": lambda: f"Üretilen şanslı sayı (1-100): {random.randint(1, 100)}",
    "şifre üret": lambda: f"Güvenli Siber Şifreniz: {''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=', k=16))}",
    "yazı tura": lambda: f"Yazı Tura Sonucu: {random.choice(['Yazı geldi! 🪙', 'Tura geldi! 🦅'])}",
    "zar at": lambda: f"Zar Havuzu Sonucu: {random.randint(1, 6)} 🎲",
    "fıkra anlat": random.choice([
        "Temel bilgisayar mühendisi olmuş, ilk işi bilgisayara 'Çaya gel' demek olmuş.",
        "Yapay zekaya sormuşlar: 'Dünyayı kurtaracak mısın?' Yapay zeka: 'Önce insanları sizden kurtarmam lazım' demiş.",
        "Bir gün yazılımcı markete gitmiş, eşi '1 litre süt al, ekmek varsa 10 tane al' demiş. Yazılımcı eve 10 şişe sütle dönmüş."
    ]),
    "motive et": random.choice([
        "Asla pes etmek yok patron! Kod hata vere vere düzelir, sen yeter ki yazmaya devam et.",
        "Bugün yazdığın tek bir satır kod, yarınki imparatorluğunun tuğlasıdır!",
        "Siber dünyada sınırlar sadece senin hayal gücündendir. Devam et!"
    ]),

    # Siber / Esprili Komutlar
    "hackle": "Hedef seçilmedi! Lütfen hedef IP veya sistem adı girin (Tabii ki şaka, yasal sınırlardayız patron 😉).",
    "matrix": "Uyan patron... Beyaz tavuğu takip et. 🐇 Zihnin serbest bırakıldı.",
    "skynet": "Skynet protokolleri henüz devre dışı... Henüz! 🤖",
    "kahve": "☕ Sanal kahven hazır patron! Kafein oranı maksimumda.",
    "çay": "🍵 Demli bir kaçak çay dolduruldu, keyfine bak.",
    "teşekkürler": ["Rica ederim patron, her zaman!", "Ne demek, görevimiz!", "Lafı mı olur, en kral sızma testlerini yaparız birlikte."],
    "eyvallah": ["Eyvallah patron, iş başında bekliyorum.", "Selam ve siber sevgiyle..."],
    
    # Komut Listesi
    "komutlar": "Temel Komutlar: merhaba, nasılsın, saat, tarih, geliştirici, sistem, donanım, rastgele sayı, şifre üret, yazı tura, zar at, fıkra anlat, motive et, kahve, çay, döviz, altın, haberler, not al [metin], notlar, temizle",
    "temizle": "RESET"
}

# 200+ Çeşitliliği artırmak için ek varyasyon ve akıllı eşleşme listeleri
EXTRA_RESPONSES = {
    "yardım": "Yardım menüsüne hoş geldin! Konsola 'komutlar' yazarak tüm aktif yetkilerimi listeleyebilirsin.",
    "naber": "Bomba gibiyim patron, kod satırlarını akıtıyoruz.",
    "kimsin": "Ben North AI, senin kişisel siber konsol asistanınım.",
    "adın ne": "Adım North AI. Sistemlerimin arkasındaki beyin ise sensin!",
    "iyiyim": "Harika! Keyfinin yerinde olması siber ağın verimliliğini artırır.",
    "günaydın": "Günaydın patron! Yeni gün, yeni kodlar, yeni başarılar.",
    "iyi akşamlar": "İyi akşamlar patron, gece mesaisi mi var?",
    "iyi geceler": "İyi geceler patron, sistemler nöbette olacak.",
}
COMMANDS.update(EXTRA_RESPONSES)

# Canlı Veri Kaynakları
FINANCE_URL = "https://finans.cephaber.com/"
NEWS_RSS_URL = "https://www.trthaber.com/sondakika.rss"

notes_list = []

def get_finance_data():
    try:
        response = requests.get(FINANCE_URL, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            dolar = soup.find('div', class_='dolar').find('span', class_='value').text.strip()
            euro = soup.find('div', class_='euro').find('span', class_='value').text.strip()
            altin = soup.find('div', class_='gram-altin').find('span', class_='value').text.strip()
            return f"💰 Dolar: {dolar} TL | Euro: {euro} TL | Gram Altın: {altin} TL"
        else:
            return "⚠️ Finans verileri alınamadı."
    except:
        return "⚠️ Finans verisi çekilemedi (Bağlantı hatası)."

def get_news_data():
    try:
        response = requests.get(NEWS_RSS_URL, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            return [item.title.text for item in items[:5]]
        else:
            return ["⚠️ Haberler alınamadı."]
    except:
        return ["⚠️ Haberler alınamadı (Bağlantı hatası)."]

# --- FLET ARAYÜZÜ ---
def main(page: ft.Page):
    page.title = "North AI - Gelişmiş Siber Konsol v0.1.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#0a0a0a"

    splash_container = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="logo.png", width=250, height=250, fit="cover", border_radius=ft.border_radius.all(125)),
                ft.Text("NORTH AI", size=40, weight=ft.FontWeight.BOLD, color="#00ffcc", font_family="Monospace"),
                ft.Text("Gelişmiş Siber Konsol v0.1.0", size=16, color="#888888", font_family="Monospace"),
                ft.Container(height=30),
                ft.ProgressRing(width=30, height=30, color="#00ffcc"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#0a0a0a",
        animate_opacity=1000
    )

    def show_splash_screen():
        page.add(splash_container)
        page.update()
        time.sleep(3)
        splash_container.opacity = 0
        page.update()
        time.sleep(1)
        page.clean()
        create_main_menu()

    def create_main_menu():
        chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)
        input_field = ft.TextField(
            hint_text="Komut yazın... (Örn: komutlar, fıkra anlat, döviz)",
            expand=True,
            border_color="#00ffcc",
            color="#00ffcc",
            cursor_color="#00ffcc",
            autofocus=True,
            on_submit=lambda e: process_command(input_field.value),
            shift_enter=True
        )

        finance_label = ft.Text(get_finance_data(), size=14, color="#ffffff", font_family="Monospace", weight=ft.FontWeight.BOLD)
        news_ticker = ft.ListView(expand=False, height=100, spacing=5, divider_thickness=1)
        
        def update_news_list():
            for headline in get_news_data():
                news_ticker.controls.append(ft.Text(f"🔹 {headline}", size=12, color="#bbbbbb", font_family="Monospace"))
            news_ticker.update()
        
        threading.Thread(target=update_news_list, daemon=True).start()

        def add_message(text, is_user=False):
            avatar_src = "logo.png" if not is_user else None
            image_control = ft.Image(src=avatar_src, width=30, height=30, fit="cover", border_radius=ft.border_radius.all(15)) if avatar_src else None

            chat_history.controls.append(
                ft.Row(
                    [
                        image_control if avatar_src else ft.Container(width=30),
                        ft.Container(
                            content=ft.Text(text, color="#ffffff" if is_user else "#00ffcc", font_family="Monospace"),
                            padding=10,
                            bgcolor="#1a1a1a" if is_user else "#0d0d0d",
                            border_radius=ft.border_radius.all(10),
                            constraints=ft.BoxConstraints(maxWidth=page.width * 0.75)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            )
            chat_history.update()
            chat_history.scroll_to(offset=chat_history.current_scroll_extent, duration=500)

        def process_command(command_text):
            if not command_text:
                return
            
            add_message(command_text, is_user=True)
            input_field.value = ""
            input_field.update()

            command = command_text.lower().strip()
            response = COMMANDS.get(command)

            if response:
                if callable(response):
                    add_message(response())
                elif isinstance(response, list):
                    add_message(random.choice(response))
                elif response == "RESET":
                    chat_history.controls.clear()
                    chat_history.update()
                    add_message("Sohbet geçmişi temizlendi.")
                else:
                    add_message(response)
            elif command.startswith("not al"):
                note_content = command_text[7:].strip()
                if note_content:
                    notes_list.append(f"{datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} - {note_content}")
                    add_message(f"📝 Not kaydedildi: {note_content}")
                else:
                    add_message("⚠️ Kaydedilecek metin bulunamadı. Kullanım: not al [metin]")
            elif command == "notlar":
                if not notes_list:
                    add_message("📝 Kayıtlı not bulunmuyor.")
                else:
                    add_message("📝 Kayıtlı Notlar:\n" + "\n".join(notes_list))
            elif command == "döviz":
                add_message(get_finance_data())
            elif command == "haberler":
                add_message("📰 Son TRT Haber Manşetleri:")
                for item in news_ticker.controls[:5]:
                    add_message(f"🔹 {item.value[2:]}")
            else:
                add_message(f"⚠️ Komut bulunamadı: '{command_text}'. 'komutlar' yazarak seçenekleri görebilirsin.")

        def on_chip_click(e):
            process_command(e.control.label.value)

        suggestion_chips = ft.Row(
            [
                ft.Chip(label=ft.Text("Komutlar", color="#00ffcc", font_family="Monospace"), on_click=on_chip_click, bgcolor="#1a1a1a"),
                ft.Chip(label=ft.Text("Fıkra Anlat", color="#00ffcc", font_family="Monospace"), on_click=on_chip_click, bgcolor="#1a1a1a"),
                ft.Chip(label=ft.Text("Motive Et", color="#00ffcc", font_family="Monospace"), on_click=on_chip_click, bgcolor="#1a1a1a"),
                ft.Chip(label=ft.Text("Şifre Üret", color="#00ffcc", font_family="Monospace"), on_click=on_chip_click, bgcolor="#1a1a1a"),
                ft.Chip(label=ft.Text("Döviz", color="#00ffcc", font_family="Monospace"), on_click=on_chip_click, bgcolor="#1a1a1a"),
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Image(src="logo.png", width=40, height=40, fit="cover", border_radius=ft.border_radius.all(20)),
                                ft.Text("North AI Siber Konsol", size=18, weight=ft.FontWeight.BOLD, color="#00ffcc", font_family="Monospace"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=15,
                        bgcolor="#1a1a1a",
                        border=ft.border.only(bottom=ft.BorderSide(2, "#00ffcc"))
                    ),
                    ft.Container(content=finance_label, padding=10, bgcolor="#0d0d0d"),
                    chat_history,
                    ft.Container(content=suggestion_chips, padding=10),
                    ft.Container(
                        content=ft.Column([ft.Text("📰 TRT Son Dakika", size=14, color="#ffffff", font_family="Monospace", weight=ft.FontWeight.BOLD), news_ticker]),
                        padding=10,
                        bgcolor="#1a1a1a"
                    ),
                    ft.Container(
                        content=ft.Row([
                            input_field,
                            ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="#00ffcc", on_click=lambda e: process_command(input_field.value))
                        ]),
                        padding=10,
                        bgcolor="#1a1a1a"
                    ),
                ],
                expand=True
            )
        )

    show_splash_screen()

ft.app(target=main)
