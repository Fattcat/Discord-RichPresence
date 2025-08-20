# discord_rpc_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from pypresence import Presence
import json
import time
import os

# Súbor na uloženie nastavení
CONFIG_FILE = "rpc_config.json"

class DiscordRPCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Rich Presence GUI")
        self.root.geometry("500x600+640+270")
        self.root.resizable(False, False)

        self.rpc = None
        self.connected = False

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        # === Nadpis ===
        tk.Label(self.root, text="Discord Rich Presence", font=("Arial", 16, "bold")).pack(pady=10)

        # === Client ID ===
        tk.Label(self.root, text="Client ID:").pack(anchor="w", padx=20)
        self.client_id_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.client_id_var, width=50).pack(padx=20, pady=5)

        # === Details (Horný riadok) ===
        tk.Label(self.root, text="Details (napr. Meno hry):").pack(anchor="w", padx=20)
        self.details_var = tk.StringVar(value="-")
        tk.Entry(self.root, textvariable=self.details_var, width=50).pack(padx=20, pady=5)

        # === State (Dolný riadok) ===
        tk.Label(self.root, text="State (napr. Na leveli 5):").pack(anchor="w", padx=20)
        self.state_var = tk.StringVar(value="Bežný stav")
        tk.Entry(self.root, textvariable=self.state_var, width=50).pack(padx=20, pady=5)

        # === Large Image (ID z Art Assets) ===
        tk.Label(self.root, text="Large Image ID (z Art Assets):").pack(anchor="w", padx=20)
        self.large_image_var = tk.StringVar(value="large_icon")
        tk.Entry(self.root, textvariable=self.large_image_var, width=50).pack(padx=20, pady=5)

        tk.Label(self.root, text="Large Text (pri prejdení myšou):").pack(anchor="w", padx=20)
        self.large_text_var = tk.StringVar(value="Veľká ikona")
        tk.Entry(self.root, textvariable=self.large_text_var, width=50).pack(padx=20, pady=5)

        # === Small Image ===
        tk.Label(self.root, text="Small Image ID (voliteľné):").pack(anchor="w", padx=20)
        self.small_image_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.small_image_var, width=50).pack(padx=20, pady=5)

        tk.Label(self.root, text="Small Text:").pack(anchor="w", padx=20)
        self.small_text_var = tk.StringVar(value="Malá ikona")
        tk.Entry(self.root, textvariable=self.small_text_var, width=50).pack(padx=20, pady=5)

        # === Tlačidlá ===
        tk.Label(self.root, text="Tlačidlo 1 (názov):").pack(anchor="w", padx=20)
        self.button1_label_var = tk.StringVar(value="Stiahnuť")
        tk.Entry(self.root, textvariable=self.button1_label_var, width=50).pack(padx=20, pady=5)

        tk.Label(self.root, text="Tlačidlo 1 (URL):").pack(anchor="w", padx=20)
        self.button1_url_var = tk.StringVar(value="https://NejakyTvojLink.com")
        tk.Entry(self.root, textvariable=self.button1_url_var, width=50).pack(padx=20, pady=5)

        # === Kontrolné tlačidlá ===
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.connect_btn = tk.Button(frame, text="Pripojiť RPC", command=self.connect_rpc, bg="lightgreen", width=12)
        self.connect_btn.grid(row=0, column=0, padx=5)

        self.update_btn = tk.Button(frame, text="Aktualizovať", command=self.update_rpc, bg="lightblue", state="disabled", width=12)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.clear_btn = tk.Button(frame, text="Zastaviť", command=self.clear_rpc, bg="orange", state="disabled", width=12)
        self.clear_btn.grid(row=0, column=2, padx=5)

        self.save_btn = tk.Button(self.root, text="Uložiť nastavenia", command=self.save_config, bg="lightgray")
        self.save_btn.pack(pady=10)

        # Status
        self.status_var = tk.StringVar(value="Stav: Odpojené")
        tk.Label(self.root, textvariable=self.status_var, fg="gray").pack(pady=5)

    def connect_rpc(self):
        client_id = self.client_id_var.get().strip()
        if not client_id:
            messagebox.showerror("Chyba", "Zadaj Client ID!")
            return

        try:
            self.rpc = Presence(client_id)
            self.rpc.connect()
            self.connected = True
            self.connect_btn.config(state="disabled")
            self.update_btn.config(state="normal")
            self.clear_btn.config(state="normal")
            self.status_var.set("Stav: Pripojené")
            self.update_rpc()  # Aktualizuj hneď po pripojení
            messagebox.showinfo("Úspech", "Pripojené k Discord RPC!")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nie je možné pripojiť: {e}")

    def update_rpc(self):
        if not self.connected:
            return

        try:
            buttons = []
            if self.button1_label_var.get() and self.button1_url_var.get():
                buttons.append({
                    "label": self.button1_label_var.get(),
                    "url": self.button1_url_var.get()
                })

            data = {
                "details": self.details_var.get() or None,
                "state": self.state_var.get() or None,
                "large_image": self.large_image_var.get() or "none",
                "large_text": self.large_text_var.get() or None,
                "start": int(time.time())
            }

            if self.small_image_var.get():
                data["small_image"] = self.small_image_var.get()
                data["small_text"] = self.small_text_var.get() or None

            if buttons:
                data["buttons"] = buttons

            self.rpc.update(**{k: v for k, v in data.items() if v is not None})
            self.status_var.set("Stav: Aktualizované")
        except Exception as e:
            messagebox.showerror("Chyba", f"Chyba pri aktualizácii: {e}")

    def clear_rpc(self):
        if self.rpc and self.connected:
            self.rpc.clear()
            self.rpc.close()
        self.connected = False
        self.connect_btn.config(state="normal")
        self.update_btn.config(state="disabled")
        self.clear_btn.config(state="disabled")
        self.status_var.set("Stav: Odpojené")

    def save_config(self):
        config = {
            "client_id": self.client_id_var.get(),
            "details": self.details_var.get(),
            "state": self.state_var.get(),
            "large_image": self.large_image_var.get(),
            "large_text": self.large_text_var.get(),
            "small_image": self.small_image_var.get(),
            "small_text": self.small_text_var.get(),
            "button1_label": self.button1_label_var.get(),
            "button1_url": self.button1_url_var.get()
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Uložené", "Nastavenia uložené!")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nie je možné uložiť: {e}")

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.client_id_var.set(config.get("client_id", ""))
            self.details_var.set(config.get("details", "Hrám hru"))
            self.state_var.set(config.get("state", "Bežný stav"))
            self.large_image_var.set(config.get("large_image", "large_icon"))
            self.large_text_var.set(config.get("large_text", "Veľká ikona"))
            self.small_image_var.set(config.get("small_image", ""))
            self.small_text_var.set(config.get("small_text", "Malá ikona"))
            self.button1_label_var.set(config.get("button1_label", "Stiahnuť hru"))
            self.button1_url_var.set(config.get("button1_url", "https://example.com"))
        except Exception as e:
            messagebox.showwarning("Načítanie", f"Nie je možné načítať nastavenia: {e}")


# === Spustenie aplikácie ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordRPCApp(root)
    root.mainloop()
