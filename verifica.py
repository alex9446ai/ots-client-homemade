from hashlib import sha256
from json import loads
from pathlib import Path
from sys import argv

def reverse_bytes(hex_string: str) -> str:
    """Inverte l'ordine dei byte di una stringa esadecimale (Little/Big Endian)."""
    return bytes.fromhex(hex_string)[::-1].hex()

def verifica_crittografica(percorso_documento: str,
                           passaggi_json: str,
                           op_return_atteso: str,
                           merkle_root_atteso: str) -> bool:
    # 1. Calcola l'hash del documento originale
    print(f"--- CALCOLO HASH DEL DOCUMENTO: {percorso_documento} ---")
    bytes_documento = Path(percorso_documento).read_bytes()
    hash_documento = sha256(bytes_documento).hexdigest()
    print(f"Hash calcolato (Documento): {hash_documento}\n")

    # 2. Carica il JSON con l'albero dei passaggi
    print("--- CARICAMENTO STRUTTURA JSON ---")
    passaggi_albero = loads(passaggi_json)

    # 3. Esecuzione dei calcoli crittografici passo-passo
    print("--- ESECUZIONE DEI CALCOLI CRITTOGRAFICI ---")

    op_return = bytes()
    current_bytes = bytes.fromhex(hash_documento)
    last_sha = current_bytes

    for i, passo in enumerate(passaggi_albero, start=1):
        # Il match analizza la struttura del dizionario. 'valore_hex' viene estratto 
        # e assegnato come variabile locale solo se corrisponde al rispettivo case.
        match passo:
            case {'tipo': 'append', 'valore': str() as valore_hex}:
                adiacente_bytes = bytes.fromhex(valore_hex)
                current_bytes = current_bytes + adiacente_bytes
                print(f"Passo {i} [Append]: ({current_bytes.hex()[:10]}... + {valore_hex[:10]}...) -> {current_bytes.hex()}")

            case {'tipo': 'prepend', 'valore': str() as valore_hex}:
                adiacente_bytes = bytes.fromhex(valore_hex)
                current_bytes = adiacente_bytes + current_bytes
                print(f"Passo {i} [Prepend]: ({valore_hex[:10]}... + {current_bytes.hex()[:10]}...) -> {current_bytes.hex()}")

            case {'tipo': 'sha256'}:
                current_bytes = sha256(current_bytes).digest()
                print(f"Passo {i} [SHA256]: hash applicato -> {current_bytes.hex()}")
                last_sha = current_bytes

            case {'tipo': 'txid'}:
                op_return = last_sha

            case {'tipo': 'merkle_root'}:
                pass

            case _:
                print(f"❌ Errore: Struttura del passo {i} non valida o tipo non riconosciuto.")
                return

    op_return_calcolato = op_return.hex()
    merkle_root_calcolato = reverse_bytes(current_bytes.hex())

    # 4. Verifica e confronto finale con Bitcoin
    print("\n" + "="*70)
    print(f"OP_RETURN Calcolato:\t {op_return_calcolato}")
    print(f"OP_RETURN Atteso:\t {op_return_atteso}")
    print("\n" + "="*70)
    print(f"Merkle Root Calcolato:\t {merkle_root_calcolato}")
    print(f"Merkle Root Atteso:\t {merkle_root_atteso}")
    print("="*70 + "\n")

    if op_return_atteso == op_return_calcolato and merkle_root_atteso == merkle_root_calcolato:
        print("✅ VERIFICA RIUSCITA! La corrispondenza matematica con la Blockchain è confermata.")
        return True
    print("❌ VERIFICA FALLITA. I valori non corrispondono. Controlla i dati inseriti.")
    return False

if __name__ == "__main__":
    if len(argv) > 4:
        passaggi_json = Path(argv[2]).read_text(encoding='utf-8')
        verifica_crittografica(argv[1], passaggi_json, argv[3], argv[4])
    else:
        # Messaggio d'errore esplicito con tutti gli argomenti richiesti
        print("❌ Errore: Mancano argomenti obbligatori.")
        print("Uso corretto:")
        print("python verifica.py <documento_originale> <passaggi.json> <op_return_bitcoin> <merkle_root_bitcoin>")
