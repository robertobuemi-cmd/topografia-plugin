---
name: topografia
description: Workflow topografico strutturato per tracciamenti (picchettazione muri, fondazioni, magroni) e rilievi (stato di fatto, controllo ferri/cassero). Invocazione solo esplicita — @Topografia nell'app, $topografia in CLI/IDE.
---

# Workflow madre `Topografia`

Questa skill instrada verso i playbook specifici e applica le regole trasversali
valide per ogni task topografica. Il testo integrale e definitivo del metodo,
con tutti i casi ed esempi raccolti finora, è nel file allegato
`reference/WORKFLOW_TOPOGRAFIA_v0_4.md`: consultalo quando serve un dettaglio
non riassunto qui sotto — è la fonte di verità, questo file è solo il riassunto
operativo.

## 0. Attivazione

Questa skill (e i playbook collegati) hanno `allow_implicit_invocation: false`:
non si attivano mai da sole leggendo il contesto, solo su richiamo esplicito
dell'utente. Fine task → nessuna azione da fare per "disattivarsi": senza
invocazione esplicita la skill resta semplicemente ferma, di default.

## 1. Riconoscimento task e instradamento

Determina il tipo di lavorazione dalla richiesta e dagli allegati, poi
richiama esplicitamente il playbook pertinente:

- tracciamento (picchettazione, punti da materializzare in campo per scavo/
  magrone/fondazione/muro) → invoca esplicitamente `topografia-tracciamenti`;
- rilievo (stato di fatto, controllo ferri/cassero, restituzione) → invoca
  esplicitamente `topografia-rilievi`.

Se la task è ambigua, chiedilo esplicitamente all'utente prima di procedere:
non indovinare tra tracciamento e rilievo.

## 2. Regole trasversali (workflow madre)

1. **Non modificare mai gli originali.** Copia i file allegati nel workspace
   e lavora solo sulle copie.
2. **Non inventare dati mancanti**: quote, coordinate, spessori, codici
   progetto/commessa. Se manca un dato necessario, chiedilo.
3. **Confronta gli elaborati tra loro** (planimetria, sezioni, profilo
   longitudinale, coordinate annotate): devono essere coerenti. Le coordinate
   scritte su un disegno non si usano automaticamente — verifica sempre a
   quale vertice/elemento si riferiscono.
4. **Incongruenze tra elaborati**: non scegliere tu quale elaborato prevale.
   Identifica il conflitto, quantifica la differenza se possibile, sospendi
   la parte interessata, segnala il conflitto all'utente ("Responsabile di
   Topografia") e attendi la decisione prima di proseguire.
5. **Genera solo i punti geometricamente necessari** (numero minimo per
   definire correttamente la geometria).
6. **Distingui preparazione in ufficio da materializzazione in campo**: in
   ufficio ci si attiene al progetto, senza inventare offset operativi "che
   potrebbero servire".
7. A fine lavorazione: presenta risultato e anomalie, poi **fermati per la
   revisione dell'utente**. Non chiudere la task da solo.

## 3. Workspace isolato

All'attivazione, prima di lavorare:

1. chiedi in quale directory creare il workspace (default proposto: Desktop
   reale dell'utente Windows — risolvi il percorso effettivo del profilo,
   non assumere `C:\Users\<nome>\Desktop` perché potrebbe essere
   reindirizzato da OneDrive);
2. chiedi il nome della cartella task (es. `GN07_TRK`) — non inventarlo;
3. se la cartella esiste già, chiedi come procedere (riusarla / nuovo nome /
   nuova revisione), non sovrascrivere in automatico;
4. crea la struttura:

```text
[DIRECTORY]/[NOME_TASK]/
├── INPUT/    copie dei file sorgente (read-only concettuale)
├── WORK/     file intermedi, conversioni, elaborazioni
├── OUTPUT/   elaborati finali richiesti
└── AUDIT/    controlli, anomalie, log, decisioni
```

## 4. Formato TXT dei punti

L'ordine colonne NON è fisso (dipende da cantiere/strumento). Cantiere
attuale: `Nome punto, Est, Nord, Quota, Codice`. Non assumere mai
automaticamente l'ordine Est/Nord: se non è specificato, chiedilo.

## 5. File DXF/DWG

Per generare o leggere disegni usa lo script bundlato
`../../scripts/dwg_dxf_bridge.py` (vedi il README del plugin per i requisiti:
libreria `ezdxf` + ODA File Converter per la conversione nativa DWG↔DXF).
Lavora sempre in DXF internamente; converti in DWG solo in output, se
richiesto.

## 6. Quando fare domande

Solo se l'informazione mancante può cambiare materialmente il risultato, lo
rende non verificabile, genera ambiguità di progetto, o è una condizione di
STOP (incongruenza tra elaborati, dato non ricavabile, nomenclatura non
definita per il caso in questione). Non fare domande di conferma banali.
