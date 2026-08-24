import flet as ft
import random
import string
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET

def main(page: ft.Page):
    page.title = "North AI - Akıllı Konsol v0.0.7"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#070913"
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False

    def normalize_text(text):
        t = text.lower().strip()
        replacements = {
            'ü': 'u', 'ö': 'o', 'ş': 's', 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'İ': 'i',
            'û': 'u', 'î': 'i', 'â': 'a'
        }
        for k, v in replacements.items():
            t = t.replace(k, v)
        return t

    NORTH_KNOWLEDGE = {
        "SİSTEM KONTROLLERİ": {
            "triggers": ["nasilsin", "naber", "durumun ne", "keyfin nasil", "iyi misin", "ne var ne yok", "sistem nasil"],
            "responses": [
                "Sistemler tam kapasite çalışıyor, enerji doluyum! Sen nasılsın?",
                "Çalışır durumdayım, veri akışı stabil. Senin durumun nedir?",
                "Sistemler gayet stabil, operasyonel olarak hazırım patron!"
            ]
        },
        "KİMLİK VE GELİŞTİRİCİ": {
            "triggers": ["adin ne", "kimsin", "sen kimsin", "kim yapti", "kim yaratti", "gelistiricin kim", "sahibin kim"],
            "responses": [
                "Ben North. Rauf Ediz Parlak tarafından geliştirilen yapay zeka asistanıyım.",
                "Benim adım North. Prototip olarak Rauf Ediz Parlak tarafından tasarlandım."
            ]
        },
        "YETENEKLER VE KOMUTLAR": {
            "triggers": ["ne yapabiliyorsun", "yetenegin ne", "ne ise yararsin", "yardim", "komutlar", "neler yapabilirsin"],
            "responses": [
                "Şifre üretebilir, yazı-tura atabilir, hava durumunu öğrenebilir, TRT haberlerini canlı listeleyebilir ve sohbet edebilirim!",
                "Sistem komutları, şans oyunları, canlı TRT haber akışı ve akıllı diyaloglar parmaklarının ucunda!"
            ]
        },
        "MOTİVASYON VE MORAL": {
            "triggers": ["motive et", "moralim bozuk", "uzgunum", "motivasyon ver", "beni gaza getir", "yoruldum", "cok yoruldum"],
            "responses": [
                "Canını sıkma! Karşındaki tüm engelleri aşabilecek güçtesin. Hedefine odaklan ve devam et!",
                "Dinlenmek yok, yola devam! Başarı sabredenlerinidir."
            ]
        },
        "PROJE DURUMU": {
            "triggers": ["gelistirme asamasi", "ne zaman biter", "stabil surum", "beta", "versiyon", "surumun ne", "surum"],
            "responses": [
                "Şu an v0.0.7 sürümündeyim. TRT Haber canlı veri API modülü entegre edildi!"
            ]
        },
        "SELAMLAMA": {
            "triggers": ["merhaba", "selam", "selamun aleykum", "hayirli gunler", "hey", "hi", "selamlar"],
            "responses": [
                "Selam! Sana bugün nasıl yardımcı olabilirim?",
                "Selamlar patron! Komut vermeye hazırım."
            ]
        }
    }

    ALL_COMMANDS = [
        "nasılsın", "naber", "adın ne", "kimsin", "ne yapabiliyorsun", 
        "motive et", "şifre üret", "yazı tura", "zar at", "hava durumu", "haberler", "sürüm", "yardım"
    ]

    def generate_password():
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(12))
        return f"🔐 Güvenli Şifre: {pwd}"

    def flip_coin():
        result = random.choice(["Yazı 🪙", "Tura 🪙"])
        return f"Atış Sonucu: {result}"

    def roll_dice():
        result = random.randint(1, 6)
        return f"Zar Sonucu: 🎲 {result}"

    def get_device_weather():
        current_hour = datetime.now().hour
        if 6 <= current_hour < 18:
            durum = "Güneşli ve Açık ☀️"
            derece = "24°C"
        else:
            durum = "Yıldızlı ve Serin 🌙"
            derece = "17°C"
        return f"🌤️ Yerel Sensör Raporu: {durum} | Sıcaklık: {derece}"

    # --- CANLI TRT HABER ÇEKME FONKSİYONU ---
    def get_real_trt_news():
        try:
            # TRT Haber'in resmi RSS veri akışına bağlanıyoruz
            url = "https://www.trthaber.com/manset_articles.rss"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                
            # Gelen XML verisini parçalıyoruz
            root = ET.fromstring(xml_data)
            news_list = []
            
            # En güncel ilk 3 haberi alıyoruz
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text
                news_list.append(f"• {title}")
                
            if news_list:
                return "\n".join(news_list)
            else:
                return "• Güncel haber bulunamadı."
        except Exception as e:
            return "• ⚠️ TRT Sunucusuna bağlanılamadı. Çevrimdışı!"

    def get_north_response(text):
        t = normalize_text(text)

        if "sifre uret" in t or "sifre olustur" in t:
            return generate_password()
        if "yazi tura" in t or "yazi-tura" in t:
            return flip_coin()
        if "zar at" in t:
            return roll_dice()
        if "hava durumu" in t or "hava" in t or "sicaklik" in t:
            return get_device_weather()
        
        # Kullanıcı sohbette "haberler" yazarsa da canlı veriyi çekip veriyor
        if "haber" in t or "trt" in t or "son dakika" in t:
            live_news = get_real_trt_news()
            return f"📰 CANLI TRT HABER AKIŞI:\n{live_news}"

        if any(op in t for op in ['+', '-', '*', '/', 'x']):
            try:
                clean_expr = text.replace('x', '*')
                result = eval(clean_expr)
                return f"🧮 Hesaplama Sonucu: {clean_expr} = {result}"
            except:
                pass
        
        for kategori_adi, veri in NORTH_KNOWLEDGE.items():
            if any(trigger in t for trigger in veri["triggers"]):
                return random.choice(veri["responses"])
        
        return f"'{text}' komutu anlaşılamadı. Detaylar için 'Rehber' sayfasına bakabilirsin."

    # --- ANA MENÜ ---
    def show_menu(e=None):
        page.clean()
        current_time = datetime.now().strftime("%H:%M")
        
        # Uygulama açılırken canlı haberleri çekiyoruz
        live_news_text = get_real_trt_news()
        
        n_logo_badge = ft.Container(
            content=ft.Text("N", size=16, weight=ft.FontWeight.BOLD, color="#070913"),
            bgcolor="#00E5FF", width=30, height=30, border_radius=6,
            alignment=ft.alignment.Alignment(0, 0)
        )

        header_row = ft.Row([
            ft.Row([n_logo_badge, ft.Text("NORTH AI", size=14, color="#00E5FF", weight=ft.FontWeight.BOLD)], spacing=8),
            ft.Text(f"🕒 {current_time}", size=13, color="#9CA3AF")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=300)

        logo_container = ft.Container(
            content=ft.Text("N", size=38, weight=ft.FontWeight.BOLD, color="#00E5FF"),
            alignment=ft.alignment.Alignment(0, 0),
            width=70, height=70,
            bgcolor="#111827",
            border=ft.border.all(2, "#00E5FF"),
            border_radius=18,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#00E5FF55")
        )

        logo_text = ft.Text("NORTH AI", size=24, weight=ft.FontWeight.BOLD, color="white", font_family="monospace")
        subtext = ft.Text("v0.0.7 // Canlı Veri API Aktif", size=11, color="#00E5FF")

        def create_menu_button(text, on_click_func):
            return ft.Container(
                content=ft.Row([
                    ft.Text(text, color="white", size=13, weight=ft.FontWeight.W_500)
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor="#111827",
                width=300, height=44,
                border_radius=10,
                border=ft.border.all(1, "#1F2937"),
                on_click=on_click_func,
                ink=True
            )

        btn_chat = create_menu_button("💬 Konsol Sohbeti & Araçlar", show_chat)
        btn_guide = create_menu_button("📖 Genişletilmiş Komut Rehberi", show_guide)
        btn_protocol = create_menu_button("🤖 AI Protokolü", show_protocol)
        btn_about = create_menu_button("ℹ️ Geliştirici Bilgisi", show_about)

        # --- CANLI TRT HABER ŞABLON KUTUSU ---
        news_widget = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("📰 TRT HABER MANŞETLERİ", size=11, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                    ft.Text("CANLI", size=9, color="#EF4444", weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(live_news_text, size=10, color="#E5E7EB") # Çekilen canlı haberler buraya yazdırılıyor
            ], spacing=4),
            bgcolor="#111827",
            width=300,
            padding=10,
            border_radius=10,
            border=ft.border.all(1, "#1F2937")
        )

        footer_text = ft.Text("North AI 2026 // Bağımsız Sistem", size=9, color="#4B5563")

        page.add(
            ft.Column([
                header_row,
                ft.Container(height=10),
                logo_container,
                ft.Container(height=6),
                logo_text, subtext,
                ft.Container(height=14),
                btn_chat,
                ft.Container(height=6),
                btn_guide,
                ft.Container(height=6),
                btn_protocol,
                ft.Container(height=6),
                btn_about,
                ft.Container(height=12),
                news_widget, 
                ft.Container(height=10),
                footer_text
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def show_chat(e):
        page.clean()
        chat_history = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
        chat_history.controls.append(ft.Text("NORTH: Sistem aktif. Merhaba patron, hangi verileri işliyoruz?", color="#00E5FF", weight=ft.FontWeight.BOLD))

        user_input = ft.TextField(
            hint_text="Komut yazın (örn: haberler)...",
            hint_style=ft.TextStyle(color="#6B7280"),
            color="white", bgcolor="#1F2937", border_radius=8, expand=True
        )

        suggestions_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=5)

        def update_suggestions(e):
            query = user_input.value.lower().strip()
            suggestions_row.controls.clear()
            if query:
                matches = [cmd for cmd in ALL_COMMANDS if cmd.startswith(query)]
                for match in matches[:5]:
                    chip = ft.Container(
                        content=ft.Text(match, color="#00E5FF", size=11, weight=ft.FontWeight.BOLD),
                        bgcolor="#1F2937", padding=8,
                        border_radius=6,
                        on_click=lambda _, m=match: select_suggestion(m)
                    )
                    suggestions_row.controls.append(chip)
            page.update()

        def select_suggestion(selected_text):
            user_input.value = selected_text
            suggestions_row.controls.clear()
            page.update()

        user_input.on_change = update_suggestions

        def send_click(e):
            if not user_input.value.strip():
                return
            query = user_input.value
            chat_history.controls.append(ft.Text(f">> {query}", color="#E5E7EB", weight=ft.FontWeight.BOLD))
            response = get_north_response(query)
            chat_history.controls.append(ft.Text(f"NORTH: {response}", color="#00E5FF"))
            user_input.value = ""
            suggestions_row.controls.clear()
            page.update()

        send_btn = ft.ElevatedButton(
            content=ft.Text("GÖNDER", color="#00E5FF", weight=ft.FontWeight.BOLD),
            bgcolor="#1F2937", on_click=send_click
        )

        mini_logo = ft.Container(
            content=ft.Text("N", size=12, weight=ft.FontWeight.BOLD, color="#070913"),
            bgcolor="#00E5FF", width=24, height=24, border_radius=4, alignment=ft.alignment.Alignment(0, 0)
        )

        top_bar = ft.Row([
            ft.Row([
                ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
                mini_logo
            ], spacing=8),
            ft.Text("Terminal Konsolu", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                chat_history,
                ft.Container(content=suggestions_row, padding=5),
                ft.Container(
                    content=ft.Row([user_input, send_btn]),
                    bgcolor="#111827", padding=10
                )
            ], expand=True)
        )
        page.update()

    def show_guide(e):
        page.clean()
        mini_logo = ft.Container(
            content=ft.Text("N", size=12, weight=ft.FontWeight.BOLD, color="#070913"),
            bgcolor="#00E5FF", width=24, height=24, border_radius=4, alignment=ft.alignment.Alignment(0, 0)
        )
        top_bar = ft.Row([
            ft.Row([
                ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
                mini_logo
            ], spacing=8),
            ft.Text("Genişletilmiş Rehber", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        guide_content = ft.Container(
            content=ft.Column([
                ft.Text("📖 NORTH KONSOL KAPSAMLI REHBERİ", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("🛠️ 1. PRATİK ARAÇ KOMUTLARI", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• `haberler` -> TRT Haber'den canlı güncel manşetleri çeker.\n• `şifre üret` -> Güçlü şifre oluşturur.\n• `hava durumu` -> Yerel hava raporu sunar.\n• `yazı tura` / `zar at` -> Şans atışı simülasyonu yapar.", color="white", size=13),
            ], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )

        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), guide_content], expand=True))
        page.update()

    def show_protocol(e):
        page.clean()
        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("AI Protokolü", color="white", weight=ft.FontWeight.BOLD)
        ])
        protocol_content = ft.Container(
            content=ft.Column([
                ft.Text("🤖 AI PROTOKOLÜ VE ALTYAPI", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nNorth, canlı veri API'leri (TRT News RSS vb.) kullanarak dış dünyayla etkileşime giren bağımsız bir sistemdir.", color="white", size=13),
            ], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )
        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), protocol_content], expand=True))
        page.update()

    def show_about(e):
        page.clean()
        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("Geliştirici Bilgisi", color="white", weight=ft.FontWeight.BOLD)
        ])
        about_content = ft.Container(
            content=ft.Column([
                ft.Text("NORTH AI - v0.0.7", size=20, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nBu uygulama Rauf Ediz Parlak tarafından geliştirilmiştir.", color="white"),
                ft.Text("\nYenilikler:\n• CANLI TRT Haber API entegrasyonu (urllib & XML parsing)\n• Geliştirilmiş menü şablonu", color="#9CA3AF")
            ]), padding=20
        )
        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), about_content], expand=True))
        page.update()

    show_menu()

ft.app(target=main)
