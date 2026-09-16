---
name: topografia-rilievi
description: Playbook per task di rilievo (stato di fatto, controllo ferri/cassero rispetto alla sagoma teorica, restituzione). Va usato insieme alla skill madre "topografia", non da solo, quando la task è identificata come rilievo.
---

# Playbook Rilievi

Dettaglio completo e casi reali in
`../topografia/reference/WORKFLOW_TOPOGRAFIA_v0_4.md` — sezione 7.2 e § 20
per il modello mentale, §§ 36-42 per i rilievi di controllo ferri/cassero.
**Nota:** rispetto al playbook Tracciamenti, questo riassunto copre solo la
parte finale (controllo ferri/cassero) del documento sorgente in modo
verificato riga per riga; per i casi intermedi del rilievo (stato di fatto
"puro", altre tipologie) fai sempre riferimento diretto al file allegato
prima di procedere, non generalizzare da questo riassunto.

## 1. Modello mentale

Prima di rilevare o pianificare cosa rilevare: **immagina come il terreno o
l'opera dovranno essere restituiti in ufficio** una volta finito il rilievo.
Ragiona a ritroso su cosa serve per una restituzione completa.

## 2. Rilievi di controllo ferri/cassero

- Ferro, cassero e sagoma teorica vanno su **layer distinti** e graficamente
  distinguibili (colore libero, non standardizzato).
- La polilinea del rilievo reale si costruisce **unendo direttamente i punti
  rilevati** — non si ricostruisce una geometria teorica alternativa.
- Ogni campagna di rilievo deve restare identificabile per layer/data
  (tracciabilità temporale tra rilievi successivi della stessa pila).
- Scostamenti reale/teorico: rappresentati punto per punto con quote
  lineari/allineate, quando richiesti.
- Controllo di centro/asse o modello 3D complessivo: **non obbligatori** nel
  flusso minimo — solo se richiesti o utili a fine opera.

## 3. Criterio di chiusura

Il rilievo è pronto se il DWG/DXF contiene in modo chiaro e coerente: punti
rilevati, restituzione, layer distinti, geometria teorica, polilinea reale,
scostamenti (se richiesti) — leggibile dal Responsabile Topografia. Se è
così, non servono controlli aggiuntivi obbligatori.

## 4. Nomenclatura file (convenzione corrente, non universale)

```text
DATA_WBS_ELEMENTO_TIPO_RILIEVO
```
Esempio: `260914_VI05_P4_RIL_CASS.DWG` (data, WBS opera, elemento/pila, tipo
rilievo). Verifica sempre se il cantiere corrente usa questa convenzione o
un'altra — non darla per scontata.

## 5. Consegna e archivio

- Consegna standard al Responsabile Topografia: **solo il DWG finale** (il
  TXT punti non si invia come consegna standard).
- Archivio interno: DWG finale + TXT originale dei punti + eventuale DWG di
  supporto/preparazione con i soli elementi usati per la lavorazione. Gli
  originali di progetto restano nelle cartelle ufficiali.

## 6. Regole da non violare

Non modificare originali · non inventare quote/coordinate · non arbitrare
tra elaborati discordanti · non generare punti inutili · non confondere
dato di progetto con decisione operativa di campo.
