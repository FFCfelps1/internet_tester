import speedtest
import subprocess
import statistics
import re

def testar_internet():
    print("Testando conexão...")

    st = speedtest.Speedtest()
    st.get_best_server()

    print("Testando Download...")
    download = st.download() / 1_000_000  # Convertendo para Mbps

    print("Testando Upload...")
    upload = st.upload() / 1_000_000  # Convertendo para Mbps

    print("Medindo Latência...")
    ping = st.results.ping  # Ping médio

    print("Medindo Jitter e Perda de Pacotes...")
    jitter, perda = calcular_jitter_perda()

    print(f"📡 Download: {download:.2f} Mbps")
    print(f"🚀 Upload: {upload:.2f} Mbps")
    print(f"⚡ Ping: {ping:.2f} ms")
    print(f"📉 Jitter: {jitter:.2f} ms")
    print(f"❌ Perda de Pacotes: {perda:.2f} %")

    print("Teste concluído!")

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

if __name__ == "__main__":
    testar_internet()