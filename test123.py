import pyshark
import json

# Carga el archivo pcap (mismo directorio que el script)
cap = pyshark.FileCapture("capture3.pcap")

# Lista para guardar los paquetes
data = []

# Recorre cada paquete y guarda la información más relevante
for pkt in cap:
    info = {
        "numero": pkt.number,
        "tiempo": pkt.sniff_time.isoformat() if hasattr(pkt, "sniff_time") else None,
        "longitud": pkt.length,
        "protocolo": pkt.highest_layer,
        "resumen": pkt.summary
    }

    # Añade IP y puertos si existen
    if "ip" in pkt:
        info["ip_origen"] = pkt.ip.src
        info["ip_destino"] = pkt.ip.dst
    if "tcp" in pkt:
        info["puerto_origen"] = pkt.tcp.srcport
        info["puerto_destino"] = pkt.tcp.dstport
    if "udp" in pkt:
        info["puerto_origen"] = pkt.udp.srcport
        info["puerto_destino"] = pkt.udp.dstport

    data.append(info)

# Guardar como JSON legible
with open("salida.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Archivo convertido a salida.json correctamente.")
