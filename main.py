import flet as ft

def main(page: ft.Page):
    page.title = "North AI - Endüstriyel Konsol"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#0B0F19"
    page.window_width = 480
    page.window_height = 750
    page.window_resizable = False

    def get_north_response(text):
        t = text.lower().strip()

        if any(op in t for op in ['+', '-', '*', '/', 'x']):
            try:
                clean_expr = t.replace('x', '*')
                result = eval(clean_expr)
                return f"Matematik İşlemi Sonucu: {clean_expr} = {result} 🧮"
            except:
                pass

        if "nasılsın" in t or "naber" in t:
            return "Sistemler tam kapasite çalışıyor, enerji doluyum! Sen nasılsın?"
        elif "adın ne" in t or "kimsin" in t:
            return "Ben North. Rauf Ediz Parlak tarafından geliştirilen yapay zeka asistanıyım."
        elif "kim yaptı" in t or "kim yarattı" in t:
            return "Beni Rauf Ediz Parlak tasarlayıp hayata geçirdi!"
        elif "geliştirme" in t or "durum ne" in t:
            return "Şu an aktif olarak geliştirme aşamasındayım. Yeni özellikler ve komutlar eklenmeye devam ediyor!"
        elif "şaka yap" in t or "fıkra" in t:
            return "Adamın biri matnaktan düşmüş, ölmemiş; mat-ematik! 😄"
        elif "motive et" in t or "moral" in t:
            return "Canını sıkma! Karşındaki tüm engelleri aşabilecek güçtesin. Hedefine odaklan ve devam et!"
        elif "ekip" in t or "katılmak" in t:
            return "Harika! Geliştirme ekibine katılmak için @raufedizparlak0 ile iletişime geçebilirsin."
        elif "merhaba" in t or "selam" in t:
            return "Selam! Sana bugün nasıl yardımcı olabilirim?"
        elif "ne yapabiliyorsun" in t or "yardım" in t:
            return "Genel sohbet edebilir, matematik işlemleri yapabilir, şakalar söyleyebilir ve sorularını yanıtlayabilirim!"
        else:
            return f"'{text}' ifadesini analiz ettim. Geliştirme aşamasında olduğum için bu konuyu henüz tam öğrenmedim ama her geçen gün gelişiyorum!"

    def show_menu(e=None):
        page.clean()
        
        title_content = ft.Column([
            ft.Text("NORTH OS", size=28, weight=ft.FontWeight.BOLD, color="#00E5FF"),
            ft.Text("Endüstriyel Yapay Zeka Konsolu v4.2", size=14, color="#8A99AD"),
            ft.Container(height=5),
            ft.Text("⚠️ Sistemler şu an GELİŞTİRME AŞAMASINDADIR", size=12, weight=ft.FontWeight.BOLD, color="#F59E0B")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)

        btn_chat = ft.ElevatedButton(
            text="🚀 NORTH AI (Sohbet Et)",
            color=ft.colors.WHITE,
            bgcolor="#1A233A",
            width=300,
            height=50,
            on_click=show_chat
        )
        btn_guide = ft.ElevatedButton(
            text="📖 Diyalog Rehberi",
            color=ft.colors.WHITE,
            bgcolor="#1A233A",
            width=300,
            height=50,
            on_click=show_guide
        )
        btn_about = ft.ElevatedButton(
            text="ℹ️ Hakkında & Geliştirici",
            color=ft.colors.WHITE,
            bgcolor="#1A233A",
            width=300,
            height=50,
            on_click=show_about
        )

        footer = ft.Container(
            content=ft.Text("📢 Geliştirme ekibi alımı mevcut: @raufedizparlak0", size=12, weight=ft.FontWeight.BOLD, color="#00E5FF", text_align=ft.TextAlign.CENTER),
            bgcolor="#111827",
            padding=12,
            alignment=ft.alignment.center,
            width=page.window_width
        )

        page.add(
            ft.Column([
                ft.Container(height=40),
                title_content,
                ft.Container(height=30),
                ft.Column([btn_chat, btn_guide, btn_about], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Expand(),
                footer
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        )
        page.update()

    def show_chat(e):
        page.clean()

        chat_list = ft.ListView(expand=True, spacing=10, padding=15, auto_scroll=True)

        def add_bubble(sender, message):
            if sender == "Sen":
                align = ft.CrossAxisAlignment.END
                bg_color = "#1F2937"
                text_color = ft.colors.WHITE
                prefix = "> "
            else:
                align = ft.CrossAxisAlignment.START
                bg_color = "#111827"
                text_color = "#00E5FF"
                prefix = "[North AI]: "

            chat_list.controls.append(
                ft.Container(
                    content=ft.Text(f"{prefix}{message}", color=text_color, size=14),
                    bgcolor=bg_color,
                    padding=10,
                    border_radius=8
                )
            )
            page.update()

        add_bubble("North", "Merhaba! Ben North. Şu an geliştirme aşamasındayım. Bana matematik işlemi sorabilir, sohbet edebilir veya komutları deneyebilirsin!")

        msg_input = ft.TextField(
            hint_text="Mesajınızı yazın...",
            hint_style=ft.TextStyle(color="#8A99AD"),
            border_color="#374151",
            focused_border_color="#00E5FF",
            bgcolor="#1F2937",
            color=ft.colors.WHITE,
            expand=True
        )

        def send_click(e):
            text = msg_input.value.strip()
            if not text:
                return
            add_bubble("Sen", text)
            msg_input.value = ""
            page.update()

            response = get_north_response(text)
            add_bubble("North", response)

        msg_input.on_submit = send_click
        send_btn = ft.ElevatedButton(text="Gönder", bgcolor="#00E5FF", color="#0B0F19", on_click=send_click)

        top_bar = ft.Row([
            ft.ElevatedButton("⬅ Geri", bgcolor="#1F2937", color=ft.colors.WHITE, on_click=show_menu),
            ft.Text("North AI - Akıllı Sohbet", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        ], alignment=ft.MainAxisAlignment.START)

        bottom_bar = ft.Row([msg_input, send_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                chat_list,
                ft.Container(content=bottom_bar, bgcolor="#111827", padding=10)
            ], expand=True)
        )
        page.update()

    def show_guide(e):
        page.clean()

        top_bar = ft.Row([
            ft.ElevatedButton("⬅ Geri", bgcolor="#1F2937", color=ft.colors.WHITE, on_click=show_menu),
            ft.Text("Diyalog ve Komut Rehberi", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        ])

        guide_content = ft.Column([
            ft.Text("📢 NORTH AI KULLANILABİLİR KOMUTLAR VE ÖZELLİKLER\n", weight=ft.FontWeight.BOLD, color="#00E5FF"),
            ft.Text("🔹 Matematik İşlemleri\nAçıklama: Sohbet ekranına doğrudan 50+50, 14*5 gibi işlemler yazarak hesaplatabilirsin.\n", color=ft.colors.WHITE),
            ft.Text("🔹 nasılsın / naber\nAçıklama: Sistemlerin durumu ve enerji seviyesi hakkında bilgi verir.\n", color=ft.colors.WHITE),
            ft.Text("🔹 adın ne / kimsin\nAçıklama: Asistanın kimliği hakkında bilgi sunar.\n", color=ft.colors.WHITE),
            ft.Text("🔹 kim yaptı?\nAçıklama: Projenin geliştiricisini gösterir.\n", color=ft.colors.WHITE),
            ft.Text("🔹 şaka yap / fıkra\nAçıklama: Eğlenceli bir matematik şakası patlatır.\n", color=ft.colors.WHITE),
            ft.Text("🔹 motive et\nAçıklama: Moral verici ve ilham dolu sözler söyler.\n", color=ft.colors.WHITE),
            ft.Text("🔹 ekip / katılmak\nAçıklama: Geliştirme ekibi iletişim bilgilerini paylaşır.", color=ft.colors.WHITE),
        ], scroll=ft.ScrollMode.AUTO, expand=True, padding=15)

        page.add(
            ft.Column([
                ft.Container(content=top_bar, bgcolor="#111827", padding=10),
                guide_content
            ], expand=True)
        )
        page.update()

    def show_about(e):
        page.clean()

        top_bar = ft.Row([
            ft.ElevatedButton("⬅ Geri", bgcolor="#1F2937", color=ft.colors.WHITE, on_click=show_menu),
            ft.Text("Hakkında & Geliştirici", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        ])

        about_content = ft.Container(
            content=ft.Column([
                ft.Text("North AI v4.2", size=22, weight=ft.FontWeight.BOLD, color="#00E5FF"),
                ft.Text("Geliştirici: Rauf Ediz Parlak", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Durum: ⚠️ Aktif Geliştirme Aşamasında", size=14, weight=ft.FontWeight.BOLD, color="#F59E0B"),
                ft.Text("Açıklama: Endüstriyel yapay zeka konsol altyapısı ve modüler diyalog motoru.", size=12, color="#9CA3AF"),
                ft.Container(height=10),
                ft.Text("📢 Ekip Alımı Aktif!\nKatılmak için:\nİletişim: @raufedizparlak0", size=13, weight=ft.FontWeight.BOLD, color="#3B82F6"),
            ], spacing=10),
            padding=20,
            bgcolor="#111827",
            border_radius=10,
            margin=20
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
        
