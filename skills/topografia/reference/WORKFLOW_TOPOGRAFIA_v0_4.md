# WORKFLOW OPERATIVO `@Topografia`
## Bozza consolidata v0.4

**Stato:** documento di lavoro aggiornabile  
**Scopo:** raccogliere e congelare progressivamente il metodo operativo definito per il futuro plugin `@Topografia`.  
**Perimetro attuale:** workflow madre + soli playbook **Tracciamenti** e **Rilievi**.  
**Fuori perimetro per questa versione:** Poligonali, Livellazioni e qualsiasi altro playbook non esplicitamente approvato.

---

# 1. Obiettivo generale

Realizzare un unico plugin topografico richiamabile esplicitamente tramite:

```text
@Topografia
```

Il plugin deve applicare automaticamente un metodo di lavoro topografico strutturato, coerente e ripetibile, senza richiedere all’utente di ricaricare ogni volta il protocollo o di scegliere manualmente tra molte skill o molti agenti.

L’obiettivo è che l’agente lavori, per quanto possibile, **come lavorerebbe l’utente**, applicando:

- un **workflow madre** comune a tutte le task topografiche supportate;
- uno o più **playbook specifici** richiamati automaticamente in base alla lavorazione;
- controlli sugli input;
- controlli di coerenza tra elaborati;
- gestione delle incongruenze;
- workspace isolato;
- produzione di output;
- verifica finale dell’utente.

Il sistema non deve essere una collezione di molte skill separate o molti agenti concorrenti.

---

# 2. Principio di attivazione

## 2.1 Stato normale

Il plugin deve restare **inattivo** durante tutte le normali conversazioni o task non topografiche.

Stato concettuale:

```text
TOPOGRAFIA = INATTIVA
```

Il metodo topografico non deve influenzare:

- conversazioni normali;
- ricerche generiche;
- programmazione non collegata alla topografia;
- altre attività dell’utente.

## 2.2 Attivazione esplicita

L’attivazione avviene solo mediante richiamo esplicito:

```text
@Topografia
```

Esempio:

```text
@Topografia

Analizza gli allegati e creami un TXT e un DWG
con i punti necessari per il tracciamento dei muri.
```

Da quel momento viene attivato il workflow topografico per la task corrente.

## 2.3 Chiusura

Quando la task è conclusa e approvata dall’utente:

```text
TOPOGRAFIA = INATTIVA
```

Il plugin ritorna dormiente.

---

# 3. Architettura generale

L’architettura prevista è:

```text
@Topografia
    ↓
Plugin Topografia
    ↓
Workflow madre
    ↓
Riconoscimento automatico della task
    ↓
Selezione del playbook pertinente
    ↓
Controllo input e contesto
    ↓
Preparazione workspace
    ↓
Esecuzione della lavorazione
    ↓
Controlli / QC
    ↓
Gestione anomalie o incongruenze
    ↓
Produzione output
    ↓
Revisione finale dell’utente
    ↓
Chiusura task
```

## 3.1 Un solo agente principale

Per la prima architettura si prevede:

- **un solo agente principale**;
- nessun sistema multi-agent generalizzato;
- nessuna moltiplicazione di skill per ogni singola lavorazione;
- playbook modulari richiamati internamente.

## 3.2 Workflow madre

Il workflow madre contiene le regole che devono valere trasversalmente per le task topografiche supportate.

Esempi:

- capire la richiesta;
- capire il risultato finale;
- controllare gli input;
- non modificare gli originali;
- confrontare gli elaborati;
- non inventare dati mancanti;
- fermarsi sulle incongruenze bloccanti;
- produrre output verificabili;
- sottoporre il risultato alla revisione finale dell’utente.

## 3.3 Playbook

Per **playbook** si intende una procedura specifica per una determinata lavorazione topografica.

Per la versione corrente sono previsti esclusivamente:

- `Playbook Tracciamenti`
- `Playbook Rilievi`

Sono fuori perimetro:

- Poligonali;
- Livellazioni;
- GNSS come playbook autonomo;
- Monitoraggi;
- qualsiasi altro modulo non esplicitamente approvato.

Altri playbook potranno essere aggiunti solo in seguito, con decisione esplicita dell’utente.

---

# 4. Avvio automatico della task

Il comportamento previsto è il seguente.

L’utente:

1. allega uno o più file;
2. richiama `@Topografia`;
3. descrive la task.

Esempio:

```text
@Topografia

Analizza gli allegati e creami un TXT e un DWG
per il tracciamento.
```

Il sistema deve procedere automaticamente con:

```text
1. Attivazione workflow Topografia
2. Acquisizione della richiesta
3. Acquisizione degli allegati
4. Preparazione del workspace
5. Copia degli input
6. Avvio della lavorazione
7. Applicazione del workflow madre
8. Applicazione del playbook pertinente
9. Eventuali domande solo se necessarie
10. Elaborazione
11. Controlli
12. Produzione output
13. Presentazione del risultato
14. STOP per revisione finale
```

Non devono essere poste domande preventive fisse e inutili.

Le domande successive devono essere determinate dal metodo di lavoro e dalla specifica task.

---

# 5. Workspace operativo

## 5.1 Principio generale

Ogni task deve essere eseguita in un **workspace isolato**.

Gli originali non devono essere modificati.

## 5.2 Scelta della directory

Dopo il richiamo `@Topografia` e la lettura iniziale della richiesta, il sistema deve chiedere dove creare il workspace.

Directory proposta di default:

```text
Desktop reale dell’utente Windows
```

Il Desktop deve essere risolto tramite il percorso effettivo del profilo utente, evitando di assumere rigidamente:

```text
C:\Users\NOME_UTENTE\Desktop
```

perché il Desktop può essere stato reindirizzato, ad esempio tramite OneDrive.

L’utente può:

- confermare la directory proposta;
- indicare un’altra directory.

## 5.3 Nome cartella task

Dopo la scelta della directory, il sistema deve chiedere:

```text
Come vuoi chiamare la cartella della task?
```

Esempio:

```text
GN07_TRK
```

Il nome della cartella principale viene deciso dall’utente.

Il sistema non deve inventare codici progetto o nomi di commessa se non sono stati forniti.

## 5.4 Struttura del workspace

Struttura iniziale prevista:

```text
[DIRECTORY_SCELTA]
└── [NOME_TASK]
    ├── INPUT/
    ├── WORK/
    ├── OUTPUT/
    └── AUDIT/
```

### INPUT
Contiene le copie dei file sorgente utilizzati per la task.

### WORK
Contiene file intermedi, conversioni, elaborazioni e copie operative.

### OUTPUT
Contiene gli elaborati finali richiesti.

### AUDIT
Contiene controlli, anomalie, log, decisioni e informazioni utili alla tracciabilità della lavorazione.

Questa struttura potrà essere raffinata in seguito se emergerà una necessità concreta.

## 5.5 Originali intoccabili

Il sistema deve:

1. identificare i file sorgente;
2. copiarli nel workspace;
3. trattare gli originali esterni come **read-only / intoccabili**;
4. eseguire modifiche e conversioni esclusivamente sulle copie.

Regola fondamentale:

> **Mai modificare direttamente i file originali forniti dall’utente.**

## 5.6 Cartella già esistente

Se la cartella richiesta esiste già, il sistema non deve sovrascriverla automaticamente.

Deve chiedere all’utente come procedere, ad esempio:

- usare il workspace esistente;
- scegliere un nome diverso;
- creare una nuova revisione.

Nessuna rinomina arbitraria deve essere eseguita senza indicazione dell’utente.

---

# 6. Autonomia e domande

## 6.1 Principio

L’agente deve arrivare autonomamente il più possibile a un risultato completo.

Non deve interrompere continuamente l’utente per conferme banali.

## 6.2 Quando deve fare domande

Deve fare una domanda solo se manca un’informazione che:

- può cambiare materialmente il risultato;
- rende la lavorazione non verificabile;
- genera un’ambiguità progettuale;
- impedisce di scegliere correttamente il dato da utilizzare;
- costituisce una condizione di STOP prevista dal workflow.

## 6.3 Revisione finale

A fine lavorazione il sistema deve:

1. presentare risultato e output;
2. riepilogare eventuali anomalie o decisioni rilevanti;
3. fermarsi;
4. attendere la revisione dell’utente.

L’utente può:

- approvare;
- richiedere correzioni.

Flusso:

```text
ESECUZIONE
    ↓
RISULTATO
    ↓
REVISIONE UTENTE
    ├── OK → CHIUSURA
    └── CORREZIONI
            ↓
       RIELABORAZIONE
            ↓
       NUOVA REVISIONE
```

---

# 7. Principio mentale generale del metodo di lavoro

Questo è un principio centrale del metodo.

## 7.1 Se la task è un tracciamento

Prima di sviluppare punti, coordinate o quote, l’agente deve:

> **studiare gli elaborati e immaginare l’opera finita.**

Deve comprendere:

- cosa deve essere costruito;
- forma finale;
- relazioni tra gli elementi;
- sequenza costruttiva;
- quali elementi devono essere materializzati in campo.

Il sistema non deve partire direttamente dalla geometria CAD senza capire l’opera.

## 7.2 Se la task è un rilievo

Prima di rilevare o pianificare ciò che deve essere rilevato, l’agente deve:

> **immaginare come il terreno o l’opera dovranno essere restituiti in ufficio una volta terminato il rilievo.**

Deve quindi ragionare su ciò che servirà per ottenere una restituzione finale completa.

---

# 8. Primo playbook in definizione: Tracciamento

Il contenuto seguente rappresenta il metodo raccolto finora per il caso di tracciamento di muri/fondazioni a partire da elaborati progettuali.

Non è ancora il playbook completo.

---

# 9. Lettura iniziale degli elaborati

## 9.1 Gli elaborati devono “parlare la stessa lingua”

Principio dichiarato:

> **Sezioni prospettiche, planimetria e profilo longitudinale devono parlare la stessa lingua.**

L’agente non deve leggere un singolo disegno in modo isolato quando sono disponibili più elaborati che descrivono la stessa opera.

Deve ricostruire la coerenza tra:

- planimetria;
- sezioni;
- profilo longitudinale;
- progressive;
- quote;
- geometrie;
- coordinate riportate;
- altri riferimenti progettuali disponibili.

---

# 10. Controllo preliminare dello stato di fatto

Prima di preparare il tracciamento, se dagli elaborati e dal contesto risulta pertinente, deve essere verificata l’esistenza di un rilievo dello stato di fatto / prima pianta del terreno.

Motivazione operativa emersa:

- le quote progettuali non devono essere automaticamente considerate coincidenti con la realtà fisica del terreno;
- se gli elaborati sono già in fase di utilizzo operativo, è ragionevole verificare che sia stato eseguito un rilievo iniziale.

Questo controllo non autorizza l’agente a modificare le quote progettuali.

Serve a capire il contesto reale prima della lavorazione.

---

# 11. Sequenza costruttiva prima del tracciamento del muro

Per preparare il tracciamento di muri, l’agente deve comprendere che il muro non è necessariamente il primo elemento da materializzare.

Sequenza individuata:

```text
SCAVO
↓
MAGRONE
↓
FONDAZIONE ARMATA
↓
FERRI DI RIPRESA
↓
GETTO FONDAZIONE
↓
TRACCIAMENTO / INGOMBRO MURI
```

Questa sequenza deve guidare la preparazione dei dati.

Regola:

> **Prima di generare “i punti del muro”, capire per quale fase costruttiva servono realmente i dati di tracciamento.**

---

# 12. Planimetria: primo riferimento geometrico

Per il caso descritto, la prima lettura operativa viene fatta sulla **planimetria**.

Si devono individuare:

- l’opera;
- gli ingombri;
- la fondazione;
- il magrone, se rappresentato;
- gli elementi geometrici necessari alla fase di scavo e costruzione.

Il primo riferimento geometrico dichiarato è:

> **individuare gli spigoli della fondazione o del magrone, se il magrone è rappresentato nel disegno.**

---

# 13. Quota per scavo e magrone

Per la fase di scavo, il riferimento operativo descritto è la **quota testa magrone**.

Esempio concettuale:

Se il magrone ha spessore di progetto pari a:

```text
0.20 m
```

allora il fondo scavo corrisponde a:

```text
quota testa magrone - 0.20 m
```

IMPORTANTE:

- lo spessore non deve essere inventato;
- deve essere ricavato dagli elaborati o da una fonte progettuale valida;
- l’esempio di `0.20 m` è solo un esempio fornito durante la definizione del metodo.

---

# 14. Sezioni e profilo longitudinale

## 14.1 Linee di riferimento delle sezioni

In planimetria devono, idealmente, essere rappresentate le linee di riferimento delle sezioni.

Queste linee devono permettere di capire:

- dove la sezione ha inizio;
- dove termina;
- quale sezione descrive un determinato tratto;
- per quanti metri quella sezione deve essere considerata valida;
- quando si passa, ad esempio, dalla Sezione 3 alla Sezione 4.

Se tali riferimenti non sono presenti o sono insufficienti, questa carenza deve essere rilevata e gestita dal workflow.

## 14.2 Quote nelle sezioni

Le sezioni vengono utilizzate per leggere:

- geometria verticale;
- quote assolute di cantiere;
- relazioni altimetriche tra gli elementi.

## 14.3 Conferma mediante profilo longitudinale

Le quote e le relazioni individuate nelle sezioni devono essere confermate con il **profilo longitudinale**, utilizzando le progressive.

Le progressive devono essere coerenti anche con quelle riportate in planimetria.

Flusso concettuale:

```text
PLANIMETRIA
↓
individuazione linea sezione / tratto / progressiva
↓
SEZIONE
↓
lettura geometria e quote
↓
PROFILO LONGITUDINALE
↓
conferma mediante progressive
```

---

# 15. Coordinate riportate negli elaborati

Negli elaborati moderni possono essere presenti coordinate di cantiere già scritte in planimetria.

Queste coordinate non devono essere usate automaticamente.

Regola:

> **Una coordinata annotata deve essere verificata rispetto al vertice e alla geometria a cui si riferisce.**

Motivazione operativa:

- può capitare che l’etichetta riporti coordinate riferite a un vertice diverso da quello effettivamente da tracciare;
- la presenza del testo non garantisce che quella coordinata sia quella necessaria alla task.

Il sistema deve quindi:

1. leggere la coordinata;
2. identificare a quale elemento/vertice è riferita;
3. confrontarla con la geometria;
4. evitare di usarla se il riferimento non è coerente.

---

# 16. Gestione delle incongruenze progettuali

Se planimetria, sezioni, profilo longitudinale, coordinate annotate o altri elaborati risultano tra loro discordanti:

> **l’agente non deve scegliere autonomamente quale elaborato prevale.**

Deve:

1. identificare l’incongruenza;
2. indicare gli elaborati o dati in conflitto;
3. quantificare la differenza quando possibile;
4. sospendere la parte interessata della lavorazione;
5. segnalare il problema al **Responsabile di Topografia**;
6. attendere la decisione;
7. registrare la decisione ricevuta;
8. proseguire utilizzando il dato indicato dal Responsabile.

Regola:

> **L’agente rileva e documenta l’incongruenza, ma non arbitra autonomamente tra elaborati progettuali discordanti.**

---

# 17. Distinzione fra preparazione in ufficio e materializzazione in campo

Questa distinzione è parte del metodo.

## 17.1 In ufficio

Quando si preparano i dati:

- ci si attiene agli elaborati di progetto;
- si sviluppano le geometrie necessarie;
- non si inventano offset operativi solo perché potrebbero risultare utili in campo.

## 17.2 In campo

Una volta sul posto:

- si valuta con l’assistente / responsabile operativo quale materializzazione sia più funzionale;
- se necessario si utilizzano picchetti di riferimento in offset.

Esempio:

```text
RIF. 1.00 m
```

Il picchetto deve essere chiaramente identificato come **riferimento in offset**, non come punto reale dell’opera.

Regola:

> **Il dato geometrico di progetto e la materializzazione pratica in campo sono due livelli distinti.**

---

# 18. Scelta dei punti per fondazioni

## 18.1 Fondazione rettangolare

Se la fondazione è un rettangolo semplice:

> **si sviluppano soltanto i quattro spigoli.**

Non vengono aggiunti punti intermedi inutili.

## 18.2 Fondazione irregolare

Se la fondazione presenta:

- rientranze;
- cambi di direzione;
- forma irregolare;
- geometria non definibile dai soli quattro vertici;

si sviluppano tutti i **vertici geometricamente significativi** necessari a definirla senza ambiguità.

Regola generale:

> **Usare il numero minimo di punti necessario a definire correttamente la geometria.**

---

# 19. Output, nomenclatura e struttura dei file di Tracciamento

## 19.1 Principio generale della nomenclatura

La nomenclatura deve essere **proporzionata alla complessità della task**.

Non deve essere complicata quando non serve, ma deve distinguere chiaramente:

- elemento;
- livello;
- tratto/concio;
- sequenza dei punti.

Se la lavorazione è semplice e non c’è rischio di ambiguità, è ammessa anche una numerazione semplice:

```text
1
2
3
4
5
```

Se invece occorre distinguere elementi o tratti, si usano prefissi e suffissi coerenti.

## 19.2 Convenzioni attuali

### Magrone

Prefisso preferito nel nome punto:

```text
MG
```

Esempi strutturati:

```text
MG_A1
MG_A2
MG_A3
MG_A4

MG_B1
MG_B2
...
```

Codice/descrizione nel TXT:

```text
MAG
```

La presenza di `MG_` nel nome punto non è obbligatoria in ogni singolo caso; se la task è semplice può essere usata la numerazione semplice.

### Fondazione

Prefisso:

```text
FND
```

Esempi semplici:

```text
FND1
FND2
FND3
FND4
```

In presenza di salti di quota, conci o tratti distinti indicati negli elaborati:

```text
FND_A1
FND_A2
FND_A3
FND_A4

FND_B1
FND_B2
...

FND_C1
FND_C2
...
```

Codice/descrizione:

```text
FND
```

### Muro

Prefisso attuale:

```text
MR
```

Esempi:

```text
MR1
MR2
MR3
...
```

oppure, se serve distinguere tratti/livelli:

```text
MR_A1
MR_A2
...
```

Codice attuale:

```text
MR
```

Questa convenzione potrà essere modificata se emergerà un criterio migliore.

## 19.3 Formato TXT

Il formato TXT non deve essere codificato come universale.

L’ordine delle colonne dipende:

- dalla convenzione del cantiere;
- dalla configurazione dello strumento;
- dal formato richiesto per l’importazione.

Nel cantiere attuale è usato:

```text
Nome punto, Est, Nord, Quota, Codice
```

In altri cantieri è stato usato:

```text
Nome punto, Nord, Est, Quota, Codice
```

Regola:

> Prima dell’esportazione, verificare sempre la convenzione del progetto/strumento. Se non è nota, chiedere all’utente.

Non assumere mai automaticamente l’ordine Est/Nord.

## 19.4 Esempio reale acquisito

È stato fornito un TXT reale in cui:

- i punti di fondazione sono nominati `FND_A1`, `FND_B1`, `FND_C1`, ecc.;
- il codice finale è `FND`;
- i punti magrone, in quell’esempio precedente, erano nominati soltanto `A1`, `B1`, `C1`, ecc.;
- il codice finale era `MAG`.

Per il playbook corrente si preferisce, quando utile, esplicitare anche il prefisso del magrone nel nome punto (`MG_A1`, ecc.), pur senza renderlo obbligatorio nei casi semplici.

---

# 20. Struttura CAD della preparazione dati

## 20.1 DWG di preparazione / archivio

Per ogni preparazione dati importante deve essere creato un **DWG pulito e dedicato** che costituisca la memoria tecnica della lavorazione.

Il DWG di preparazione deve contenere, quando disponibili e pertinenti:

- planimetria georeferenziata;
- geometrie effettivamente utilizzate;
- elaborati di supporto usati per sviluppare i punti;
- sezioni, dettagli e altri disegni utili disposti accanto alla planimetria;
- eventuali riquadri/rettangoli per separare e organizzare visivamente gli elaborati;
- polilinee elaborate;
- punti sviluppati;
- quote;
- layer e colori utili alla lettura.

Scopo:

> poter riaprire in futuro un singolo DWG e capire con quali elaborati e riferimenti sono stati sviluppati i punti, senza dover cercare nuovamente tutti i file originali.

Il DWG di preparazione non deve essere considerato un file intermedio da eliminare.

## 20.2 Layer

I layer vengono organizzati con prefisso comune:

```text
FIBE
```

Scopo del prefisso:

- mantenere vicini i layer creati dall’utente;
- recuperarli rapidamente nell’elenco layer di AutoCAD.

La sintassi esatta dei nomi layer non è ancora congelata in forma rigida.

Esempi concettuali:

```text
FIBE_FONDAZIONE
FIBE_MAGRONE
FIBE_MURO
```

oppure varianti più sintetiche.

Magrone, fondazione, muro e altri elementi devono poter essere distinti:

- tramite layer differenti;
- tramite colori differenti.

I colori specifici non sono fissati: vengono scelti operativamente.

## 20.3 Inserimento punti

Il metodo attuale dell’utente prevede normalmente l’uso di **Civil Design** con comando di inserimento punto continuo.

I punti vengono inseriti come riferimenti/blocchi secondo il comportamento del software.

Per ogni punto sono gestiti almeno:

- nome;
- coordinate;
- quota;
- codice.

La quota può essere aggiornata successivamente se inizialmente non è nota.

Questa è una modalità operativa attuale, non un vincolo assoluto di implementazione del futuro plugin.

## 20.4 Geometria di riferimento

Nel DWG di preparazione deve rimanere la geometria necessaria a comprendere il tracciamento.

Non devono rimanere soltanto i punti.

---

# 21. DXF operativo di campo

Dopo la preparazione del DWG completo, viene creato un file **ancora più pulito**, destinato all’uso operativo in campo.

Formato attuale:

```text
DXF AutoCAD 2013
```

Il DXF deve contenere soltanto quanto utile sullo strumento o nel software da campo:

- polilinee;
- polilinee 3D, se necessarie;
- ingombri;
- riferimenti utili;
- geometrie necessarie alla lavorazione.

I punti vengono esportati separatamente nel TXT.

## 21.1 Pulizia obbligatoria del DXF

Prima di considerare pronto il DXF:

1. eseguire `PURGE`;
2. eseguire `VERIFICA / AUDIT`;
3. eliminare definizioni e layer inutilizzati;
4. correggere eventuali errori del disegno;
5. esplodere i blocchi quando non servono come blocchi;
6. mantenere, per quanto possibile, entità semplici e compatibili;
7. privilegiare polilinee e polilinee 3D.

Obiettivo:

> produrre un DXF leggero, pulito e compatibile con l’uso in campo.

Il controllo di compatibilità viene normalmente concluso in AutoCAD; non è prevista come obbligatoria una pre-verifica preventiva direttamente nello strumento.

---

# 22. QC finale dei punti di Tracciamento

Prima dell’esportazione definitiva del TXT, eseguire un controllo punto per punto su:

- nome punto;
- coordinata Est;
- coordinata Nord;
- quota;
- codice;
- posizione del punto rispetto alla geometria;
- duplicati;
- ordine logico dei punti;
- eventuali punti mancanti.

Regola:

> Il TXT non è pronto solo perché i punti esistono: deve essere eseguito un QC completo prima dell’export.

---

# 23. File di supporto per la Stazione Totale

Quando la lavorazione verrà eseguita con stazione totale, il topografo utilizza anche un TXT con i capisaldi.

Schema minimo attuale:

```text
Nome punto, Est, Nord, Quota
```

Questo file serve alla fase operativa sullo strumento.

Per il futuro plugin il focus resta la **preparazione dati in ufficio**.

Per GNSS/GPS è stata citata la necessità di una calibrazione, ma formato e procedura non sono ancora stati definiti e restano fuori da questa versione.

---

# 24. Confine operativo del Playbook Tracciamenti

Il playbook è focalizzato principalmente sulla **preparazione dati in ufficio**.

La conduzione pratica del tracciamento sul campo resta responsabilità del topografo.

Ciclo complessivo di riferimento:

```text
PREPARAZIONE DATI IN UFFICIO
↓
DWG di preparazione / archivio
↓
TXT punti
↓
DXF operativo
↓
eventuale TXT capisaldi
↓
TRACCIAMENTO IN CAMPO
↓
RAT - Rapportino di Attività Topografica
↓
firma dell’assistente
↓
RIENTRO IN UFFICIO
↓
restituzione dei punti effettivamente tracciati
↓
DWG chiaro e leggibile dei punti tracciati
↓
invio al Responsabile Topografia
+ RAT
```

La parte di campo non deve essere trasformata in un workflow rigido del plugin.

Se in campo un punto non è materializzabile come previsto, il topografo può:

- adattarsi con i riferimenti disponibili, se la soluzione è affidabile;
- oppure rientrare in ufficio e rigenerare i punti.

Questa decisione resta operativa e non viene automatizzata dal playbook.

---

# 25. Playbook Rilievi — principio generale

Il playbook Rilievi è focalizzato soprattutto sulla **restituzione e organizzazione in ufficio**.

Principio mentale:

> Prima di rilevare, immaginare già come il rilievo dovrà essere restituito al computer.

La restituzione può essere:

- 2D;
- 3D;
- layerizzata;
- con DTM;
- con sezioni;
- con eventuali calcoli di volume, se richiesti dalla commessa.

Nel cantiere attuale non vengono eseguiti normalmente calcoli di volume; in altri cantieri possono essere richiesti.

La complessità della restituzione dipende dallo scopo del rilievo.

---

# 26. Preparazione preliminare del Rilievo

Di norma il Responsabile Topografia indica:

- zona;
- luogo;
- obiettivo del rilievo.

Se il rilievo viene eseguito con stazione totale, prima dell’uscita si verifica la disponibilità di capisaldi nella zona.

Metodo attuale:

1. cercare i capisaldi disponibili sul server;
2. visualizzarne la posizione in AutoCAD;
3. usare Google Earth, Google Maps o strumenti equivalenti per capire dove ricadono fisicamente;
4. scegliere il caposaldo più pratico da utilizzare sul posto.

Questa parte serve alla preparazione, ma non è il nucleo principale del playbook d’ufficio.

---

# 27. Principio di acquisizione: minimo lavoro utile, massima qualità della restituzione

Nel rilievo non si cerca di acquisire il maggior numero possibile di punti.

Principio:

> rilevare il minimo necessario per ottenere una restituzione completa, leggibile e fedele.

Elementi tipici:

- bordi;
- cigli;
- muri;
- pozzetti;
- scarpate;
- punti di rottura del terreno;
- asse;
- piano scavo;
- magrone;
- ingombri;
- altri elementi realmente necessari allo scopo.

Esempi operativi:

### Pozzetto
Un pozzetto rettangolare può essere rilevato anche con tre spigoli se questo è sufficiente a ricostruirlo senza ambiguità.

### Scarpata
Rilevare:

- testa;
- piede, quando possibile e determinabile.

### Terreno / movimento terra
Se il rilievo serve a descrivere un’area scavata o un movimento terra, rilevare principalmente la superficie e le rotture necessarie a ricostruire correttamente l’area.

---

# 28. Nomenclatura e codici di campagna — riferimento non vincolante

La parte di campagna non è il focus del plugin, ma il metodo attuale utilizza:

- numerazione progressiva tipo `RIL1`, `RIL2`, `RIL3`, ...;
- codici per riconoscere il significato dei punti.

Esempi forniti:

```text
TS  = testa scarpata
PD  = piede scarpata
PZ  = pozzetto
C   = ciglio
ST  = strada
AX  = asse
PS  = piano scavo
TM  = magrone
ING = ingombro
```

Questi codici rappresentano il metodo personale attuale e non sono ancora fissati come standard universale.

---

# 29. Restituzione del Rilievo in ufficio

Dopo il rientro dal campo:

1. esportare i dati rilevati in TXT;
2. importare i punti in AutoCAD tramite Civil Design;
3. usare il formato previsto dalla commessa/strumento;
4. ricostruire le geometrie collegando correttamente i punti;
5. interpretare i codici;
6. organizzare il disegno in layer;
7. produrre la restituzione 2D o 3D secondo lo scopo;
8. generare il DTM se utile;
9. produrre eventuali sezioni o altre elaborazioni se richieste;
10. rendere il DWG chiaro e leggibile;
11. aggiungere riferimenti di orientamento utili alla lettura;
12. inviare il risultato al Responsabile Topografia;
13. conservarlo sul server.

Nel contesto attuale, come riferimento grafico possono essere inserite anche indicazioni di orientamento territoriale, ad esempio frecce verso `Messina` e `Catania`, quando aiutano a comprendere immediatamente la posizione e l’orientamento del rilievo.

Questi riferimenti sono strumenti di leggibilità, non una regola universale.

---

# 30. QC della restituzione del Rilievo

Prima dell’invio al Responsabile Topografia, verificare:

- presenza e correttezza dei layer;
- presenza delle polilinee necessarie;
- distinzione grafica tra polilinee e facce 3D;
- coerenza visiva e geometrica della restituzione;
- fedeltà rispetto alla situazione realmente osservata;
- confronto con le fotografie scattate durante il rilievo.

## 30.1 Confronto con rilievi precedenti

Se esistono rilievi precedenti della stessa zona, il confronto è utile **solo quando ha senso**.

Non deve essere usato come controllo di uguaglianza.

Esempi:

- può aiutare a individuare un errore o un’anomalia;
- può chiarire differenze sospette tra due campagne;
- non deve essere interpretato come errore se il terreno è realmente cambiato;
- nei lavori di movimento terra o contabilità le differenze possono essere perfettamente normali.

Regola:

> Il confronto con rilievi precedenti è diagnostico e contestuale, non un criterio automatico di validità.

Non deve bloccare automaticamente la consegna se non è richiesto dalla procedura della commessa.

---

# 31. Filosofia operativa del Playbook Rilievi

Il rilievo non termina quando sono stati acquisiti i punti.

Termina quando i punti sono stati trasformati in un elaborato:

- comprensibile;
- fedele;
- leggibile;
- layerizzato;
- proporzionato allo scopo;
- utile al Responsabile Topografia e alle lavorazioni successive.

Principio riassuntivo:

> Meno punti inutili, più informazione utile e maggiore qualità della restituzione finale.

---

# 32. Metadati minimi del DWG finale di Rilievo

Nel DWG finale di restituzione vengono riportati almeno:

- **data del rilievo**;
- **zona / opera**.

Per i rilievi ordinari come quelli di area, terreno, vasche, ponti tubo o altre restituzioni generiche:

- non è previsto automaticamente un RAT;
- il RAT non deve essere richiesto dal playbook salvo casi specifici.

---

# 33. Sottocaso: rilievo di controllo cassero pila

Il rilievo del cassero di una pila non deve essere trattato come un semplice rilievo generico.

## 33.1 Geometria teorica e geometria reale

Nel caso di una pila con geometria curva o ellittica non si cercano spigoli inesistenti.

Il metodo è:

1. rilevare in campo il cassero;
2. importare i punti rilevati in ufficio;
3. predisporre una **geometria teorica pulita di progetto**;
4. sovrapporre i punti reali alla geometria teorica;
5. verificare lo scostamento di ciascun punto rispetto alla forma teorica;
6. rendere graficamente leggibile il confronto.

## 33.2 Scostamento planimetrico

Accanto a ciascun punto di controllo viene riportato lo **scostamento planimetrico** rispetto alla geometria teorica.

Esempio concettuale:

```text
+0.03 m
```

Il valore riportato non rappresenta la quota altimetrica del punto, ma la distanza/scostamento planimetrico dalla geometria teorica di riferimento.

Scopo:

> permettere al Responsabile Topografia di vedere immediatamente come il cassero reale si dispone rispetto alla forma teorica e quanto risulta deformato o fuori posizione rispetto al riferimento geometrico.

Il metodo di segno positivo/negativo, la direzione dello scostamento e la convenzione grafica devono ancora essere definiti in modo esplicito prima di automatizzarli.

---

# 34. Sottocaso: rilievo ferri prima del cassero

Prima del montaggio del cassero può essere richiesto il rilievo delle armature / ferri.

Lo scopo non è soltanto rappresentare i ferri, ma verificare la loro posizione rispetto alla geometria teorica dell'elemento strutturale.

Metodo:

1. rilevare i ferri significativi;
2. importare i punti in ufficio;
3. sovrapporre il rilievo alla geometria teorica del cassero / pila;
4. verificare la distanza tra armatura rilevata e geometria teorica;
5. usare questa distanza per controllare il **copriferro disponibile**.

## 34.1 Valore del copriferro

Il valore richiesto:

- non deve essere assunto automaticamente;
- non deve essere fissato dal playbook;
- deve essere ricavato dagli elaborati, dal progetto o dalle specifiche valide della commessa.

Valori come `5 cm`, `10 cm` o altri sono esempi possibili emersi durante la definizione del metodo, non regole universali.

Regola:

> il playbook deve verificare il copriferro rispetto al valore progettuale effettivamente applicabile alla lavorazione corrente.

---



# 35. Convenzioni grafiche per rilievi di controllo ferri e cassero

## 35.1 Quote di scostamento punto per punto

Per i rilievi di controllo di **ferri** e **cassero**, lo scostamento rispetto alla geometria teorica viene rappresentato graficamente con:

- `Quota allineata`;
- oppure `Quota lineare`.

La distanza viene riportata **punto per punto**.

La posizione grafica della quota deve aiutare a leggere immediatamente il verso dello scostamento:

- se il punto rilevato è **fuori sagoma**, la quota viene posizionata all’esterno, dal lato in cui cade realmente il punto;
- se il punto rilevato è **dentro sagoma**, la quota viene lasciata all’interno.

Questa convenzione vale sia per il rilievo ferri sia per il rilievo cassero.

---

# 36. Layerizzazione temporale e per tipologia

Ogni campagna di rilievo deve restare identificabile nel tempo.

I punti e le polilinee rilevate devono essere organizzati su layer che permettano di distinguere almeno:

- data del rilievo;
- tipologia del rilievo;
- geometria teorica.

Esempi concettuali:

```text
RIL_FERRO_2026-09-14
RIL_CASSERO_2026-09-15
SAGOMA_PROGETTO
```

La sintassi esatta del nome layer non è ancora fissata in modo rigido.

## 36.1 Colori

Ferro, cassero e sagoma teorica devono risultare graficamente distinguibili.

I colori:

- possono essere differenti;
- sono scelti operativamente;
- non costituiscono uno standard fisso del playbook.

Esempi citati durante la definizione del metodo:

- magenta;
- rosso;
- blu;
- bianco.

La regola è la leggibilità, non il colore specifico.

---

# 37. Polilinea del rilievo reale

Per ferri e cassero, la polilinea reale viene costruita **unendo direttamente i punti rilevati**.

Non viene ricostruita una geometria teorica alternativa.

Regola:

> la polilinea reale deve passare per i punti acquisiti e rappresentare la forma effettivamente rilevata.

---

# 38. Controlli aggiuntivi non obbligatori

Il controllo del:

- centro;
- asse;
- eventuale modello 3D finale;

non è obbligatorio nel flusso minimo.

Viene eseguito:

- solo se necessario;
- solo se richiesto;
- oppure come elaborazione aggiuntiva dell’utente.

## 38.1 Modello 3D finale della pila

L’utente può conservare i diversi rilievi successivi della stessa pila/elevazione e unirli successivamente per costruire un modello 3D complessivo.

Questa attività:

- è opzionale;
- non fa parte dell’output minimo obbligatorio;
- può essere utile a fine opera o quando viene richiesta successivamente.

---

# 39. Criterio di chiusura del rilievo di controllo

Per i rilievi ferri/cassero, il rilievo può essere considerato pronto quando il DWG contiene in modo chiaro e coerente:

- punti rilevati;
- planimetria/restituzione;
- layer distinti;
- geometria teorica;
- polilinea reale;
- scostamenti punto per punto quando richiesti;
- informazioni sufficienti a comprendere il confronto tra reale e teorico.

Se il DWG è graficamente chiaro, coerente con il rilievo e leggibile dal Responsabile Topografia, non sono richiesti ulteriori controlli specifici.

---

# 40. Convenzione corrente per il nome file dei rilievi

La convenzione corrente è:

```text
DATA_WBS_ELEMENTO_TIPO_RILIEVO
```

Esempio:

```text
260914_VI05_P4_RIL_CASS.DWG
```

dove:

- `260914` = data del rilievo;
- `VI05` = **WBS** dell’opera;
- `P4` = elemento / pila;
- `RIL_CASS` = tipo di rilievo.

Questa è una convenzione corrente di cantiere e non deve essere assunta come standard universale per ogni commessa.

---

# 41. Consegna al Responsabile Topografia

Per i rilievi descritti in questo workflow, la consegna standard al Responsabile Topografia è:

```text
DWG finale
```

Il TXT dei punti non viene inviato come consegna standard.

---

# 42. Archivio interno della lavorazione di rilievo

Per ogni rilievo vengono conservati internamente:

- **DWG finale**;
- **TXT originale dei punti**;
- possibilmente un **DWG di supporto / preparazione** contenente i dati e gli elaborati di riferimento effettivamente utilizzati.

Gli elaborati originali di progetto restano nelle loro cartelle ufficiali.

Nel DWG di supporto/preparazione vengono inseriti solo gli elementi utili alla specifica lavorazione, secondo la stessa logica già definita per la preparazione dati dei tracciamenti.

Scopo:

> poter ricostruire in futuro come è stata eseguita la restituzione senza duplicare inutilmente l’intero archivio progettuale.

---

# 43. Decisioni consolidate

## D-01 — Obiettivo generale
Creare un protocollo generale di workflow topografico per un agente IA, applicabile a più lavorazioni.

## D-02 — Architettura
Adottare:

```text
WORKFLOW MADRE + PLAYBOOK SPECIFICI
```

e non un unico prompt monolitico contenente tutto.

## D-03 — Contenitore operativo
Realizzare un unico sistema/plugin Topografia che applichi automaticamente il metodo senza dover ricaricare ogni volta il protocollo.

## D-04 — Ingresso unico
Utilizzare un unico ingresso esplicito:

```text
@Topografia
```

Task e allegati vengono forniti dall’utente; il sistema riconosce automaticamente il tipo di lavorazione.

## D-05 — Revisione
L’agente lavora autonomamente fino al risultato, salvo condizioni realmente bloccanti, poi si ferma per la revisione finale dell’utente.

## D-06 — Workspace isolato
Ogni task utilizza copie di lavoro. Gli originali non vengono modificati.

## D-07 — Directory e cartella task
Directory proposta di default: Desktop reale dell’utente.  
Il nome della cartella task viene deciso dall’utente.

## D-08 — Avvio automatico
Dopo:

```text
@Topografia + task + allegati
```

il sistema prepara il workspace, copia gli input e avvia automaticamente il metodo pertinente.

## D-09 — Plugin dormiente
Il plugin resta inattivo finché non viene richiamato esplicitamente con `@Topografia`.

## D-10 — Metodo operativo
Il metodo viene ricostruito progressivamente attraverso casi reali e regole operative dell’utente.

### D-10.0 — Modello mentale
- tracciamento → immaginare l’opera finita;
- rilievo → immaginare la restituzione finale.

### D-10.1 — Coerenza elaborati
Planimetria, sezioni e profilo longitudinale devono parlare la stessa lingua.

### D-10.2 — Stato di fatto
Verificare, quando pertinente, l’esistenza di un rilievo iniziale / prima pianta.

### D-10.3 — Sequenza costruttiva
Comprendere cosa deve essere realizzato prima del muro: scavo, magrone, fondazione, ferri di ripresa, getto, muro.

### D-10.4 — Primo riferimento geometrico
Individuare gli spigoli della fondazione o del magrone se rappresentato.

### D-10.5 — Ufficio vs campo
In ufficio si prepara il dato progettuale; in campo si può decidere l’uso di offset se funzionale.

### D-10.6 — Determinazione altimetrica
Usare planimetria, linee di sezione, sezioni, progressive e profilo longitudinale in modo incrociato.

### D-10.7 — Coordinate annotate
Non fidarsi automaticamente delle coordinate scritte sul disegno; verificare il vertice a cui appartengono.

### D-10.8 — Incongruenze
In caso di conflitto tra elaborati, escalation al Responsabile di Topografia.

### D-10.9 — Punti da sviluppare
Sviluppare solo i punti geometricamente necessari.

### D-10.10 — Fondazione rettangolare
Usare i quattro spigoli.

### D-10.11 — Fondazione irregolare
Usare tutti i vertici geometricamente significativi necessari.

---


### D-10.12 — Tracciabilità temporale dei rilievi
Ogni campagna di rilievo deve restare identificabile tramite layer/data.

### D-10.13 — Rilievi ferri/cassero
Ferro, cassero e sagoma teorica devono essere separati su layer distinti; gli scostamenti vengono rappresentati punto per punto con quote lineari/allineate.

### D-10.14 — Output minimo rilievo di controllo
Se il DWG è chiaro, coerente e leggibile, il rilievo è pronto senza ulteriori controlli obbligatori.

### D-10.15 — Nome file rilievo
Schema corrente: `DATA_WBS_ELEMENTO_TIPO_RILIEVO`.

### D-10.16 — Consegna
Al Responsabile Topografia viene inviato il solo DWG finale.

### D-10.17 — Archivio rilievo
Conservare DWG finale, TXT originale e, quando utile, DWG di supporto/preparazione; gli originali di progetto restano nelle cartelle ufficiali.


# 44. Regole da non violare

Finché non verranno eventualmente modificate esplicitamente:

1. non modificare gli originali;
2. non inventare quote;
3. non inventare coordinate;
4. non inventare spessori;
5. non scegliere autonomamente tra elaborati progettuali discordanti;
6. non generare punti inutili;
7. non confondere preparazione dati in ufficio con decisioni operative prese in campo;
8. non attivare il workflow Topografia senza richiamo esplicito;
9. limitare il perimetro ai soli playbook **Tracciamenti** e **Rilievi**;
10. non assumere automaticamente l’ordine Est/Nord nei TXT;
11. non imporre una nomenclatura complessa quando la task è semplice;
12. non considerare il workflow attuale completo: è una bozza incrementale.

---

# 45. Parti ancora da definire

- criteri automatici per capire quando il controllo di centro/asse è necessario;

- convenzione formale per eventuale segno positivo/negativo degli scostamenti;

- sintassi definitiva dei nomi layer per rilievi di controllo;


Il documento dovrà essere aggiornato progressivamente con:

- sintassi definitiva dei nomi layer `FIBE_*`;
- eventuali regole definitive per il codice `MR`;
- controlli geometrici e altimetrici finali da automatizzare;
- gestione revisioni progettuali;
- criteri di validazione automatica degli output;
- gestione degli elaborati mancanti;
- procedure di STOP dettagliate;
- contenuto e struttura dell’AUDIT;
- eventuale gestione futura della calibrazione GNSS, se entrerà nel perimetro;
- implementazione tecnica del plugin;
- tool locali necessari;
- automazione reale dei formati DWG/DXF/TXT;
- integrazione con AutoCAD/Civil Design o strumenti equivalenti;
- test del plugin su casi reali di Tracciamento;
- test del plugin su casi reali di Rilievo.

---

# 46. Metodo di aggiornamento del documento

Questo file deve essere trattato come **documento vivo e versionato**.

Modalità concordata:

- continuare l’intervista sul metodo operativo;
- aggiornare questo file periodicamente, indicativamente ogni 10–15 domande o a chiusura di un blocco logico;
- non creare decine di documenti paralleli;
- mantenere un documento principale aggiornato;
- utilizzare il documento consolidato come base per la realizzazione del plugin `@Topografia`.

---

**Fine bozza v0.4**
