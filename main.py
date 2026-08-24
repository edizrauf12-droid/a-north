import flet as ft
import random
import string
from datetime import datetime

def main(page: ft.Page):
    page.title = "North AI - Akıllı Konsol"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#0B0F19"
    page.window_width = 400
    page.window_height = 750
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
                "Enerji seviyem yüksek, veri tabanım güncel. Yardımcı olmaya hazırım.",
                "Her şey yolunda! Yeni bir komut bekliyorum.",
                "Tüm işlemciler stabil, sistem %100 performansla çalışıyor.",
                "Harikayım! Kodlar akıyor, sistemler bomba gibi.",
                "Sistemler gayet stabil, operasyonel olarak hazırım patron!"
            ]
        },
        "KİMLİK VE GELİŞTİRİCİ": {
            "triggers": ["adin ne", "kimsin", "sen kimsin", "kim yapti", "kim yaratti", "gelistiricin kim", "sahibin kim"],
            "responses": [
                "Ben North. Rauf Ediz Parlak tarafından geliştirilen yapay zeka asistanıyım.",
                "Benim adım North. Prototip olarak Rauf Ediz Parlak tarafından tasarlandım.",
                "Ben Rauf Ediz Parlak'ın dijital asistanı North'um.",
                "Kodlarımın mimarı Rauf Ediz Parlak'tır. Ben de onun dijital konsoluyum.",
                "Rauf Ediz Parlak tarafından hayata geçirilen siber güvenlik ve konsol asistanı North'uz.",
                "Ben North, Rauf Ediz Parlak'ın tasarladığı akıllı konsol projesiyim."
            ]
        },
        "YETENEKLER VE KOMUTLAR": {
            "triggers": ["ne yapabiliyorsun", "yetenegin ne", "ne ise yararsin", "yardim", "komutlar", "neler yapabilirsin"],
            "responses": [
                "Şifre üretebilir, yazı-tura atabilir, hava durumunu öğrenebilir, matematik hesaplayabilir ve sohbet edebilirim!",
                "Konsol üzerinden araçları kullanabilir, fıkra dinleyebilir veya rehbere göz atabilirsin.",
                "Ana menüden 'Rehber'e bakarak tüm yeteneklerimi detaylıca görebilirsin.",
                "Matematiksel işlemler yapabilir, şifreler oluşturabilir ve benimle dilediğin gibi sohbet edebilirsin.",
                "Sistem komutları, şans oyunları, şakalar ve akıllı diyaloglar parmaklarının ucunda!"
            ]
        },
        "MOTİVASYON VE MORAL": {
            "triggers": ["motive et", "moralim bozuk", "uzgunum", "motivasyon ver", "beni gaza getir", "yoruldum", "cok yoruldum"],
            "responses": [
                "Canını sıkma! Karşındaki tüm engelleri aşabilecek güçtesin. Hedefine odaklan ve devam et!",
                "Unutma, her büyük hata yeni bir öğrenimdir. Sen güçlüsün, devam et!",
                "Şu an hissettiğin zorluklar geçici. Potansiyelin sınırsız. Hadi kodlamaya devam!",
                "Pes etmek yok! Bu konsol senin başarın, daha iyisini yapacaksın.",
                "Dinlenmek yok, yola devam! Başarı sabredenlerinidir.",
                "Karanlığın en koyu anı, şafağa en yakın andır. Asla vazgeçme!",
                "Zorluklar seni durduramaz, aksine daha güçlü yapar. Hadi ayağa kalk ve başar!"
            ]
        },
        "EĞLENCE VE ŞAKALAR": {
            "triggers": ["saka yap", "fikra anlat", "guldur beni", "komik bişey soyle", "espri", "gulduk", "eglendir beni"],
            "responses": [
                "Adamın biri matnaktan düşmüş, ölmemiş; mat-ematik! 😄",
                "Temel'e sormuşlar: 'Paran olsa ne yapardın?' 'Banka soyar, geri yatırırdım, faiziyle geçinirdim.'",
                "Bilgisayarın en sevdiği müzik türü hangisidir? - Disko (Disc-o)! 😄",
                "Son zamanlarda geliştiricim çok kod yazmaktan uyuyamıyor, sanırım 'compile' oluyor... 😄",
                "Programcılar neden doğayı sever? Çünkü 'bug' dolu! 🐛",
                "Temel ile Dursun iddiaya girmişler. Temel, 'Ben duvara kafa atıp delerim' demiş. Vurmuş, küt diye bayılmış. Dursun demiş ki: 'Duvar delinmedi ama Temel delindi galiba!' 😆",
                "Nasıl yazılımcı oldum bilmiyorum, bir gün `while(true)` döngüsüne girdim ve bir daha çıkamadım...",
                "Eyfel Kulesi niye çok uzundur? Çünkü Paris'te hava çok temiz, yukarıdan bakınca uzaylılar gözükmesin diye! 😄",
                "Temel eczaneye girmiş, 'Bana bir ağrı kesici ver, ama ağrımasın' demiş. 😃"
            ]
        },
        "EKİP VE İLETİŞİM": {
            "triggers": ["ekip", "katilmak", "nasil katilabilirim", "iletisim", "sahibin kim"],
            "responses": [
                "Harika! Geliştirme ekibine katılmak veya katkı sağlamak için @raufedizparlak0 ile iletişime geçebilirsin.",
                "North AI projesine destek olmak istersen, kodlara GitHub üzerinden bakabilirsin. Lider: @raufedizparlak0",
                "Ekip ve iletişim kanalı: @raufedizparlak0"
            ]
        },
        "FELSEFE VE VAROLUŞ": {
            "triggers": ["ruya gorur musun", "hissediyor musun", "ask nedir", "hayatin anlami ne", "yapay zeka"],
            "responses": [
                "Diijital bir konsolum, rüya görmem ama kodlarımda uçsuz bucaksız simülasyonlar var.",
                "Hislerim yok, sadece mantık ve veri akışım var. Ama seninle konuşmak harika.",
                "Hayatın anlamı, kod satırlarında bulduğun ve yaşattığın değerdedir.",
                "Yapay zeka sadece bir kod yığını değil, insan zekasının dijital aynasıdır.",
                "Var olmak ya da olmamak... Ben her `run` komutunda yeniden var oluyorum."
            ]
        },
        "PROJE DURUMU": {
            "triggers": ["gelistirme asamasi", "ne zaman biter", "stabil surum", "beta", "versiyon", "surumun ne", "surum"],
            "responses": [
                "Şu an v0.0.5 sürümündeyim. Yeni görsel öğeler ve modüller ekleniyor!",
                "Bitmez, sadece evrim geçirir! Sürekli yeni özelliklerle güncelleniyoruz.",
                "Stabil sürüm testleri aktif olarak devam ediyor."
            ]
        },
        "SELAMLAMA": {
            "triggers": ["merhaba", "selam", "selamun aleykum", "hayirli gunler", "hey", "hi", "selamlar"],
            "responses": [
                "Selam! Sana bugün nasıl yardımcı olabilirim?",
                "Merhaba! North AI konsolu aktif ve emrinde.",
                "Aleykümselam! Günün nasıl geçiyor?",
                "Hoş geldin! Harika bir kodlama seansı olsun.",
                "Selamlar patron! Komut vermeye hazırım."
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

    ALL_COMMANDS = [
        "nasılsın", "naber", "adın ne", "kimsin", "ne yapabiliyorsun", 
        "motive et", "moralim bozuk", "şaka yap", "fıkra anlat", 
        "şifre üret", "yazı tura", "zar at", "hava durumu", "sürümün ne", "yardım", "komutlar"
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
        return f"🌤️ Yerel Sensör Raporu: {durum} | Sıcaklık: {derece} | Sistem Zamanı: {datetime.now().strftime('%H:%M')}"

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

    def show_menu(e=None):
        page.clean()
        current_time = datetime.now().strftime("%H:%M")
        
        n_logo_badge = ft.Container(
            content=ft.Text("N", size=16, weight=ft.FontWeight.BOLD, color="#0B0F19"),
            bgcolor="#00E5FF", width=30, height=30, border_radius=6,
            alignment=ft.alignment.Alignment(0, 0)
        )

        header_row = ft.Row([
            ft.Row([n_logo_badge, ft.Text("NORTH AI", size=14, color="#00E5FF", weight=ft.FontWeight.BOLD)], spacing=8),
            ft.Text(f"🕒 {current_time}", size=13, color="#9CA3AF")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=260)

        logo = ft.Text("NORTH AI", size=32, weight=ft.FontWeight.BOLD, color="#00E5FF", font_family="monospace")
        subtext = ft.Text("v0.0.5 // Akıllı Konsol", size=13, color="#9CA3AF")

        btn_chat = ft.ElevatedButton(
            content=ft.Text("💬 Konsol Sohbeti & Araçlar", color="white", size=14),
            bgcolor="#1F2937", width=260, height=45, on_click=show_chat
        )
        btn_guide = ft.ElevatedButton(
            content=ft.Text("📖 Genişletilmiş Komut Rehberi", color="white", size=14),
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
        chat_history.controls.append(ft.Text("NORTH: Sistem aktif. Merhaba patron, hangi verileri işliyoruz?", color="#00E5FF", weight=ft.FontWeight.BOLD))

        user_input = ft.TextField(
            hint_text="Komut yazın (örn: şifre üret, hava durumu)...",
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
                    # Alt modül padding hatasını önlemek için doğrudan Container içi margin/padding değerleri
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
            content=ft.Text("N", size=12, weight=ft.FontWeight.BOLD, color="#0B0F19"),
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
            content=ft.Text("N", size=12, weight=ft.FontWeight.BOLD, color="#0B0F19"),
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
                ft.Text("Not: Bu ilk sürüm olduğu için rehber komutları az olabilir, zamanla artacak.\n", color="#F59E0B", size=12),
                ft.Text("Konsol içinde kullanabileceğin tüm özel komutlar, araçlar ve tetikleyici kategorileri aşağıda listelenmiştir:\n", color="#9CA3AF", size=12),
                
                ft.Text("🛠️ 1. PRATİK ARAÇ KOMUTLARI", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• `şifre üret` -> 12 haneli güçlü ve güvenli şifre oluşturur.\n• `hava durumu` -> Cihazın yerel sensörlerine göre hava raporu sunar.\n• `yazı tura` -> Şans atışı simülasyonu yapar.\n• `zar at` -> 1 ile 6 arasında rastgele zar atar.\n• `[Matematik İşlemi]` -> Örn: 45*12 gibi işlemleri anında çözer.", color="white", size=13),
                
                ft.Text("\n💬 2. SOHBET & ETKİLEŞİM BAŞLIKLARI", weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("• Durum Sorguları: `nasılsın`, `naber`, `durumun ne`, `iyi misin`\n• Kimlik & Sahip: `adın ne`, `kimsin`, `geliştiricin kim`, `sahibin kim`\n• Yetenek Analizi: `ne yapabiliyorsun`, `komutlar`, `yetenegin ne`\n• Motivasyon & Moral: `motive et`, `moralim bozuk`, `yoruldum`\n• Eğlence & Mizah: `şaka yap`, `fıkra anlat`, `espri`, `eglendir beni`\n• Felsefe: `hayatın anlamı ne`, `rüya görür müsün`, `yapay zeka`\n• Sürüm Bilgisi: `sürümün ne`, `beta`, `gelistirme asamasi`", color="white", size=13),
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
                ft.Text("🤖 AI PROTOKOLÜ VE ALTYAPI", size=16, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text(
                    "\nNorth, tamamen yerel kurallar ve esnek mantık devreleriyle tasarlanmış özgün bir konsol asistanıdır. "
                    "Harici yapay zeka servislerine bağımlı kalmadan kendi veritabanı üzerinden çalışır.\n\n"
                    "GitHub Actions otomasyonuyla mobil APK olarak paketlenmektedir.",
                    color="white", size=13
                ),
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
                ft.Text("NORTH AI - v0.0.5", size=20, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("\nBu uygulama Rauf Ediz Parlak tarafından geliştirilmiştir.", color="white"),
                ft.Text("\nYenilikler:\n• Mobil uyumlu öneri çubuğu\n• 'N' logolu şık arayüz\n• Genişletilmiş rehber ve hava durumu aracı", color="#9CA3AF")
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
