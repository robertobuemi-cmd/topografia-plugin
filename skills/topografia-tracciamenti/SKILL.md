---
name: topografia-tracciamenti
description: Playbook per task di tracciamento/picchettazione (muri, fondazioni, magroni) a partire da elaborati progettuali. Va usato insieme alla skill madre "topografia", non da solo, quando la task è identificata come tracciamento.
---

# Playbook Tracciamenti

Dettaglio completo e casi reali in
`../topografia/reference/WORKFLOW_TOPOGRAFIA_v0_4.md` (sezioni 7.1, 9-19).
Qui il riassunto operativo.

## 1. Modello mentale

Prima di sviluppare punti/coordinate/quote: **studia gli elaborati e
immagina l'opera finita** (forma, relazioni tra elementi, sequenza
costruttiva, cosa va materializzato in campo). Non partire dalla geometria
CAD senza aver capito l'opera.

## 2. Lettura elaborati

Planimetria, sezioni e profilo longitudinale devono "parlare la stessa
lingua": ricostruisci la coerenza tra progressive, quote, geometrie e
coordinate riportate — non leggere un disegno isolatamente se ce ne sono
altri che descrivono la stessa opera.

Se pertinente, verifica se esiste un rilievo di stato di fatto: le quote
progettuali non coincidono automaticamente con la realtà fisica del
terreno (questo non ti autorizza a modificarle).

## 3. Sequenza costruttiva (muri)

```text
SCAVO → MAGRONE → FONDAZIONE ARMATA → FERRI DI RIPRESA → GETTO → TRACCIAMENTO MURI
```

Prima di generare "i punti del muro", capisci per quale fase servono
realmente i dati.

Primo riferimento geometrico: spigoli della fondazione (o del magrone, se
rappresentato). Quota fondo scavo = quota testa magrone − spessore magrone
(lo spessore va preso dagli elaborati, mai inventato).

## 4. Scelta dei punti

- fondazione rettangolare semplice → **solo i 4 spigoli**;
- fondazione irregolare → tutti i vertici geometricamente significativi,
  numero minimo necessario a definire la geometria senza ambiguità.

## 5. Nomenclatura (convenzione attuale, adattabile alla complessità reale)

| Elemento   | Prefisso punto | Codice TXT |
|------------|-----------------|------------|
| Magrone    | `MG_A1, MG_B1...` | `MAG` |
| Fondazione | `FND1...` o `FND_A1...` (se ci sono conci/tratti) | `FND` |
| Muro       | `MR1...` o `MR_A1...` | `MR` |

Se la task è semplice e senza rischio di ambiguità è ammessa numerazione
semplice (1,2,3...). Non complicare la nomenclatura quando non serve.

## 6. CAD di preparazione

Per ogni preparazione dati importante, crea un DWG/DXF pulito e dedicato
(memoria tecnica della lavorazione) con: planimetria georeferenziata,
geometrie usate, elaborati di supporto, polilinee, punti, quote. Non è un
file da eliminare — deve permettere di ricostruire in futuro come sono
stati sviluppati i punti.

Layer con prefisso `FIBE_` (es. `FIBE_FONDAZIONE`, `FIBE_MAGRONE`,
`FIBE_MURO`), colori differenti per elemento (non standardizzati).

## 7. Regole da non violare

Non modificare originali · non inventare quote/coordinate/spessori · non
arbitrare tra elaborati discordanti (segnala e fermati) · non generare
punti inutili · non confondere dato di progetto (ufficio) con offset
operativo (campo) · non assumere l'ordine Est/Nord nel TXT senza verifica.
