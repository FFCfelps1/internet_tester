from fastapi import FastAPI
import speedtest
import subprocess
import statistics
import re

app = FastAPI()

def calcular_jitter_perda(host="8.8.8.8", num_pings=10):
    try:
        command = ["ping", "-n" if subprocess.os.name == "nt" else "-c", str(num_pings), host]
        output = subprocess.run(command, capture_output=True, text=True).stdout

        tempos = [int(match.group(1)) for match in re.finditer(r"time[=<]([\d.]+) ms", output)]
        perda = 0

        perda_match = re.search(r"(\d+)% packet loss", output)
        if perda_match:
            perda = float(perda_match.group(1))

        jitter = statistics.stdev(tempos) if len(tempos) > 1 else 0

        return jitter, perda
    except Exception:
        return 0, 0

@app.get("/testar_internet")
def testar_internet():
    st = speedtest.Speedtest()
    st.get_best_server()

    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000
    ping = st.results.ping  # ms
    jitter, perda = calcular_jitter_perda()

    return {
        "download": round(download, 2),
        "upload": round(upload, 2),
        "ping": round(ping, 2),
        "jitter": round(jitter, 2),
        "perda_pacotes": round(perda, 2)
    }

