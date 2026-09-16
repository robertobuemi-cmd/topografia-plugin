#!/usr/bin/env python3
"""
Bridge DXF/DWG + gestione punti TXT per il plugin Topografia.

Requisiti:
    pip install ezdxf
    ODA File Converter installato (gratuito, ufficiale):
    https://www.opendesign.com/guestfiles/oda_file_converter
    Percorso atteso su Windows di default:
    C:\\Program Files\\ODA\\ODAFileConverter\\ODAFileConverter.exe
    (se diverso, impostare la variabile d'ambiente ODAFC_PATH)

Uso da riga di comando:
    python dwg_dxf_bridge.py dwg2dxf input.dwg output.dxf
    python dwg_dxf_bridge.py dxf2dwg input.dxf output.dwg [--version R2018]
    python dwg_dxf_bridge.py points2dxf punti.txt output.dxf
        [--order NEC|ENC] [--prefix FIBE]
    python dwg_dxf_bridge.py dxf2points input.dxf output.txt
        [--order NEC|ENC]

Formato TXT punti atteso (una riga per punto, separatore virgola):
    NomePunto,Est,Nord,Quota,Codice   (--order ENC, default cantiere attuale)
    NomePunto,Nord,Est,Quota,Codice   (--order NEC)

Nota: lo script NON assume da solo l'ordine Est/Nord — va sempre passato
esplicitamente con --order, come richiesto dal workflow (§19.3 del
documento sorgente).
"""

import argparse
import os
import sys

try:
    import ezdxf
    from ezdxf.addons import odafc
except ImportError:
    print("Manca ezdxf. Installa con: pip install ezdxf", file=sys.stderr)
    sys.exit(1)


def _set_oda_path():
    custom = os.environ.get("ODAFC_PATH")
    if custom:
        ezdxf.options.config["odafc-addon"]["win_exec_path"] = custom


def dwg2dxf(src: str, dst: str):
    _set_oda_path()
    doc = odafc.readfile(src)
    doc.saveas(dst)
    print(f"OK: {src} -> {dst} (DXF versione {doc.dxfversion})")


def dxf2dwg(src: str, dst: str, version: str = "R2018"):
    _set_oda_path()
    doc = ezdxf.readfile(src)
    odafc.export_dwg(doc, dst, version=version)
    print(f"OK: {src} -> {dst} (DWG versione {version})")


def points2dxf(src_txt: str, dst_dxf: str, order: str = "ENC", prefix: str = "FIBE"):
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()
    with open(src_txt, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                print(f"Riga ignorata (formato non valido): {line}", file=sys.stderr)
                continue
            name = parts[0]
            if order == "ENC":
                e, n, z = float(parts[1]), float(parts[2]), float(parts[3])
            elif order == "NEC":
                n, e, z = float(parts[1]), float(parts[2]), float(parts[3])
            else:
                raise ValueError("order deve essere ENC o NEC")
            code = parts[4] if len(parts) > 4 else "PT"

            layer = f"{prefix}_{code}".upper()
            if layer not in doc.layers:
                doc.layers.add(layer)

            msp.add_point((e, n, z), dxfattribs={"layer": layer})
            msp.add_text(
                name,
                dxfattribs={"layer": layer, "height": 0.15, "insert": (e, n, z)},
            )
    doc.saveas(dst_dxf)
    print(f"OK: punti da {src_txt} -> {dst_dxf}")


def dxf2points(src_dxf: str, dst_txt: str, order: str = "ENC"):
    doc = ezdxf.readfile(src_dxf)
    msp = doc.modelspace()
    with open(dst_txt, "w", encoding="utf-8") as f:
        for i, p in enumerate(msp.query("POINT"), start=1):
            x, y, z = p.dxf.location
            layer = p.dxf.layer
            name = f"P{i}"
            if order == "ENC":
                f.write(f"{name},{x},{y},{z},{layer}\n")
            elif order == "NEC":
                f.write(f"{name},{y},{x},{z},{layer}\n")
            else:
                raise ValueError("order deve essere ENC o NEC")
    print(f"OK: punti da {src_dxf} -> {dst_txt}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("dwg2dxf")
    p1.add_argument("src")
    p1.add_argument("dst")

    p2 = sub.add_parser("dxf2dwg")
    p2.add_argument("src")
    p2.add_argument("dst")
    p2.add_argument("--version", default="R2018")

    p3 = sub.add_parser("points2dxf")
    p3.add_argument("src")
    p3.add_argument("dst")
    p3.add_argument("--order", default="ENC", choices=["ENC", "NEC"])
    p3.add_argument("--prefix", default="FIBE")

    p4 = sub.add_parser("dxf2points")
    p4.add_argument("src")
    p4.add_argument("dst")
    p4.add_argument("--order", default="ENC", choices=["ENC", "NEC"])

    args = ap.parse_args()

    if args.cmd == "dwg2dxf":
        dwg2dxf(args.src, args.dst)
    elif args.cmd == "dxf2dwg":
        dxf2dwg(args.src, args.dst, args.version)
    elif args.cmd == "points2dxf":
        points2dxf(args.src, args.dst, args.order, args.prefix)
    elif args.cmd == "dxf2points":
        dxf2points(args.src, args.dst, args.order)


if __name__ == "__main__":
    main()
