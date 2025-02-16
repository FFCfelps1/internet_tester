import speedtest
import subprocess
import statistics
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def testar_internet():
    botao_iniciar["state"] = "disabled"
    status_label["text"] = "Testando conexão..."
    root.update()

    st = speedtest.Speedtest()
    st.get_best_server()

    status_label["text"] = "Testando Download..."
    root.update()
    download = st.download() / 1_000_000  # Convertendo para Mbps

    status_label["text"] = "Testando Upload..."
    root.update()
    upload = st.upload() / 1_000_000  # Convertendo para Mbps

    status_label["text"] = "Medindo Latência..."
    root.update()
    ping = st.results.ping  # Ping médio

    status_label["text"] = "Medindo Jitter e Perda de Pacotes..."
    root.update()
    jitter, perda = calcular_jitter_perda()

    resultado_texto.set(f"📡 Download: {download:.2f} Mbps\n"
                        f"🚀 Upload: {upload:.2f} Mbps\n"
                        f"⚡ Ping: {ping:.2f} ms\n"
                        f"📉 Jitter: {jitter:.2f} ms\n"
                        f"❌ Perda de Pacotes: {perda:.2f} %")

    status_label["text"] = "Teste concluído!"
    botao_iniciar["state"] = "normal"

def calcular_jitter_perda(host="8.8.8.8", num_pings=10):
    try:
        command = ["ping", "-n" if subprocess.os.name == "nt" else "-c", str(num_pings), host]
        output = subprocess.run(command, capture_output=True, text=True).stdout
        
        tempos = [int(match.group(1)) for match in re.finditer(r"time[=<]([\d.]+) ms", output)]
        perda = 0

        perda_match = re.search(r"(\d+)% packet loss", output)
        if perda_match:
            perda = float(perda_match.group(1))

        jitter = statistics.stdev(tempos) if len(tempos) > 1 else 0  # Desvio padrão

        return jitter, perda
    except Exception:
        return 0, 0

# Criando a interface gráfica
root = tk.Tk()
root.title("Teste de Internet")
root.geometry("400x300")
root.resizable(True, True)

# Carregando a imagem de fundo
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Criando um Canvas para a imagem de fundo
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Criando um frame sobre o Canvas
frame = ttk.Frame(canvas, padding=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

status_label = ttk.Label(frame, text="Clique para iniciar o teste", font=("Helvetica", 12))
status_label.pack()

botao_iniciar = ttk.Button(frame, text="Iniciar Teste", command=testar_internet, style="TButton")
botao_iniciar.pack(pady=10)

resultado_texto = tk.StringVar()
resultado_label = ttk.Label(frame, textvariable=resultado_texto, font=("Helvetica", 10), justify="left")
resultado_label.pack()

root.mainloop()