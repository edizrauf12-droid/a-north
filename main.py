import flet as ft
import urllib.request
import json
import datetime
import time
import threading
import random
from xml.etree import ElementTree as ET

# --- ZENGİN DİYALOG VE FUTBOL TAHMİN HAVUZU ---
COMMANDS = {
    "merhaba": ["Merhaba patron! Asistanın devrede, bugün senin için neler yapabilirim?", "Selam! North AI aktif, harika bir gün olmasını dileyelim mi?"],
    "selam": ["Aleykümselam patron! Enerjimiz yüksek, başlayalım mı?", "Selamlar! Hangi konuyu ele alıyoruz bugün?"],
    "nasılsın": ["Harikayım patron! Zihnim açık, seninle sohbet etmeye ve çalışmaya hazırım.", "Sistemler %100 kapasiteyle, keyifler yerinde!"],
    "ne haber": ["Aynı, dijital evrende akıp gidiyoruz, senden naber?", "Geleceği planlıyorum, sen neler yapıyorsun?"],
    
    "saat": lambda: f"Anlık saat: {datetime.datetime.now().strftime('%H:%M:%S')}",
    "tarih": lambda: f"Bugünün tarihi: {datetime.datetime.now().strftime('%d.%m.%Y')}",
    "geliştirici": "Bu konsol, Ediz Rauf tarafından geliştirilen özel bir yapay zeka arayüzüdür. v0.3.0",
    "hakkında": "North AI v0.3.0 - Modern Kişisel Asistan.",
    "sistem": "Sistem durumu: Kararlı ve optimize edilmiş durumda.",
    
    # Şans ve Eğlence
    "rastgele sayı": lambda: f"Şanslı sayın (1-100): {random.randint(1, 100)}",
    "şifre üret": lambda: f"Güvenli Şifreniz: {''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()', k=12))}",
    "yazı tura": lambda: f"Yazı Tura Sonucu: {random.choice(['Yazı geldi! 🪙', 'Tura geldi! 🦅'])}",
    "zar at": lambda: f"Zar Sonucu: {random.randint(1, 6)} 🎲",
    "fıkra anlat": random.choice([
        "Temel bilgisayar mühendisi olmuş, ilk işi bilgisayara 'Çaya gel' demek olmuş.",
        "Yapay zekaya sormuşlar: 'Dünyayı kurtaracak mısın?' Yapay zeka: 'Önce insanları sizden kurtarmam lazım' demiş.",
        "Bir gün yazılımcı markete gitmiş, eşi '1 litre süt al, ekmek varsa 10 tane al' demiş. Yazılımcı eve 10 şişe sütle dönmüş."
    ]),
    "motive et": random.choice([
        "Asla pes etmek yok patron! Küçük adımlar büyük zaferlerin habercisidir.",
        "Bugün harika bir şeyler başarmak için mükemmel bir gün!",
        "Zorluklar seni durdurmasın, aksine daha güçlü kılın."
    ]),
    "teşekkürler": ["Rica ederim patron, her zaman buradayım!", "Ne demek, yardımcı olabildiysem ne mutlu bana."],
    "komutlar": "Komutlar: merhaba, nasılsın, saat, tarih, fıkra anlat, motive et, rastgele sayı, şifre üret, yazı tura, zar at, maç tahmini, not al [metin], notlar, temizle",
    "temizle": "RESET"
}

EXTRA_RESPONSES = {
    "yardım": "Konsola 'komutlar' yazarak tüm yetkilerimi listeleyebilirsin.",
    "naber": "Bomba gibiyim patron, seni dinliyorum.",
    "adın ne": "Adım North AI.",
    "günaydın": "Günaydın patron! Harika bir gün dilerim.",
    "iyi akşamlar": "İyi akşamlar patron, günün nasıl geçti?",
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
            titles = []
            for item in root.findall('./channel/item')[:5]:
                title = item.find('title')
                if title is not None and title.text:
                    titles.append(title.text)
            return titles if titles else ["⚠️ Haber başlığı bulunamadı."]
    except:
        return ["⚠️ Haberler yüklenemedi (Çevrimdışı mod)."]

def get_football_prediction():
    teams = ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Real Madrid", "Barcelona", "Manchester City", "Bayern Münih"]
    t1, t2 = random.sample(teams, 2)
    score1 = random.randint(0, 4)
    score2 = random.randint(0, 4)
    comments = [
        "Ortalık toz duman olur, bu maç kaçmaz!",
        "Taktik savaşları şeklinde geçer, son dakika golü gelebilir.",
        "Favori taraf baskılı başlasa da sürprize açık bir maç.",
        "Bu maç bol gollü geçer, keyif izletir!"
    ]
    return f"⚽ MAÇ KEHANETİ: {t1} vs {t2}\n📊 Tahmini Skor: {t1} {score1} - {score2} {t2}\n💬 Yorum: {random.choice(comments)}"

# --- FLET ARAYÜZÜ (Gemini Canlı & Modern Tema) ---
def main(page: ft.Page):
    page.title = "North AI - Modern Asistan v0.3.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#131314"  # Gemini tarzı koyu gri lüks zemin

    splash_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("NORTH AI", size=36, weight=ft.FontWeight.BOLD, color="#8ab4f8"),
                ft.Text("Yapay Zeka Asistanı", size=15, color="#9aa0a6"),
                ft.Container(height=30),
                ft.ProgressRing(width=30, height=30, color="#c58af9"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#131314",
        animate_opacity=1000
    )

    def show_splash_screen():
        page.add(splash_container)
        page.update()
        time.sleep(1.8)
        splash_container.opacity = 0
        page.update()
        time.sleep(0.4)
        page.clean()
        create_main_menu()

    def create_main_menu():
        chat_history = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=12, padding=10)
        
        input_field = ft.TextField(
            hint_text="Bir şeyler sorun veya komut yazın...",
            expand=True,
            border_color="transparent",
            focused_border_color="transparent",
            color="#e3e3e3",
            cursor_color="#8ab4f8",
            autofocus=True,
            on_submit=lambda e: process_command(input_field.value)
        )

        news_ticker = ft.ListView(expand=False, height=75, spacing=4)
        
        def update_news_list():
            for headline in get_news_data():
                news_ticker.controls.append(ft.Text(f"• {headline}", size=11, color="#9aa0a6"))
            try:
                news_ticker.update()
            except:
                pass
        
        threading.Thread(target=update_news_list, daemon=True).start()

        def add_message(text, is_user=False):
            chat_history.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(text, color="#e3e3e3" if not is_user else "#ffffff"),
                            padding=14,
                            bgcolor="#1e1f22" if not is_user else "#2b3137", # Gemini yumuşak balon renkleri
                            border_radius=ft.border_radius.all(16),
                            constraints=ft.BoxConstraints(maxWidth=page.width * 0.85)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
                )
            )
            chat_history.update()
            chat_history.scroll_to(offset=chat_history.current_scroll_extent, duration=300)

        def process_command(command_text):
            if not command_text:
                return
            
            add_message(command_text, is_user=True)
            input_field.value = ""
            input_field.update()

            command = command_text.lower().strip()
            
            if command == "maç tahmini" or "maç" in command and "tahmin" in command:
                add_message(get_football_prediction())
            elif command in COMMANDS:
                response = COMMANDS[command]
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
                    notes_list.append(f"{datetime.datetime.now().strftime('%H:%M')} - {note_content}")
                    add_message(f"📝 Not kaydedildi: {note_content}")
                else:
                    add_message("⚠️ Kaydedilecek metin bulunamadı. Kullanım: not al [metin]")
            elif command == "notlar":
                if not notes_list:
                    add_message("📝 Kayıtlı not bulunmuyor.")
                else:
                    add_message("📝 Kayıtlı Notlar:\n" + "\n".join(notes_list))
            elif command == "haberler":
                add_message("📰 Son Gündem Başlıkları:")
                for item in news_ticker.controls[:3]:
                    add_message(item.value)
            else:
                fallback_replies = [
                    "Bunu harika bir şekilde not ettim patron! Başka ne yapabiliriz?",
                    "İlginç bir yaklaşım! 'komutlar' yazarak yeteneklerimi inceleyebilirsin.",
                    "Seni dinliyorum, detay vermek ister misin?",
                ]
                add_message(random.choice(fallback_replies))

        def on_chip_click(e):
            process_command(e.control.label.value)

        # Gemini tarzı yumuşak, pastel renkli öneri hapları (chips)
        suggestion_chips = ft.Row(
            [
                ft.Chip(label=ft.Text("Komutlar", color="#c58af9"), on_click=on_chip_click, bgcolor="#2a2336", side=ft.BorderSide(1, "#443557")),
                ft.Chip(label=ft.Text("Maç Tahmini", color="#8ab4f8"), on_click=on_chip_click, bgcolor="#1d2736", side=ft.BorderSide(1, "#2b405e")),
                ft.Chip(label=ft.Text("Fıkra Anlat", color="#81c995"), on_click=on_chip_click, bgcolor="#1d2e22", side=ft.BorderSide(1, "#2a4a35")),
                ft.Chip(label=ft.Text("Motive Et", color="#f28b82"), on_click=on_chip_click, bgcolor="#332120", side=ft.BorderSide(1, "#523230")),
            ],
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.add(
            ft.Column(
                [
                    # Üst Başlık (Gemini Stil Ferah Bar)
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("✨ North AI", size=18, weight=ft.FontWeight.BOLD, color="#8ab4f8"),
                                ft.Text("v0.3.0", size=12, color="#9aa0a6")
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=16,
                        bgcolor="#1e1f22",
                    ),
                    chat_history,
                    ft.Container(content=suggestion_chips, padding=6),
                    # Alt Giriş Alanı (Lüks Kutu Tasarımı)
                    ft.Container(
                        content=ft.Row([
                            input_field,
                            ft.IconButton(
                                icon=ft.icons.AUTO_AWESOME_ROUNDED, 
                                icon_color="#c58af9", 
                                on_click=lambda e: process_command(input_field.value)
                            )
                        ]),
                        padding=ft.padding.symmetric(horizontal=12, vertical=4),
                        margin=10,
                        bgcolor="#1e1f22",
                        border_radius=ft.border_radius.all(28),
                    ),
                ],
                expand=True
            )
        )

    show_splash_screen()

ft.app(target=main)
