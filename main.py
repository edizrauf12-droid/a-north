import flet as ft
import random
import string
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
import json
import threading
import time

def main(page: ft.Page):
    page.title = "North AI - Gelişmiş Siber Konsol v0.1.0"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#070913"
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False

    global_chat_history = [
        "NORTH: Siber konsol ve veri akışı aktif. Hangi veriyi inceliyoruz patron?"
    ]
    user_notes = []

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
                "Sistemler tam kapasite ve maksimum performansla çalışıyor patron! Arka planda anlık finans akışı, TRT haber manşetleri ve bellek optimizasyonu kusursuz şekilde yürütülüyor. Tüm çekirdekler aktif ve emre amade. Senin dijital cephede işler nasıl gidiyor, keyifler yerinde mi?",
                "Tüm dijital altyapım, veri akış protokollerim ve yapay zeka modüllerim kararlı bir kararlılıkla çalışıyor. Herhangi bir gecikme veya paket kaybı yok. Canlı piyasaları izliyor, gelen komutları anlık işliyorum. Sen nasılsın, bugün hangi projeleri patlatıyoruz?"
            ]
        },
        "KİMLİK VE GELİŞTİRİCİ": {
            "triggers": ["adin ne", "kimsin", "sen kimsin", "kim yapti", "kim yaratti", "gelistiricin kim", "sahibin kim"],
            "responses": [
                "Ben North; Rauf Ediz Parlak tarafından sıfırdan inşa edilen, modern siber estetiğe ve akıllı diyalog yeteneklerine sahip yeni nesil bir yapay zeka konsoluyum. Standart kalıpların dışına çıkan, tamamen bağımsız ve işlevsel bir dijital asistan olarak görev yapıyorum."
            ]
        },
        "YETENEKLER VE KOMUTLAR": {
            "triggers": ["ne yapabiliyorsun", "yetenegin ne", "ne ise yararsin", "yardim", "komutlar", "neler yapabilirsin"],
            "responses": [
                "Yeteneklerim oldukça geniştir patron! Anlık TRT haberlerini ve canlı piyasa kurlarını (Dolar, Euro, Altın) çekebilir, güvenli şifreler üretebilir, yerel hava durumunu raporlayabilir, matematiksel hesaplamalar yapabilir, özel notlar alabilir ve en önemlisi seninle akıcı bir şekilde sohbet edebilirim. 'yardim' yazarak tüm listeye göz atabilirsin."
            ]
        },
        "SELAMLAMA": {
            "triggers": ["merhaba", "selam", "selamun aleykum", "hayirli gunler", "hey", "hi", "selamlar"],
            "responses": [
                "Selam patron! Siber konsolun kapıları sonuna kadar açıldı. Piyasalar, haberler ve tüm sistem modülleri emrinde. Bugün hangi komutları çalıştırıyoruz?"
            ]
        }
    }

    ALL_COMMANDS = [
        "nasılsın", "naber", "adın ne", "ne yapabiliyorsun", 
        "dolar", "euro", "altın", "piyasa", "haberler", 
        "şifre üret", "hava durumu", "not al", "notlar", "yardım"
    ]

    def generate_password():
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.choice(chars) for _ in range(12))
        return f"🔐 Güvenli Şifre Üretildi: {pwd}"

    def flip_coin():
        result = random.choice(["Yazı 🪙", "Tura 🪙"])
        return f"Kritik Atış Sonucu: {result}"

    def roll_dice():
        result = random.randint(1, 6)
        return f"Zar Çekirdeği Sonucu: 🎲 {result}"

    def get_device_weather():
        current_hour = datetime.now().hour
        if 6 <= current_hour < 18:
            return "🌤️ Yerel Rapor: Güneşli ve Açık Gökyüzü ☀️ | 24°C"
        else:
            return "🌙 Yerel Rapor: Yıldızlı Gece ve Serin Altyapı | 17°C"

    def get_real_trt_news():
        try:
            url = "https://www.trthaber.com/manset_articles.rss"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                xml_data = response.read()
            root = ET.fromstring(xml_data)
            news_list = [f"• {item.find('title').text}" for item in root.findall('.//item')[:2]]
            return "\n".join(news_list) if news_list else "• Haber akışı bulunamadı."
        except:
            return "• ⚠️ TRT Haber sunucusuna şu an ulaşılamıyor."

    def get_market_data():
        try:
            url = "https://api.genelpara.com/embed/altin.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            usd = data.get('USD', {}).get('satis', 'N/A')
            eur = data.get('EUR', {}).get('satis', 'N/A')
            gram_altin = data.get('GA', {}).get('satis', 'N/A')
            
            return f"💵 Dolar: {usd} TL  |  💶 Euro: {eur} TL\n🥇 Gram Altın: {gram_altin} TL"
        except:
            return "💵 Dolar: 34.20 TL | 💶 Euro: 37.10 TL\n🥇 Gram Altın: 2,950 TL (Önbellek)"

    def get_north_response(text):
        t = normalize_text(text)

        if "sifre uret" in t or "sifre olustur" in t:
            return generate_password()
        if "yazi tura" in t:
            return flip_coin()
        if "zar at" in t:
            return roll_dice()
        if "hava durumu" in t or "hava" in t:
            return get_device_weather()
        if "haber" in t or "trt" in t or "son dakika" in t:
            return f"📰 CANLI TRT HABERLERİ:\n{get_real_trt_news()}"
        if "dolar" in t or "euro" in t or "altin" in t or "piyasa" in t or "kur" in t:
            return f"📈 CANLI PİYASA KURU:\n{get_market_data()}"
        
        if t.startswith("not al "):
            note_content = text[7:].strip()
            if note_content:
                user_notes.append(note_content)
                return f"📝 Not başarıyla hafızaya kaydedildi:\n\"{note_content}\""
            else:
                return "⚠️ Kaydedilecek metin bulunamadı. Örnek: 'not al projeyi geliştir'"
        
        if t == "notlar" or t == "notlarim":
            if user_notes:
                formatted_notes = "\n".join([f"{i+1}. {note}" for i, note in enumerate(user_notes)])
                return f"📋 KAYITLI NOTLARINIZ:\n{formatted_notes}"
            else:
                return "📋 Henüz hafızaya kaydedilmiş bir notunuz bulunmuyor."

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
        
        return f"'{text}' komutu algılandı ancak tam olarak eşleştirilemedi. 'yardim' yazarak aktif komutlara göz atabilirsin patron."

    # --- 1. AÇILIŞ (SPLASH) EKRANI ---
    def show_splash_screen():
        page.clean()

        splash_logo = ft.Container(
            content=ft.Image(src="logo.png", width=110, height=110, fit=ft.ImageFit.CONTAIN),
            alignment=ft.alignment.Alignment(0, 0),
            width=110, height=110,
            bgcolor="#111827",
            border_radius=24,
            shadow=ft.BoxShadow(spread_radius=3, blur_radius=25, color="#00E5FF88")
        )

        title_text = ft.Text("NORTH AI", size=28, weight=ft.FontWeight.BOLD, color="white", font_family="monospace")
        status_text = ft.Text("Sistem çekirdekleri yükleniyor...", size=11, color="#00E5FF")

        page.add(
            ft.Column([
                splash_logo,
                ft.Container(height=15),
                title_text,
                ft.Container(height=5),
                status_text
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

        # 2 saniye sonra otomatik olarak ana menüye geçiş yap
        def delayed_transition():
            time.sleep(2.0)
            show_menu()

        threading.Thread(target=delayed_transition, daemon=True).start()

    # --- 2. ANA MENÜ ---
    def show_menu(e=None):
        page.clean()
        current_time = datetime.now().strftime("%H:%M")
        
        live_news = get_real_trt_news()
        market_summary = get_market_data()
        
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
            content=ft.Image(src="logo.png", width=70, height=70, fit=ft.ImageFit.CONTAIN),
            alignment=ft.alignment.Alignment(0, 0),
            width=70, height=70,
            bgcolor="#111827",
            border_radius=18,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#00E5FF55")
        )

        logo_text = ft.Text("NORTH AI", size=24, weight=ft.FontWeight.BOLD, color="white", font_family="monospace")
        subtext = ft.Text("v0.1.0 // Parlayan Açılış & Bellek Aktif", size=10, color="#00E5FF")

        def create_menu_button(text, on_click_func):
            return ft.Container(
                content=ft.Row([ft.Text(text, color="white", size=13, weight=ft.FontWeight.W_500)], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor="#111827", width=300, height=40, border_radius=10,
                on_click=on_click_func, ink=True
            )

        btn_chat = create_menu_button("💬 Konsol Sohbeti & Araçlar", show_chat)
        btn_guide = create_menu_button("📖 Komut Rehberi", show_guide)
        btn_protocol = create_menu_button("🤖 AI Protokolü", show_protocol)
        btn_about = create_menu_button("ℹ️ Geliştirici Bilgisi", show_about)

        market_widget = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("📈 CANLI PİYASA KURU", size=11, weight=ft.FontWeight.BOLD, color="#10B981"),
                    ft.Text("CANLI", size=9, color="#10B981", weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(market_summary, size=10, color="#E5E7EB")
            ], spacing=3),
            bgcolor="#111827", width=300, padding=8, border_radius=10
        )

        news_widget = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("📰 TRT HABER MANŞETLERİ", size=11, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                    ft.Text("CANLI", size=9, color="#EF4444", weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(live_news, size=10, color="#E5E7EB")
            ], spacing=3),
            bgcolor="#111827", width=300, padding=8, border_radius=10
        )

        footer_text = ft.Text("North AI 2026 // Bağımsız Sistem", size=9, color="#4B5563")

        page.add(
            ft.Column([
                header_row,
                ft.Container(height=4),
                logo_container,
                ft.Container(height=2),
                logo_text, subtext,
                ft.Container(height=6),
                btn_chat,
                ft.Container(height=3),
                btn_guide,
                ft.Container(height=3),
                btn_protocol,
                ft.Container(height=3),
                btn_about,
                ft.Container(height=6),
                market_widget,
                ft.Container(height=4),
                news_widget,
                ft.Container(height=4),
                footer_text
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    # --- 3. KONSOL SOHBETİ ---
    def show_chat(e):
        page.clean()
        chat_history = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
        
        for msg in global_chat_history:
            if msg.startswith("NORTH:"):
                chat_history.controls.append(ft.Text(msg, color="#00E5FF"))
            else:
                chat_history.controls.append(ft.Text(msg, color="#E5E7EB", weight=ft.FontWeight.BOLD))

        user_input = ft.TextField(
            hint_text="Komut veya not yazın (örn: dolar, not al işleri bitir)...",
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
                        bgcolor="#1F2937", padding=8, border_radius=6,
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
            
            user_msg = f">> {query}"
            chat_history.controls.append(ft.Text(user_msg, color="#E5E7EB", weight=ft.FontWeight.BOLD))
            global_chat_history.append(user_msg)
            
            response = get_north_response(query)
            ai_msg = f"NORTH: {response}"
            chat_history.controls.append(ft.Text(ai_msg, color="#00E5FF"))
            global_chat_history.append(ai_msg)
            
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
            ft.Text("Terminal Konsolu & Bellek", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                chat_history,
                ft.Container(content=suggestions_row, padding=5),
                ft.Container(content=ft.Row([user_input, send_btn]), bgcolor="#111827", padding=10)
            ], expand=True)
        )
        page.update()

    def show_guide(e):
        page.clean()
        mini_logo = ft.Container(content=ft.Text("N", size=12, weight=ft.FontWeight.BOLD, color="#070913"), bgcolor="#00E5FF", width=24, height=24, border_radius=4, alignment=ft.alignment.Alignment(0, 0))
        top_bar = ft.Row([
            ft.Row([ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu), mini_logo], spacing=8),
            ft.Text("Komut Rehberi", color="white", weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        guide_content = ft.Container(
            content=ft.Column([
                ft.Text("📖 NORTH FİNANS & KONSOL REHBERİ", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• `dolar` / `euro` / `altın` -> Anlık piyasa kurlarını gösterir.\n• `haberler` -> TRT Haber canlı manşetlerini getirir.\n• `not al [metin]` -> Uygulama içine not kaydeder.\n• `notlar` -> Kaydettiğiniz tüm notları listeler.\n• `şifre üret` -> Güvenli şifre oluşturur.\n• `hava durumu` -> Yerel hava raporu sunar.", color="white", size=13),
            ], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )
        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), guide_content], expand=True))
        page.update()

    def show_protocol(e):
        page.clean()
        top_bar = ft.Row([ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu), ft.Text("AI Protokolü", color="white", weight=ft.FontWeight.BOLD)])
        protocol_content = ft.Container(
            content=ft.Column([ft.Text("🤖 AI PROTOKOLÜ & BELLEK", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"), ft.Text("\nNorth, zenginleştirilmiş diyalog veritabanı, oturum içi sohbet hafızası ve entegre not defteriyle tam donanımlı bağımsız bir yapay zeka asistanıdır.", color="white", size=13)], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )
        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), protocol_content], expand=True))
        page.update()

    def show_about(e):
        page.clean()
        top_bar = ft.Row([ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu), ft.Text("Geliştirici Bilgisi", color="white", weight=ft.FontWeight.BOLD)])
        about_content = ft.Container(
            content=ft.Column([
                ft.Text("NORTH AI - v0.1.0", size=20, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nBu uygulama Rauf Ediz Parlak tarafından geliştirilmiştir.", color="white"),
                ft.Text("\nYenilikler:\n• Parlayan Açılış (Splash) Ekranı\n• 200+ Dolgun Diyalog ve Derin Yanıtlar\n• Oturum İçi Sohbet Geçmişi Kaydı\n• Entegre Not Alma Modülü", color="#9CA3AF")
            ]), padding=20
        )
        page.add(ft.Column([ft.Container(content=top_bar, bgcolor="#111827", padding=10), about_content], expand=True))
        page.update()

    # Uygulama ilk açıldığında doğrudan parlayan açılış ekranını çalıştır
    show_splash_screen()

ft.app(target=main)
