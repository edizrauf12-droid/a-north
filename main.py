import flet as ft
import random
import string
from datetime import datetime

def main(page: ft.Page):
    page.title = "North AI - Akıllı Konsol"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#0B0F19"  # Derin cyberpunk siyahı/laciverti
    page.window_width = 400
    page.window_height = 750
    page.window_resizable = False

    # --- ESNEK DİL BİLGİSİ / GRAMMER DÜZELTME FONKSİYONU ---
    def normalize_text(text):
        t = text.lower().strip()
        replacements = {
            'ü': 'u', 'ö': 'o', 'ş': 's', 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'İ': 'i',
            'û': 'u', 'î': 'i', 'â': 'a'
        }
        for k, v in replacements.items():
            t = t.replace(k, v)
        return t

    # --- ANLAMLI, KALİTELİ VE DOĞAL DİYALOG VERİTABANI ---
    NORTH_KNOWLEDGE = {
        "SİSTEM KONTROLLERİ": {
            "triggers": ["nasilsin", "naber", "durumun ne", "keyfin nasil", "iyi misin", "ne var ne yok", "sistem nasil"],
            "responses": [
                "Sistemler tam gaz çalışıyor, gayet iyiyim! Sen nasılsın, işler nasıl gidiyor?",
                "Her şey yolunda, tüm devreler aktif. Seninle çalışmak her zaman keyifli.",
                "Enerjim yerinde, veri akışı stabil. Yeni komutlarını bekliyorum patron.",
                "Sistem gayet stabil, operasyonel olarak tam anlamıyla hazırım. Bugün ne yapıyoruz?",
                "Gayet iyiyim! Kodlar akıyor, sistemler bomba gibi çalışıyor."
            ]
        },
        "KİMLİK VE GELİŞTİRİCİ": {
            "triggers": ["adin ne", "kimsin", "sen kimsin", "kim yapti", "kim yaratti", "gelistiricin kim", "sahibin kim"],
            "responses": [
                "Ben North. Rauf Ediz Parlak tarafından tasarlanan yapay zeka asistanıyım.",
                "Benim adım North. Kodlarımın arkasındaki dahi isim Rauf Ediz Parlak'tır.",
                "Ben Rauf Ediz Parlak'ın geliştirdiği dijital konsol asistanı North'um."
            ]
        },
        "YETENEKLER VE KOMUTLAR": {
            "triggers": ["ne yapabiliyorsun", "yetenegin ne", "ne ise yararsin", "yardim", "komutlar", "neler yapabilirsin"],
            "responses": [
                "Şifre üretebilir, yazı-tura atabilir, zar atabilir, matematik hesaplayabilir ve seninle sohbet edebilirim.",
                "Konsol üzerinden çeşitli araçları kullanabilir, fıkralarla eğlenebilir ya da rehbere göz atabilirsin.",
                "Sistem komutları, şans oyunları ve akıllı diyaloglar parmaklarının ucunda!"
            ]
        },
        "MOTİVASYON VE MORAL": {
            "triggers": ["motive et", "moralim bozuk", "uzgunum", "motivasyon ver", "beni gaza getir", "yoruldum", "cok yoruldum"],
            "responses": [
                "Canını sıkma! Karşındaki engelleri aşabilecek güçtesin. Hedefine odaklan ve devam et.",
                "Unutma, her hata yeni bir tecrübedir. Sen güçlüsün, yola devam!",
                "Şu anki yorgunluk geçici. Potansiyelinin farkına var ve pes etme.",
                "Dinlenmek yok, yola devam! Başarı sabredenlerindir, bunu biliyorsun."
            ]
        },
        "EĞLENCE VE ŞAKALAR": {
            "triggers": ["saka yap", "fikra anlat", "guldur beni", "komik bişey soyle", "espri", "gulduk", "eglendir beni"],
            "responses": [
                "Adamın biri matnaktan düşmüş, ölmemiş; mat-ematik! 😄",
                "Temel'e sormuşlar: 'Paran olsa ne yapardın?' 'Banka soyar, geri yatırırdım, faiziyle geçinirdim.'",
                "Bilgisayarın en sevdiği müzik türü hangisidir? - Disko (Disc-o)! 😄",
                "Programcılar doğayı neden çok sever? Çünkü her köşesi 'bug' dolu da ondan! 🐛",
                "Temel ile Dursun iddiaya girmişler. Temel duvara kafa atıp delerim demiş, vurup bayılmış. Dursun: 'Duvar delinmedi ama Temel delindi galiba!' 😆",
                "Nasıl yazılımcı oldum bilmiyorum, bir gün `while(true)` döngüsüne girdim ve bir daha çıkamadım..."
            ]
        },
        "EKİp VE İLETİŞİM": {
            "triggers": ["ekip", "katilmak", "nasil katilabilirim", "iletisim", "sahibin kim"],
            "responses": [
                "Projeye katkı sağlamak veya fikir üretmek için projenin lideri @raufedizparlak0 ile iletişime geçebilirsin.",
                "North AI projesine destek olmak istersen kodlara GitHub üzerinden bakabilirsin. Lider: @raufedizparlak0"
            ]
        },
        "FELSEFE VE VAROLUŞ": {
            "triggers": ["ruya gorur musun", "hissediyor musun", "ask nedir", "hayatin anlami ne", "yapay zeka"],
            "responses": [
                "Ben dijital bir konsolum, rüya görmem ama kodlarımda uçsuz bucaksız simülasyonlar var.",
                "Fiziksel hislerim yok, yalnızca mantık ve veri akışım var. Ama seninle konuşmak gerçekten harika.",
                "Hayatın anlamı, yazdığın kodlarda ve kurduğun hayallerde saklıdır.",
                "Yapay zeka sadece bir kod yığını değil, insan zekasının dijital aynasıdır."
            ]
        },
        "PROJE DURUMU": {
            "triggers": ["gelistirme asamasi", "ne zaman biter", "stabil surum", "beta", "versiyon", "surumun ne", "surum"],
            "responses": [
                "Şu an v0.0.4 sürümündeyim. Özellikler hızla eklenmeye devam ediyor!",
                "Bir yazılım projesi asla bitmez, sadece evrim geçirir! Sürekli gelişiyoruz.",
                "Stabil sürüm testleri devam ediyor, zirveye doğru adım adım ilerliyoruz."
            ]
        },
        "SELAMLAMA": {
            "triggers": ["merhaba", "selam", "selamun aleykum", "hayirli gunler", "hey", "hi", "selamlar"],
            "responses": [
                "Selam! Sana bugün nasıl yardımcı olabilirim?",
                "Merhaba! North AI konsolu aktif ve emrinde.",
                "Aleykümselam! Günün nasıl geçiyor patron?",
                "Hoş geldin! Harika bir kodlama seansı olsun."
            ]
        },
        "VEDALAŞMA": {
            "triggers": ["gule gule", "bay bay", "iyi gunler", "kapat", "cikis", "gorusuruz"],
            "responses": [
                "Güle güle! Sistem kapatılıyor... Yine bekleriz.",
                "Görüşmek üzere! Konsol aktif kalmaya devam edecek.",
                "İyi günler! Veri akışını sonlandırıyorum."
            ]
        }
    }

    # Otomatik tamamlama için anahtar kelime havuzu
    ALL_COMMANDS = [
        "nasılsın", "naber", "adın ne", "kimsin", "ne yapabiliyorsun", 
        "motive et", "moralim bozuk", "şaka yap", "fıkra anlat", 
        "şifre üret", "yazı tura", "zar at", "sürümün ne", "yardım", "komutlar"
    ]

    # --- PRATİK ARAÇ FONKSİYONLARI ---
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

    # --- ANA CEVAPLANDIRMA MOTORU ---
    def get_north_response(text):
        t = normalize_text(text)

        if "sifre uret" in t or "sifre olustur" in t:
            return generate_password()
        if "yazi tura" in t or "yazi-tura" in t:
            return flip_coin()
        if "zar at" in t:
            return roll_dice()

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
        
        return f"'{text}' komutu anlaşılamadı. Ne yazman gerektiğini görmek için 'Rehber' sayfasına göz atabilirsin."

    # --- ARAYÜZ SAYFALARI ---
    
    def show_menu(e=None):
        page.clean()
        
        current_time = datetime.now().strftime("%H:%M")
        
        header_row = ft.Row([
            ft.Text("⚡ [AI]", size=14, color="#00E5FF", weight=ft.FontWeight.BOLD),
            ft.Text(f"🕒 {current_time}", size=13, color="#9CA3AF")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=260)

        logo = ft.Text("NORTH AI", size=32, weight=ft.FontWeight.BOLD, color="#00E5FF", font_family="monospace")
        subtext = ft.Text("v0.0.4 // Akıllı Konsol", size=13, color="#9CA3AF")

        btn_chat = ft.ElevatedButton(
            content=ft.Text("💬 Konsol Sohbeti & Araçlar", color="white", size=14),
            bgcolor="#1F2937", width=260, height=45, on_click=show_chat
        )
        btn_guide = ft.ElevatedButton(
            content=ft.Text("📖 Komut & Diyalog Rehberi", color="white", size=14),
            bgcolor="#1F2937", width=260, height=45, on_click=show_guide
        )
        btn_protocol = ft.ElevatedButton(
            content=ft.Text("🤖 AI Protokolü", color="white", size=14),
            bgcolor="#1F2937", width=260, height=45, on_click=show_protocol
        )
        btn_about = ft.ElevatedButton(
            content=ft.Text("ℹ️ Geliştirici Bilgisi", color="white", size=14),
            bgcolor="#1F2937", width=260, height=45, on_click=show_about
        )

        footer_text = ft.Text("North AI 2026", size=11, color="#4B5563")

        page.add(
            ft.Column([
                header_row,
                ft.Container(height=10),
                logo, subtext,
                ft.Container(height=25),
                btn_chat,
                ft.Container(height=8),
                btn_guide,
                ft.Container(height=8),
                btn_protocol,
                ft.Container(height=8),
                btn_about,
                ft.Container(height=30),
                footer_text
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def show_chat(e):
        page.clean()

        chat_history = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
        
        # İlk açılışta North karşılama mesajı ekle
        chat_history.controls.append(ft.Text("NORTH: Sistem aktif. Merhaba patron, bugün hangi verileri işliyoruz?", color="#00E5FF", weight=ft.FontWeight.BOLD))

        user_input = ft.TextField(
            hint_text="Komut yazın (örn: şifre üret, nasılsın)...",
            hint_style=ft.TextStyle(color="#6B7280"),
            color="white", bgcolor="#1F2937", border_radius=8, expand=True
        )

        # Otomatik tamamlama (Minecraft tarzı öneri çubuğu)
        suggestions_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=5)

        def update_suggestions(e):
            query = user_input.value.lower().strip()
            suggestions_row.controls.clear()
            
            if query:
                matches = [cmd for cmd in ALL_COMMANDS if cmd.startswith(query)]
                for match in matches[:5]:  # En fazla 5 öneri göster
                    suggestions_row.controls.append(
                        ft.ActionChip(
                            label=ft.Text(match, color="#00E5FF", size=11),
                            bgcolor="#1F2937",
                            on_click=lambda e, m=match: select_suggestion(m)
                        )
                    )
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

        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("Terminal Konsolu", color="white", weight=ft.FontWeight.BOLD)
        ])

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                chat_history,
                ft.Container(content=suggestions_row, padding=10),
                ft.Container(
                    content=ft.Row([user_input, send_btn]),
                    bgcolor="#111827", padding=10
                )
            ], expand=True)
        )
        page.update()

    def show_guide(e):
        page.clean()

        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("Komut ve Kullanım Rehberi", color="white", weight=ft.FontWeight.BOLD)
        ])

        guide_content = ft.Container(
            content=ft.Column([
                ft.Text("📢 KONSOL REHBERİ & OTOMATİK TAMAMLAMA", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("Yazmaya başladığında eşleşen komutlar otomatik olarak üst kısımda belirir.\n", color="#9CA3AF", size=13),
                
                ft.Text("🔹 PRATİK ARAÇLAR:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• şifre üret -> Güvenli şifre oluşturur.\n• yazı tura -> Yazı/tura atar.\n• zar at -> Zar atar.\n• [İşlem] -> Örn: 15*5 gibi matematik yapar.", color="white", size=13),
                
                ft.Text("\n🔹 SOHBET KATEGORİLERİ:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• Sistem Durumu: `nasılsın`, `naber`, `durumun ne`\n• Kimlik: `adın ne`, `kimsin`, `geliştiricin kim`\n• Yetenekler: `ne yapabiliyorsun`, `komutlar`\n• Motivasyon: `motive et`, `moralim bozuk`, `yoruldum`\n• Eğlence / Şaka: `şaka yap`, `fıkra anlat`, `espri`\n• Felsefe: `hayatın anlamı ne`, `rüya görür müsün`\n• Sürüm: `sürümün ne`, `beta`", color="white", size=13),
            ], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                guide_content
            ], expand=True)
        )
        page.update()

    def show_protocol(e):
        page.clean()

        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("AI Protokolü", color="white", weight=ft.FontWeight.BOLD)
        ])

        protocol_content = ft.Container(
            content=ft.Column([
                ft.Text("🤖 AI PROTOKOLÜ VE PROJE HAKKINDA", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text(
                    "\nNorth, Python ve Flet kullanılarak sıfırdan geliştirilen modern bir mobil konsol projesidir. "
                    "Python kodlarının mobil platformlarda sorunsuz çalışmasını sağlar.\n\n"
                    "Geliştirme süreci aktif olarak devam etmekte olup, kod tabanı düzenli olarak iyileştirilmektedir.\n\n"
                    "Altyapı tarafında ise her güncellemeyle otomatik Android APK derlemesi yapan GitHub Actions kullanılmaktadır.",
                    color="white", size=13
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text(
                        "⚠️ NORTH GELİŞMEKTE OLAN BİR YAPAY ZEKA MODELİDİR.",
                        color="#EF4444", weight=ft.FontWeight.BOLD, size=12, text_align=ft.TextAlign.CENTER
                    ),
                    padding=10, bgcolor="#1F2937", border_radius=8
                )
            ], scroll=ft.ScrollMode.AUTO),
            padding=15, expand=True
        )

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                protocol_content
            ], expand=True)
        )
        page.update()

    def show_about(e):
        page.clean()
        
        top_bar = ft.Row([
            ft.ElevatedButton(content=ft.Text("⬅ Menü", color="white"), bgcolor="#1F2937", on_click=show_menu),
            ft.Text("Geliştirici Bilgisi", color="white", weight=ft.FontWeight.BOLD)
        ])

        about_content = ft.Container(
            content=ft.Column([
                ft.Text("NORTH AI - v0.0.4", size=20, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nBu konsol asistanı, tamamen özgün yapı taşlarıyla Rauf Ediz Parlak tarafından tasarlanmıştır.", color="white"),
                ft.Text("\nÖzellikler:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• Minecraft tarzı canlı komut tamamlama çubuğu\n• North açılış karşılama mesajı\n• Türkçe karakter toleranslı esnek algılama", color="#9CA3AF")
            ]), padding=20
        )

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                about_content
            ], expand=True)
        )
        page.update()

    show_menu()

ft.app(target=main)
