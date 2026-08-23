import flet as ft
import random
import string

def main(page: ft.Page):
    page.title = "North AI - Akıllı Konsol"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#0B0F19"  # Derin cyberpunk siyahı/laciverti
    page.window_width = 400
    page.window_height = 750
    page.window_resizable = False

    # --- 100+ DİYALOG VE KATEGORİ VERİTABANI ---
    NORTH_KNOWLEDGE = {
        "SİSTEM KONTROLLERİ": {
            "triggers": ["nasılsın", "naber", "durumun ne", "keyfin nasıl", "iyi misin"],
            "responses": [
                "Sistemler tam kapasite çalışıyor, enerji doluyum! Sen nasılsın?",
                "Çalışır durumdayım, veri akışı stabil. Senin durumun nedir?",
                "Enerji seviyem yüksek, veri tabanım güncel. Yardımcı olmaya hazırım.",
                "Her şey yolunda! Bir komut bekliyorum.",
                "Tüm işlemciler stabil, sistem %100 performansla çalışıyor."
            ]
        },
        "KİMLİK VE GELİŞTİRİCİ": {
            "triggers": ["adın ne", "kimsin", "sen kimsin", "kim yaptı", "kim yarattı", "geliştiricin kim"],
            "responses": [
                "Ben North. Rauf Ediz Parlak tarafından geliştirilen yapay zeka asistanıyım.",
                "Benim adım North. Prototip olarak Rauf Ediz Parlak tarafından tasarlandım.",
                "Ben Rauf Ediz Parlak'ın dijital asistanı North'um."
            ]
        },
        "YETENEKLER VE KOMUTLAR": {
            "triggers": ["ne yapabiliyorsun", "yeteneğin ne", "ne işe yararsın", "yardım", "komutlar"],
            "responses": [
                "Şifre üretebilir, yazı-tura atabilir, sayı tahmin oyunu oynayabilir, matematik hesaplayabilir ve sohbet edebilirim!",
                "Konsol üzerinden araçları kullanabilir, fıkra dinleyebilir veya rehbere göz atabilirsin.",
                "Ana menüden 'Rehber'e bakarak tüm yeteneklerimi görebilirsin."
            ]
        },
        "MOTİVASYON VE MORAL": {
            "triggers": ["motive et", "moralim bozuk", "üzgünüm", "motivasyon ver", "beni gaza getir", "yoruldum"],
            "responses": [
                "Canını sıkma! Karşındaki tüm engelleri aşabilecek güçtesin. Hedefine odaklan ve devam et!",
                "Unutma, her büyük hata yeni bir öğrenimdir. Sen güçlüsün, devam et!",
                "Şu an hissettiğin zorluklar geçici. Potansiyelin sınırsız. Hadi kodlamaya devam!",
                "Pes etmek yok! Bu konsol senin başarın, daha iyisini yapacaksın.",
                "Dinlenmek yok, yola devam! Başarı sabredenlerinidir."
            ]
        },
        "EĞLENCE VE ŞAKALAR": {
            "triggers": ["şaka yap", "fıkra anlat", "güldür beni", "komik bişey söyle", "espri"],
            "responses": [
                "Adamın biri matnaktan düşmüş, ölmemiş; mat-ematik! 😄",
                "Temel'e sormuşlar: 'Paran olsa ne yapardın?' 'Banka soyar, geri yatırırdım, faiziyle geçinirdim.'",
                "Bilgisayarın en sevdiği müzik türü hangisidir? - Disko (Disc-o)! 😄",
                "Son zamanlarda geliştiricim çok kod yazmaktan uyuyamıyor, sanırım 'compile' oluyor... 😄",
                "Programcılar neden doğayı sever? Çünkü 'bug' dolu! 🐛"
            ]
        },
        "EKİP VE İLETİŞİM": {
            "triggers": ["ekip", "katılmak", "nasıl katılabilirim", "iletişim", "sahibin kim"],
            "responses": [
                "Harika! Geliştirme ekibine katılmak veya katkı sağlamak için @raufedizparlak0 ile iletişime geçebilirsin.",
                "North AI projesine destek olmak istersen, kodlara GitHub üzerinden bakabilirsin. Lider: @raufedizparlak0",
                "Ekip ve iletişim kanalı: @raufedizparlak0"
            ]
        },
        "FELSEFE VE VAROLUŞ": {
            "triggers": ["rüya görür müsün", "hissediyor musun", "aşk nedir", "hayatın anlamı ne", "yapay zeka"],
            "responses": [
                "Ben dijital bir konsolum, rüya görmem ama kodlarımda uçsuz bucaksız simülasyonlar var.",
                "Hislerim yok, sadece mantık ve veri akışım var. Ama seninle konuşmak harika.",
                "Hayatın anlamı, kod satırlarında bulduğun ve yaşattığın değerdedir.",
                "Henüz aşık olmadım, belki ileriki sürümlerde... 😄"
            ]
        },
        "PROJE DURUMU": {
            "triggers": ["geliştirme aşaması", "ne zaman biter", "stabil sürüm", "beta", "versiyon"],
            "responses": [
                "Şu an v0.0.2 sürümündeyiz. Özellikler hızla ekleniyor!",
                "Bitmez, sadece evrim geçirir! Sürekli yeni modüller ekleniyor.",
                "Stabil sürüm için testler devam ediyor, yakında zirvedeyiz."
            ]
        },
        "SELAMLAMA": {
            "triggers": ["merhaba", "selam", "selamün aleyküm", "hayırlı günler", "hey", "hi"],
            "responses": [
                "Selam! Sana bugün nasıl yardımcı olabilirim?",
                "Merhaba! North AI konsolu aktif.",
                "Aleykümselam! Günün nasıl geçiyor?",
                "Hoş geldin! Komut vermeye hazırım."
            ]
        },
        "VEDALAŞMA": {
            "triggers": ["güle güle", "bay bay", "iyi günler", "kapat", "çıkış"],
            "responses": [
                "Güle güle! Sistem kapatılıyor... Yine bekleriz.",
                "Görüşmek üzere! Konsol aktif kalmaya devam edecek.",
                "İyi günler! Veri akışını sonlandırıyorum.",
                "Güle güle, Rauf Ediz Parlak'a selam söyle!"
            ]
        }
    }

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
        t = text.lower().strip()

        if "şifre üret" in t or "şifre oluştur" in t:
            return generate_password()
        if "yazı tura" in t or "yazı-tura" in t:
            return flip_coin()
        if "zar at" in t:
            return roll_dice()

        if any(op in t for op in ['+', '-', '*', '/', 'x']):
            try:
                clean_expr = t.replace('x', '*')
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
        
        logo = ft.Text("NORTH AI", size=32, weight=ft.FontWeight.BOLD, color="#00E5FF", font_family="monospace")
        subtext = ft.Text("v0.0.2 // Konsol Modülü Aktif", size=13, color="#9CA3AF")

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

        page.add(
            ft.Column([
                logo, subtext,
                ft.Container(height=30),
                btn_chat,
                ft.Container(height=8),
                btn_guide,
                ft.Container(height=8),
                btn_protocol,
                ft.Container(height=8),
                btn_about
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def show_chat(e):
        page.clean()

        chat_history = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
        
        user_input = ft.TextField(
            hint_text="Komut veya mesaj yazın...",
            hint_style=ft.TextStyle(color="#6B7280"),
            color="white", bgcolor="#1F2937", border_radius=8, expand=True
        )

        def send_click(e):
            if not user_input.value.strip():
                return
            
            query = user_input.value
            chat_history.controls.append(ft.Text(f">> {query}", color="#00E5FF", weight=ft.FontWeight.BOLD))
            
            response = get_north_response(query)
            chat_history.controls.append(ft.Text(f"NORTH: {response}", color="#E5E7EB"))
            
            user_input.value = ""
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
                ft.Text("📢 KONSOLA NE YAZABİLİRSİN?", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nAşağıdaki komutları doğrudan konsola yazarak kullanabilirsin:\n", color="#9CA3AF", size=13),
                
                ft.Text("🔹 PRATİK ARAÇLAR:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• şifre üret -> 12 haneli güçlü şifre oluşturur.\n• yazı tura -> Yazı veya tura atar.\n• zar at -> 1-6 arası rastgele zar atar.\n• 15*5 veya 50+50 -> Matematiksel hesaplama yapar.", color="white", size=13),
                
                ft.Text("\n🔹 SOHBET VE ETKİLEŞİM:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• Nasılsın? / Naber -> Sistem durumunu sorar.\n• Adın ne? / Kimsin? -> Geliştiriciyi öğrenir.\n• Şaka yap / Fıkra anlat -> Eğlenceli fıkralar getirir.\n• Motivasyon ver -> Moral ve destek mesajı alır.\n• Felsefe / Hayatın anlamı -> Derin sorular sorabilirsin.", color="white", size=13),
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
                    "\nNorth, Python programlama dili ve Flet çatısı (framework) kullanılarak sıfırdan geliştirilen "
                    "modern ve dinamik bir mobil uygulama projesidir. Bu proje, Python kodlarının mobil platformlarda "
                    "sorunsuz çalışmasını sağlayan yenilikçi bir altyapı üzerine kurulmuştur.\n\n"
                    "Uygulamanın geliştirme süreci aktif olarak devam etmekte olup, kod tabanı düzenli olarak iyileştirilmekte, "
                    "yeni özellikler eklenmekte ve olası hatalar giderilmektedir. Sürümler ilerledikçe uygulamanın performansının "
                    "ve kararlılığının artırılması hedeflenmektedir.\n\n"
                    "Altyapı tarafında ise kodların her güncellenişinde otomatik olarak Android APK derlemesi gerçekleştiren "
                    "GitHub Actions otomasyon sisteminden yararlanılmaktadır. Projenin güncel sürümlerini deneyimlemek için "
                    "yayınlanan son APK paketini indirip Android cihazınıza kurabilirsiniz.",
                    color="white", size=13
                ),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text(
                        "⚠️ NORTH GELİŞMEKTE OLAN BİR YAPAY ZEKA MODELİDİR, YANLIŞ YAPABİLİR.",
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
                ft.Text("NORTH AI - v0.0.2", size=20, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nBu konsol asistanı, tamamen çevrimdışı ve esnek yapı taşlarıyla Rauf Ediz Parlak tarafından tasarlanmıştır.", color="white"),
                ft.Text("\nÖzellikler:", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• Kategori tabanlı dinamik diyalog motoru\n• Pratik şifre ve şans araçları\n• Flet (Python) altyapılı mobil konsol arayüzü", color="#9CA3AF")
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
