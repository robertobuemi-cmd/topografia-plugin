#!/usr/bin/env python3
"""
Controllo dipendenze del plugin Topografia. Lanciato dall'hook SessionStart
(hooks/hooks.json). Non stampa nulla se tutto è già a posto: l'output di
questo script finisce come contesto extra nella sessione Codex, quindi resta
silenzioso salvo azioni/avvisi reali.

- ezdxf: se manca, prova a installarlo automaticamente (pip, utente corrente).
- ODA File Converter: se manca, avvisa soltanto. Non lo scarica né lo
  installa da solo: è un installer desktop esterno, va approvato ed eseguito
  dall'utente.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def check_and_install_ezdxf():
    try:
        import ezdxf  # noqa: F401
        return None
    except ImportError:
        pass

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "ezdxf"],
            check=True,
            capture_output=True,
            timeout=120,
            text=True,
        )
        return "Installato automaticamente: ezdxf (mancava)."
    except Exception as exc:
        return (
            "ATTENZIONE: manca ezdxf e l'installazione automatica e' fallita "
            f"({exc}). Installa manualmente con: pip install ezdxf"
        )


def check_oda_file_converter():
    default_win = Path(
        r"C:\Program Files\ODA\ODAFileConverter\ODAFileConverter.exe"
    )
    if default_win.exists():
        return None
    if shutil.which("ODAFileConverter"):
        return None

    return (
        "ATTENZIONE: ODA File Converter non risulta installato "
        "(nessun eseguibile trovato nel percorso di default ne' nel PATH). "
        "Serve per lavorare con file DWG nativi. Scaricalo (gratuito) da: "
        "https://www.opendesign.com/guestfiles/oda_file_converter "
        "poi riavvia Codex. Se lo installi in un percorso diverso, imposta "
        "la variabile d'ambiente ODAFC_PATH con il percorso completo "
        "dell'eseguibile."
    )


def main():
    messages = []
    m1 = check_and_install_ezdxf()
    if m1:
        messages.append(m1)
    m2 = check_oda_file_converter()
    if m2:
        messages.append(m2)

    if messages:
        print("\n".join(messages))
    # exit 0 sempre: un problema di dipendenze non deve bloccare la sessione


if __name__ == "__main__":
    main()
