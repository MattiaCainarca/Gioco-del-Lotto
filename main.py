import codicefiscale
from datetime import datetime
import numpy as np
import os.path

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari",
             "Ruota Nazionale"]

mod1 = "Premi 1 per la modalita 'ESTRATTO'\nPremi 2 per la modalita 'AMBO'\nPremi 3 per la modalita 'TERNO'\nPremi 4 per la modalita 'QUATERNA'\nPremi 5 per la modalita 'CINQUINA'\n"
mod2 = "Premi 6 per la modalita 'ESTRATTO SECCO'\nPremi 7 per la modalita 'AMBO SECCO'\nPremi 8 per la modalita 'TERNO SECCO'\nPremi 9 per la modalita 'QUATERNA SECCO'\nPremi 10 per la modalita 'CINQUINA SECCO'\n"

vincite = [5, 25, 450, 12000, 600000, 55, 250, 4500, 120000, 6000000]


def calcoloCodiceFiscale():  # Controlla che che il codice fiscale inserito sia corretto:
    test_codice_fiscale = -1
    while not codicefiscale.isvalid(test_codice_fiscale):
        test_codice_fiscale = leggiCodiceFiscale()
    return test_codice_fiscale


def leggiCodiceFiscale():  # Richiede all'utente l'inserimento del codice fiscale:
    print("\nInserisci il tuo codice fiscale: ")
    stringa = input()
    return stringa.upper()  # Rende tutti i caratteri della stringa maiuscoli, nel caso non lo fossero.


def verificaEta(cod_fisc):  # Viene verificato se l'utente ha almeno 18 anni:
    dataNascita = getDataNascita(cod_fisc)
    dataNascita[2] = convertiAnno(dataNascita[2])
    eta = calcolaEta(int(dataNascita[0]), int(dataNascita[1]), int(dataNascita[2]))
    if eta >= 18:
        return 1
    else:
        print("Mi dispiace non hai un'età sufficiente per giocare.")
        return 0


def getDataNascita(codice):  # Restituisce la data di nascita:
    data = (codicefiscale.get_birthday(codice))  # Dal codice inserito ricava la data di nascita.
    return data.split('-')  # Divide la data di nascita in un array di tre elementi [giorno, mese, anno].


def convertiAnno(anno):  # Converte l'anno del codice fiscale in un anno con 4 cifre:
    year = datetime.now().strftime(
        "%y")  # Assegna alla varibiale "year" solo le ultime due cifre dell'anno corrente (2021 --> 21).
    if int(anno) < int(year):
        return int(anno) + 2000
    else:
        return int(anno) + 1900


def calcolaEta(giorno, mese, anno):  # Ritorna l'età in base al codice fiscale inserito:
    today = datetime.today()
    return today.year - anno - ((today.month, today.day) < (mese, giorno))


def giocoDelLotto(cod_fisc):
    salvaEstrazione()
    modalita_scelta = scegliModalita()
    ruota_scelta = 0
    if modalita_scelta > 5:
        ruota_scelta = scegliRuota()
    numeri_scelti = scegliNumeri(modalita_scelta)
    puntata_scelta = scegliPuntata()
    numeri_estratti = leggiFile()
    vincita_utente = controlloVincite(numeri_estratti, modalita_scelta, numeri_scelti, ruota_scelta, puntata_scelta)
    stampaVincita(vincita_utente)
    aggiornaFileGiocatori(cod_fisc, numeri_scelti, vincita_utente)


def salvaEstrazione():  # Viene salvata la matrice su un file con la data del giorno corrente:
    filename = fileGiornoOdierno()
    if not os.path.exists(filename):
        num_estratti = generaNumeriRuote()
        file = open(filename, 'w')
        np.savetxt(file, num_estratti, fmt='%i', delimiter=';', newline='\n')
        file.close()


def scegliModalita():  # L'utente sceglie la modalità con la quale vuole fare la sua puntata:
    modalita = 0
    while (modalita < 1) or (modalita > 10):
        print(mod1, mod2, "\nSeleziona la modalità con cui vuoi fare la tua puntata:")
        modalita = int(input())
    return modalita


def scegliRuota():  # L'utente sceglie la ruota du cui vuole fare la sua puntata:
    stampaRoute()
    ruota = -1
    while (ruota < 1) or (ruota > 11):
        print("Scegliere la ruota su cui puntare")
        ruota = int(input())
    return ruota


def stampaRoute():  # Stampa i nomi delle ruote:
    for i in range(11):
        print(i + 1, ": Ruota", nomiRuote[i])


def scegliNumeri(
        numeri_da_giocare):  # Chiede all'utente di inserire i numeri per effetturare la giocata in base alla modalità scelta:
    numeri_inseriti = []
    if numeri_da_giocare > 5:
        numeri_da_giocare -= 5
    print("\nInserisci i", numeri_da_giocare, "numeri da puntare: ")
    for i in range(numeri_da_giocare):
        numero = -1
        while (numero < 1) or (numero > 90) or not(controlloNumero(numero, numeri_inseriti)):
            print("\tInserisci un numero compreso tra 1 e 90: ")
            numero = int(input())
        numeri_inseriti.insert(i, numero)
    return numeri_inseriti


def controlloNumero(num, numeri):
    if num in numeri:
        print("\tNumero già scelto, selezionare un altro numero!")
        return 0
    return 1


def generaNumeriRuote():  # Genera 5 numeri compresi tra 0 e 90 diversi per ogni riga, per ogni ruota:
    mat = np.zeros((11, 5))
    for i in range(len(mat)):
        mat[i] = np.random.choice(89, 5, replace=False) + 1
    return mat


def scegliPuntata():  # Chiede all'utente di inserire l'importo con il quale vuole effetturare la giocata:
    puntata = -1
    while (puntata < 1) or (puntata > 200):
        print("\nInsersci l'importo della puntata, compreso tra 1€ e 200€: ")
        puntata = int(input())
    return puntata


def leggiFile():  # Legge i numeri estratti dal file dei numeri vincenti del giorno corrente:
    filename = fileGiornoOdierno()
    file = open(filename, 'r')
    matrice = np.loadtxt(file, dtype=int, delimiter=';', usecols=(0, 1, 2, 3, 4))
    return matrice


def fileGiornoOdierno():
    now = datetime.now()
    nome_file = now.strftime("NumeriVincenti_%d-%m-%Y")
    nome_file = f'{nome_file}.txt'
    return nome_file


def controlloVincite(num_estratti, mod_scelta, num_scelti, r_scelta,
                     punt_scelta):  # Vengono confrontati i numeri inseriti dall'utente con quelli dell'estrazione:
    if mod_scelta < 6:
        indovinati = controlloVinciteEstrazioni(num_scelti, mod_scelta, num_estratti)
    else:
        indovinati = controlloVinciteEstrazioniSecche(num_scelti, r_scelta, num_estratti)
    if indovinati > 0:
        return calcoloVincita(indovinati, mod_scelta, punt_scelta)
    else:
        return 0


def controlloVinciteEstrazioni(num_utente, modalita,
                               num_vincenti):  # Controlla se i numeri dell'utenti sono presenti in quelli estratti, su tutte le ruote:
    trovati = 0
    for i in range(10):
        trovati_interni = 0
        for j in range(len(num_utente)):
            if num_utente[j] in num_vincenti[i]:
                trovati_interni += 1
        if trovati_interni >= modalita:
            trovati += 1
    return trovati


def controlloVinciteEstrazioniSecche(num_utente, ruota, num_vincenti):  # Controlla se i numeri dell'utenti sono presenti in quelli estratti, sulla ruota scelta dall'utente:
    for i in range(len(num_utente)):
        if not num_utente[i] in num_vincenti[ruota - 1]:
            return 0
    return 1


def calcoloVincita(trovati, mod_scelta, punt_scelta):  # Viene calcolata la vincita in base all'importo giocato:
    return vincite[mod_scelta - 1] * trovati * punt_scelta


def stampaVincita(vincita):  # Nel caso ci fosse, viene stampata il valore della vincita:
    if vincita > 0:
        print("\nHai vinto: %d€!" % vincita)
    else:
        print("\nMi spiace non hai vinto.\nRitenta con dei nuovi numeri!")


def aggiornaFileGiocatori(cod_fisc, num_utente,
                          ammontare):  # Viene aggiunto al file dei giocatori, il codice fiscale dell'utente con la rispettiva vincita:
    now = datetime.now()
    data = now.strftime("%d-%m-%Y")
    filename = f"{data}_{cod_fisc}.txt"
    if os.path.exists(filename):
        file_utenti = open(filename, "a")
    else:
        file_utenti = open(filename, "w")
    file_utenti.write(f"{cod_fisc}, {num_utente}, {ammontare}\n")
    file_utenti.close()


def vuoiRigiocare():  # Chiede all'utente se vuole rigiocare:
    ritenta = -1
    while not (ritenta == 0 or ritenta == 1):
        print("Premi 0 se vuoi uscire oppure 1 se vuoi effetturare un'altra giocata.")
        ritenta = int(input())
    return ritenta


continua = -1
codice_fiscale = calcoloCodiceFiscale()
if verificaEta(codice_fiscale):
    while continua:
        giocoDelLotto(codice_fiscale)
        continua = vuoiRigiocare()
