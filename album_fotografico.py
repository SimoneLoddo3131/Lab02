def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            header = f.readline()
            if not header:
                return album
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                parti = [p.strip() for p in riga.split(",")]
                if len(parti) < 5:
                    continue
                codice = parti[0]
                titolo = parti[1]
                autore = parti[2]
                mese = int(parti[3])
                anno = int(parti[4])
                foto = {
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese,
                    "anno": anno
                }

                anno_trovato = None
                for elemento in album:
                    if elemento[0] == anno:
                        anno_trovato = elemento
                        break
                if anno_trovato is not None:
                    anno_trovato[1].append(foto)
                else:
                    album.append([anno, [foto]])
            return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if not (1 <= mese <= 12):
        return None

    if cerca_foto(album, codice) is not None:
        return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for elemento in album:
        foto_dell_anno = elemento[1]
        for foto in foto_dell_anno:
            if foto["codice"] == codice:
                return f"{foto['codice']},  {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for elemento in album:
        if elemento[0] == anno:
            titoli = [foto["titolo"] for foto in elemento[1]]
            titoli.sort()
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
