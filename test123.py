import pyshark
import json

# Carga el archivo pcap
cap = pyshark.FileCapture("captura.pcap")

data = []

# Recorre los paquetes y guarda los datos más relevantes
for pkt in cap:
    packet_info = {
        "numero": pkt.number,
        "tiempo": pkt.sniff_time.isoformat(),
        "longitud": pkt.length,
        "protocolo": pkt.highest_layer,
        "resumen": pkt.summary
    }
    data.append(packet_info)

# Guarda como JSON
with open("salida.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Archivo convertido a salida.json")
