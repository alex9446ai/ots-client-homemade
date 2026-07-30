from json import dumps
from pathlib import Path
from sys import argv

APPEED = 'append '
PREPEND = 'prepend '
TXID = '# Transaction id '
MERKLE_ROOT = '# Bitcoin block merkle root '

def passaggi_come_json_compatto(passaggi: str) -> str:
    # 1. Legge il testo riga per riga
    righe = passaggi.splitlines()

    passaggi_rilevati = []
    primo_ramo_iniziato = False
    altri_rami_da_ignorare = False

    # 2. Analizza la stringa di ogni riga e popola una lista di dizionari Python
    for riga in righe:
        riga_pulita = riga.strip()
        if not riga_pulita:
            continue

        # Gestione delle biforcazioni (->) per isolare solo il primo ramo utile
        if "->" in riga:
            if not primo_ramo_iniziato:
                primo_ramo_iniziato = True  
                riga_pulita = riga_pulita.replace("->", "").strip()
            else:
                altri_rami_da_ignorare = True  # Blocca la lettura quando iniziano i rami successivi

        if altri_rami_da_ignorare:
            continue

        def aggiungi_a_passaggi(riga_pulita: str, start_str: str, tipo: str | None = None):
            valore = riga_pulita.replace(start_str, "")
            tipo = tipo or start_str.strip()
            passaggi_rilevati.append({"tipo": tipo, "valore": valore})

        # Mappatura testuale nei dizionari Python
        if riga_pulita.startswith(APPEED):
            aggiungi_a_passaggi(riga_pulita, APPEED)
        elif riga_pulita.startswith(PREPEND):
            aggiungi_a_passaggi(riga_pulita, PREPEND)
        elif riga_pulita == "sha256":
            passaggi_rilevati.append({"tipo": "sha256", "valore": None})
        elif riga_pulita.startswith(TXID):
            aggiungi_a_passaggi(riga_pulita, TXID, 'txid')
        elif riga_pulita.startswith(MERKLE_ROOT):
            aggiungi_a_passaggi(riga_pulita, MERKLE_ROOT, 'merkle_root')

    # 3. Serializza ogni singolo dizionario su un'unica riga senza indentazione interna
    righe_json = [f"    {dumps(passo)}" for passo in passaggi_rilevati]

    # 4. Unisce le righe separandole con una virgola e racchiudendole nelle parentesi quadre
    output_json_compatto = "[\n" + ",\n".join(righe_json) + "\n]"

    # 5. Ritorna il JSON compatto a schermo
    return output_json_compatto

if __name__ == "__main__":
    if len(argv) > 1:
        passaggi = Path(argv[1]).read_text(encoding='utf-8')
        print(passaggi_come_json_compatto(passaggi))
    else:
        print("❌ Passa il percorso del file con i passaggi estratti come argomento.")
