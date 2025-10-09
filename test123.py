from scapy.all import rdpcap
import json

packets = rdpcap("capture3.pcap")

data = []
for i, pkt in enumerate(packets, start=1):
    info = {
        "numero": i,
        "resumen": pkt.summary()
    }

    if pkt.haslayer("IP"):
        info["ip_origen"] = pkt["IP"].src
        info["ip_destino"] = pkt["IP"].dst

    if pkt.haslayer("TCP"):
        info["puerto_origen"] = pkt["TCP"].sport
        info["puerto_destino"] = pkt["TCP"].dport

    if pkt.haslayer("UDP"):
        info["puerto_origen"] = pkt["UDP"].sport
        info["puerto_destino"] = pkt["UDP"].dport

    data.append(info)

with open("salida.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Archivo convertido a salida.json correctamente.")
