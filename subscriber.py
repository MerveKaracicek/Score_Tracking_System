# subscriber.py
import pika
import threading
import time
from queue import Queue
import customtkinter as ctk
from tkinter import messagebox

# Tema ve ayar
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

message_queue = Queue()
channel = None
connection = None


def callback(ch, method, properties, body):
    message_queue.put(body.decode())


def start_listening(team_name, textbox):
    global channel, connection

    try:
        routing_key = f"team.{team_name.lower().replace(' ', '_')}"
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.exchange_declare(exchange="teams", exchange_type="topic")

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="teams", queue=queue_name, routing_key=routing_key)

        def display_messages():
            while True :
                if not message_queue.empty():
                    msg = message_queue.get()
                    textbox.insert("end",f"⚽ {msg}\n")
                    textbox.yview("end")
                    time.sleep(3)
                else:
                    time.sleep(1)

        threading.Thread(target=display_messages, daemon=True).start()
        def consume():
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
        threading.Thread(target=consume, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Hata", f"Bağlantı hatası: {e}")


def on_start_click(entry, textbox):
    team_name = entry.get().strip()
    if not team_name:
        messagebox.showwarning("Uyarı", "Lütfen bir takım adı girin.")
        return
    textbox.delete("1.0", "end")
    start_listening(team_name, textbox)

# GUI oluştur
app = ctk.CTk()
app.title("⚽ Canlı Skor Takip")
app.geometry("600x500")

ctk.CTkLabel(app, text="Takım Adı Girin", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)

entry = ctk.CTkEntry(app, width=300, height=40, placeholder_text="Örn: Real Madrid")
entry.pack(pady=10)

button = ctk.CTkButton(app, text="Takibi Başlat", command=lambda: on_start_click(entry, text_box))
button.pack(pady=15)

text_box = ctk.CTkTextbox(app, width=550, height=300)
text_box.pack(pady=10)

app.mainloop()