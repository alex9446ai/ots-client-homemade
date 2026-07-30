from sys import argv
from estrai_passaggi import estrai_passaggi
from passaggi_come_json import passaggi_come_json_compatto
from verifica import verifica_crittografica

if __name__ == "__main__":
    if len(argv) > 4:
        passaggi = estrai_passaggi(argv[2])
        passaggi_json = passaggi_come_json_compatto(passaggi)
        verifica_crittografica(argv[1], passaggi_json, argv[3], argv[4])
    else:
        # Messaggio d'errore esplicito con tutti gli argomenti richiesti
        print("❌ Errore: Mancano argomenti obbligatori.")
        print("Uso corretto:")
        print(f"python {argv[0]} [documento_originale] [ots_documento_originale] [op_return_bitcoin] [merkle_root_bitcoin]")
