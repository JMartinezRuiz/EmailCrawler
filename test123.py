# dump_pcap_full.py
from scapy.all import rdpcap
from scapy.layers.http import HTTPRequest, HTTPResponse  # registra capas HTTP
from scapy.layers.tls.all import TLS                     # registra capas TLS
from scapy.utils import hexdump
import json, datetime

PCAP_FILE = "capture3.pcap"
OUT_JSON  = "capture3_full.json"

def make_jsonable(x):
    """Convierte cualquier valor Scapy a algo serializable en JSON."""
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, bytes):
        return {"_type": "bytes", "len": len(x), "hex": x.hex()}
    if isinstance(x, dict):
        return {str(k): make_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, set)):
        return [make_jsonable(v) for v in x]
    # Objetos Scapy con campos
    if hasattr(x, "fields_desc"):
        out = {}
        for f in x.fields_desc:
            name = f.name
            try:
                val = x.getfieldval(name)
            except Exception:
                val = getattr(x, name, None)
            out[name] = make_jsonable(val)
        return out
    # Último recurso: cadena
    try:
        return str(x)
    except Exception:
        return repr(x)

def layer_to_dict(layer):
    d = {"_layer": layer.__class__.__name__}
    # Campos declarados por la capa
    if hasattr(layer, "fields_desc"):
        for f in layer.fields_desc:
            name = f.name
            try:
                val = layer.getfieldval(name)
            except Exception:
                val = getattr(layer, name, None)
            d[name] = make_jsonable(val)
    # Bytes crudos de la capa
    try:
        d["_raw"] = bytes(layer).hex()
    except Exception:
        pass
    return d

def packet_to_dict(pkt, idx):
    # Tiempos
    t_epoch = float(pkt.time)
    t_iso = datetime.datetime.utcfromtimestamp(t_epoch).isoformat() + "Z"
    # Capas
    layers = []
    try:
        for lay in pkt.layers():
            layers.append(layer_to_dict(lay))
    except Exception:
        # Si algo falla al recorrer capas, al menos guarda el resumen
        layers.append({"_layer": "Unknown", "note": "layer walk failed"})

    # Hexdump completo del paquete
    hx = hexdump(pkt, dump=True)

    return {
        "number": idx,
        "time_epoch": t_epoch,
        "time_iso": t_iso,
        "len": len(pkt),
        "summary": pkt.summary(),
        "layers": layers,
        "hexdump": hx
    }

def main():
    packets = rdpcap(PCAP_FILE)
    out = []
    for i, pkt in enumerate(packets, start=1):
        out.append(packet_to_dict(pkt, i))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ Volcado completo en {OUT_JSON} ({len(out)} paquetes)")

if __name__ == "__main__":
    main()
