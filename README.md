# Plugin Codex `topografia`

## Cosa contiene

```text
topografia-plugin/
├── .codex-plugin/plugin.json     manifest del plugin
├── skills/
│   ├── topografia/                skill madre (router + regole trasversali)
│   │   └── reference/WORKFLOW_TOPOGRAFIA_v0_4.md   documento sorgente completo
│   ├── topografia-tracciamenti/   playbook tracciamento
│   └── topografia-rilievi/        playbook rilievo
└── scripts/dwg_dxf_bridge.py     conversione DXF/DWG + punti TXT
```

## Requisiti — ora in gran parte automatici

Il plugin include un hook `SessionStart` (`hooks/hooks.json` →
`scripts/check_dependencies.py`) che ad ogni avvio sessione:

- controlla se **ezdxf** è installato, e se manca lo installa da solo
  (`pip install --user ezdxf`);
- controlla se **ODA File Converter** è presente; se manca **non lo installa**
  (è un `.exe` desktop scaricato da terzi, va approvato da te) — ti avvisa
  con il link ufficiale: https://www.opendesign.com/guestfiles/oda_file_converter

**Attenzione — due cose non automatizzabili, per come funziona Codex:**

1. **La prima volta** Codex ti chiederà di rivedere e approvare l'hook
   (`/hooks`) prima che possa girare — è una misura di sicurezza della
   piattaforma, non qualcosa che posso saltare.
2. **Non è garantito al 100%** che gli hook bundlati in un plugin vengano
   caricati in automatico in ogni versione di Codex (bug noto, issue
   openai/codex #16430 al momento della stesura). Se dopo l'installazione
   `check_dependencies.py` non sembra girare, verifica con `/hooks` se
   risulta tra le fonti caricate; in caso contrario, come fallback puoi
   copiare `hooks/hooks.json` anche in `~/.codex/hooks.json` (adattando i
   percorsi assoluti al posto di `$PLUGIN_ROOT`/`%PLUGIN_ROOT%`).

Se preferisci evitare del tutto gli hook, resta comunque valido il percorso
manuale: `pip install ezdxf` + installazione di ODA File Converter una tantum.

## Installazione del plugin in Codex

Il plugin va registrato in una marketplace locale. Due opzioni:

**Personale (disponibile in tutte le sessioni Codex):**
Copia la cartella `topografia-plugin/` in una posizione stabile, poi crea o
aggiorna `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "personal",
  "plugins": [
    {
      "name": "topografia",
      "source": { "source": "local", "path": "/percorso/assoluto/topografia-plugin" }
    }
  ]
}
```

**Alternativa più semplice**: in una sessione Codex digita `$plugin-creator`
e forniscigli la cartella `topografia-plugin/` già pronta — lo scaffolding
e la registrazione in marketplace li fa lui in automatico, verificando
anche eventuali errori di manifest nel tuo ambiente reale (cosa che io da
qui non posso controllare).

Dopo l'installazione, riavvia Codex.

## Uso

Attivazione **solo esplicita** (l'automatica è disattivata di proposito via
`agents/openai.yaml` → `policy.allow_implicit_invocation: false`):

- Codex App (superficie ChatGPT/Codex, quella con menu "Plugin" su `@`):
  digita `@Topografia`
- Codex CLI / estensione IDE: `$topografia` o `/skills`

Fine task = nessuna azione richiesta per "spegnerla": senza un nuovo
richiamo esplicito la skill non si riattiva da sola.

## Cosa NON è ancora definito (dal documento sorgente stesso, §45)

- sintassi definitiva dei layer `FIBE_*` oltre agli esempi dati;
- criteri automatici per capire quando serve il controllo centro/asse;
- procedure di STOP dettagliate e struttura AUDIT;
- playbook Rilievi completo (qui è riassunta solo la parte "controllo
  ferri/cassero", verificata riga per riga sul documento; il resto va letto
  dal file reference caso per caso).

Il primo uso reale del plugin nel tuo ambiente Codex è anche il primo test
vero — qui non ho potuto installarlo né verificarlo dal vivo.
