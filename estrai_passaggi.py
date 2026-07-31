from io import BytesIO
from opentimestamps.core.timestamp import DetachedTimestampFile
from opentimestamps.core.serialize import StreamDeserializationContext
from sys import argv

def estrai_passaggi(percorso_ots: str) -> str:
    print("--- APERTURA FILE E DESERIALIZZAZIONE ---")

    # 1. Leggiamo il file .ots come byte grezzi
    with open(percorso_ots, "rb") as f:
        ots_bytes = f.read()

    # 2. Creiamo lo stream in memoria
    fd = BytesIO(ots_bytes)

    # 3. Avvolgiamo lo stream nel contesto richiesto dalla libreria
    ctx = StreamDeserializationContext(fd)

    # 4. Passiamo il contesto al metodo di deserializzazione
    detached_timestamp = DetachedTimestampFile.deserialize(ctx)

    # 5. Prendiamo direttamente l'oggetto timestamp senza toccare le operazioni di hash
    timestamp = detached_timestamp.timestamp

    return timestamp.str_tree()

def stampa_percorso_ots(percorso_ots: str) -> None:
    passaggi = estrai_passaggi(percorso_ots)

    print("--- INIZIO PERCORSO CRITTOGRAFICO ---")

    # 6. Stampiamo l'albero testuale dei passaggi
    print(passaggi)
    print("-------------------------------------")

if __name__ == "__main__":
    if len(argv) > 1:
        # Pesca correttamente il primo argomento stringa passato da terminale
        stampa_percorso_ots(argv[1])
    else:
        # Messaggio d'errore esplicito con tutti gli argomenti richiesti
        print("❌ Errore: Manca un argomento obbligatorio.")
        print("Uso corretto:")
        print("python estrai_passaggi.py <ots_documento_originale> > passaggi.txt")
