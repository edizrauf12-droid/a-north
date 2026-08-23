import tkinter as tk
from tkinter import scrolledtext
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

class NorthAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("North AI - Endüstriyel Konsol")
        self.root.geometry("480x750")
        self.root.config(bg="#0B0F19")
        self.root.resizable(False, False)

        self.create_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # 1. ANA MENÜ
    def create_menu(self):
        self.clear_window()

        title_frame = tk.Frame(self.root, bg="#0B0F19")
        title_frame.pack(pady=40)

        tk.Label(title_frame, text="NORTH OS", font=("Segoe UI", 28, "bold"), fg="#00E5FF", bg="#0B0F19").pack()
        tk.Label(title_frame, text="Endüstriyel Yapay Zeka Konsolu v4.2", font=("Segoe UI", 10), fg="#8A99AD", bg="#0B0F19").pack(pady=5)
        tk.Label(title_frame, text="⚠️ Sistemler şu an GELİŞTİRME AŞAMASINDADIR", font=("Segoe UI", 9, "bold"), fg="#F59E0B", bg="#0B0F19").pack(pady=2)

        btn_frame = tk.Frame(self.root, bg="#0B0F19")
        btn_frame.pack(pady=10)

        self.create_menu_button(btn_frame, "🚀 NORTH AI (Sohbet Et)", self.open_chat)
        self.create_menu_button(btn_frame, "📖 Diyalog Rehberi", self.open_guide)
        self.create_menu_button(btn_frame, "ℹ️ Hakkında & Geliştirici", self.open_about)

        footer = tk.Label(self.root, text="📢 Geliştirme ekibi alımı mevcut: @raufedizparlak0", font=("Segoe UI", 9, "bold"), fg="#00E5FF", bg="#111827")
        footer.pack(side=tk.BOTTOM, fill=tk.X, ipady=12)

    def create_menu_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, font=("Segoe UI", 12, "bold"), fg="white", bg="#1A233A",
            activebackground="#25324D", activeforeground="#00E5FF", relief="flat",
            command=command, width=28, height=2, cursor="hand2"
        )
        btn.pack(pady=8)

    # 2. SOHBET EKRANI (Düzeltilmiş ve Güçlendirilmiş)
    def open_chat(self):
        self.clear_window()

        # Üst Bar
        top_bar = tk.Frame(self.root, bg="#111827", height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        tk.Button(top_bar, text="⬅ Geri", font=("Segoe UI", 10, "bold"), fg="white", bg="#1F2937", activebackground="#374151", activeforeground="white", bd=0, command=self.create_menu, cursor="hand2").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(top_bar, text="North AI - Akıllı Sohbet", font=("Segoe UI", 12, "bold"), fg="white", bg="#111827").pack(side=tk.LEFT, padx=10)

        # Alt Giriş Paneli (Önce oluşturuyoruz ki altta sabit kalsın)
        input_frame = tk.Frame(self.root, bg="#111827", height=75)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)
        input_frame.pack_propagate(False)

        send_btn = tk.Button(input_frame, text="Gönder", font=("Segoe UI", 11, "bold"), fg="#0B0F19", bg="#00E5FF", activebackground="#00B4D8", relief="flat", command=self.send_message, cursor="hand2", width=10)
        send_btn.pack(side=tk.RIGHT, padx=12, pady=15)

        self.msg_entry = tk.Entry(input_frame, font=("Segoe UI", 12), bg="#1F2937", fg="white", insertbackground="white", relief="flat")
        self.msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=12, pady=15)
        self.msg_entry.focus_set()
        self.msg_entry.bind("<Return>", lambda event: self.send_message())

        # Sohbet Geçmişi Alanı (Kalan boşluğu doldurur)
        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#0B0F19", fg="#E5E7EB", font=("Segoe UI", 11), bd=0, padx=10, pady=10)
        self.chat_history.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=10, pady=10)
        self.chat_history.config(state=tk.DISABLED)

        self.append_chat("North", "Merhaba! Ben North. Şu an geliştirme aşamasındayım. Bana matematik işlemi sorabilir, sohbet edebilir veya komutları deneyebilirsin!")

    def append_chat(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        if sender == "Sen":
            self.chat_history.insert(tk.END, f"\n> {message}\n", "user")
        else:
            self.chat_history.insert(tk.END, f"\n[North AI]: {message}\n", "bot")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def get_north_response(self, text):
        t = text.lower().strip()

        # Matematik Hesaplama Motoru (Örn: 50+50, 12*4, 100/5)
        if any(op in t for op in ['+', '-', '*', '/', 'x']):
            try:
                # Güvenli matematik hesaplama
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

    def send_message(self):
        text = self.msg_entry.get().strip()
        if not text:
            return

        self.append_chat("Sen", text)
        self.msg_entry.delete(0, tk.END)

        response = self.get_north_response(text)
        self.append_chat("North", response)

    # 3. DİYALOG REHBERİ
    def open_guide(self):
        self.clear_window()

        top_bar = tk.Frame(self.root, bg="#111827", height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        tk.Button(top_bar, text="⬅ Geri", font=("Segoe UI", 10, "bold"), fg="white", bg="#1F2937", activebackground="#374151", activeforeground="white", bd=0, command=self.create_menu, cursor="hand2").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(top_bar, text="Diyalog ve Komut Rehberi", font=("Segoe UI", 12, "bold"), fg="white", bg="#111827").pack(side=tk.LEFT, padx=10)

        guide_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#0B0F19", fg="white", font=("Segoe UI", 11), bd=0, padx=15, pady=15)
        guide_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        dialogues = [
            ("Matematik İşlemleri", "Sohbet ekranına doğrudan 50+50, 14*5, 100/4 gibi işlemler yazarak hesaplatabilirsin."),
            ("nasılsın / naber", "Sistemlerin durumu ve enerji seviyesi hakkında bilgi verir."),
            ("adın ne / kimsin", "Asistanın kimliği hakkında bilgi sunar."),
            ("kim yaptı?", "Projenin geliştiricisini gösterir."),
            ("geliştirme / durum ne", "Yapay zekanın şu anki sürüm ve gelişim aşamasını açıklar."),
            ("şaka yap / fıkra", "Eğlenceli bir matematik şakası patlatır."),
            ("motive et", "Moral verici ve ilham dolu sözler söyler."),
            ("ekip / katılmak", "Geliştirme ekibi iletişim bilgilerini paylaşır.")
        ]

        guide_box.insert(tk.END, "📢 NORTH AI KULLANILABİLİR KOMUTLAR VE ÖZELLİKLER\n\n", "header")
        for cmd, desc in dialogues:
            guide_box.insert(tk.END, f"🔹 {cmd}\n", "cmd")
            guide_box.insert(tk.END, f"Açıklama: {desc}\n\n", "desc")

        guide_box.config(state=tk.DISABLED)

    # 4. HAKKINDA
    def open_about(self):
        self.clear_window()

        top_bar = tk.Frame(self.root, bg="#111827", height=55)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)

        tk.Button(top_bar, text="⬅ Geri", font=("Segoe UI", 10, "bold"), fg="white", bg="#1F2937", activebackground="#374151", activeforeground="white", bd=0, command=self.create_menu, cursor="hand2").pack(side=tk.LEFT, padx=12, pady=10)
        tk.Label(top_bar, text="Hakkında & Geliştirici", font=("Segoe UI", 12, "bold"), fg="white", bg="#111827").pack(side=tk.LEFT, padx=10)

        about_frame = tk.Frame(self.root, bg="#111827")
        about_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=30)

        tk.Label(about_frame, text="North AI v4.2", font=("Segoe UI", 18, "bold"), fg="#00E5FF", bg="#111827").pack(anchor="w", pady=10)
        tk.Label(about_frame, text="Geliştirici: Rauf Ediz Parlak", font=("Segoe UI", 13, "bold"), fg="white", bg="#111827").pack(anchor="w", pady=5)
        tk.Label(about_frame, text="Durum: ⚠️ Aktif Geliştirme Aşamasında", font=("Segoe UI", 11, "bold"), fg="#F59E0B", bg="#111827").pack(anchor="w", pady=5)
        tk.Label(about_frame, text="Açıklama: Endüstriyel yapay zeka konsol altyapısı ve modüler diyalog motoru.", font=("Segoe UI", 10), fg="#9CA3AF", bg="#111827", justify=tk.LEFT).pack(anchor="w", pady=10)
        tk.Label(about_frame, text="📢 Ekip Alımı Aktif!\nKatılmak için:\nİletişim: @raufedizparlak0", font=("Segoe UI", 11, "bold"), fg="#3B82F6", bg="#111827", justify=tk.LEFT).pack(anchor="w", pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = NorthAIApp(root)
    root.mainloop()