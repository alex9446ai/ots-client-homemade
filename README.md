# OTS Client — semplice tool di verifica per OpenTimestamps

Questo repository contiene script Python per estrarre i passaggi crittografici da un file .ots, serializzarli in un JSON compatto e verificare localmente i risultati (OP_RETURN e Merkle Root) confrontandoli con i valori attesi dalla Blockchain Bitcoin.

## Requisiti
- Python 3.10+
- Dipendenze elencate in `requirements.txt` (installare con `pip install -r requirements.txt`).

## Installazione
1. Clona o copia il repository nella tua macchina.
2. (Opzionale) crea e attiva un virtualenv.
3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Panoramica dei file
- `__main__.py`: flusso principale che combina estrazione, serializzazione e verifica. Uso: `python __main__.py [documento_originale] [ots_file] [op_return_hex] [merkle_root_hex]`.
- `estrai_passaggi.py`: legge un file `.ots` e ritorna la rappresentazione testuale dell'albero dei passaggi; contiene anche la funzione `stampa_percorso_ots` per uso da riga di comando.
- `passaggi_come_json.py`: converte l'output testuale dei passaggi in un JSON "compatto" usato dalla logica di verifica.
- `verifica.py`: applica i passaggi crittografici al documento originale, calcola l'OP_RETURN e il Merkle Root e li confronta con i valori attesi forniti dall'utente.
- `requirements.txt`: elenca le dipendenze (`opentimestamps`, `opentimestamps-client`).

## Esempi d'uso

- Estrarre e stampare il percorso da un file `.ots`:

```bash
python estrai_passaggi.py documento.pdf.ots > passaggi.txt
```

- Convertire file di passaggi (testo) in JSON compatto:

```bash
python passaggi_come_json.py passaggi.txt > passaggi.json
```

- Verifica completa (documento originale + file .ots -> calcola e confronta OP_RETURN e Merkle Root):

```bash
python __main__.py documento.pdf documento.pdf.ots <op_return_atteso_hex> <merkle_root_atteso_hex>
```

Oppure eseguire la verifica a partire da un JSON di passaggi:

```bash
python verifica.py documento.pdf passaggi.json <op_return_atteso_hex> <merkle_root_atteso_hex>
```

Nota: gli esempi richiedono che i valori hex di OP_RETURN e Merkle Root siano forniti come stringhe esadecimali senza prefissi.

## Cosa fa il progetto (breve)
Il progetto prende un file `.ots` (OpenTimestamps), deserializza la proof, ne estrae la sequenza di operazioni crittografiche (append/prepend/sha256/etc.), la converte in JSON e applica questi passaggi all'hash del documento originale per ricavare i valori usati in Bitcoin (OP_RETURN e Merkle Root). Serve per verificare offline la corrispondenza matematica tra proof OTS e le informazioni pubblicate su blockchain.

## Avviso
Il codice è stato scritto tramite tool IA e successivamente modificato da umani. È puramente a scopo di test e studio.
