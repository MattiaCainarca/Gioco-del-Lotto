import codicefiscale
from datetime import datetime
import numpy as np
import os.path

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari",
             "Ruota Nazionale"]

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


def calcolaEtà(giorno, mese, anno):  # Ritorna l'età in base al codice fiscale inserito:
    today = datetime.today()
    return today.year - anno - ((today.month, today.day) < (mese, giorno))


def generaNumeriRuote():  # Genera 5 numeri compresi tra 0 e 90 diversi per ogni riga, per ogni ruota:
    mat = np.zeros((11, 5))
    for i in range(len(mat)):
        mat[i] = np.random.choice(89, 5, replace=False) + 1
    return mat


def fileGiornoOdierno():
    now = datetime.now()
    nome_file = now.strftime("NumeriVincenti_%m-%d-%Y")
    nome_file = f'{nome_file}.txt'
    return nome_file


def salvaEstrazione():  # Viene salvata la matrice su un file con la data del giorno corrente:
    filename = fileGiornoOdierno()
    if not os.path.exists(filename):
        num_estratti = generaNumeriRuote()
        file = open(filename, 'w')
        np.savetxt(file, num_estratti, fmt='%i', delimiter=';', newline='\n')
        file.close()


def leggiFile():  # Legge i numeri estratti dal file dei numeri vincenti del giorno corrente:
    filename = fileGiornoOdierno()
    file = open(filename, 'r')
    matrice = np.loadtxt(file, dtype=int, delimiter=';', usecols=(0, 1, 2, 3, 4))
    return matrice


def scegliModalita():  # L'utente sceglie la modalità con la quale vuole fare la sua puntata:
    modalita = 0
    while (modalita < 1) or (modalita > 10):
        print(
            "Premi 1 per la modalita 'ESTRATTO'\nPremi 2 per la modalita 'AMBO'\nPremi 3 per la modalita 'TERNO'\nPremi 4 per la modalita 'QUATERNA'\nPremi 5 per la modalita 'CINQUINA'")
        print(
            "Premi 6 per la modalita 'ESTRATTO SECCO'\nPremi 7 per la modalita 'AMBO SECCO'\nPremi 8 per la modalita 'TERNO SECCO'\nPremi 9 per la modalita 'QUATERNA SECCO'\nPremi 10 per la modalita 'CINQUINA SECCO'\n")
        print("Seleziona la modalità con cui vuoi fare la tua puntata:")
        modalita = int(input())
    return modalita


def stampaRoute():  # Stampa i nomi delle ruote:
    for i in range(11):
        print(i + 1, "Ruota", nomiRuote[i])


def scegliRuota():  # L'utente sceglie la ruota du cui vuole fare la sua puntata:
    stampaRoute()
    ruota = -1
    while (ruota < 1) or (ruota > 11):
        print("Scegliere la ruota su cui puntare")
        ruota = int(input())
    return ruota


def scegliNumeri(
        numeri_da_giocare):  # Chiede all'utente di inserire i numeri per effetturare la giocata in base alla modalità scelta:
    numeriScelti = []
    if numeri_da_giocare > 5:
        numeri_da_giocare -= 5
    print("\nInserisci i", numeri_da_giocare, "numeri da puntare: ")
    for i in range(numeri_da_giocare):
        numero = -1
        while (numero < 1) or (numero > 90):
            print("\tInserisci un numero compreso tra 1 e 90: ")
            numero = int(input())
        numeriScelti.insert(i, numero)
    return numeriScelti


def scegliPuntata():  # Chiede all'utente di inserire l'importo con il quale vuole effetturare la giocata:
    puntata = -1
    while (puntata < 1) or (puntata > 200):
        print("\nInsersci l'importo della puntata, compreso tra 1€ e 200€: ")
        puntata = int(input())
    return puntata


def calcoloVincita(trovati, mod_scelta, punt_scelta):  # Viene calcolata la vincita in base all'importo giocato:
    return vincite[mod_scelta - 1] * trovati * punt_scelta


def controlloVinciteEstrazioni(num_utente, modalita, num_vincenti):
    trovati = 0
    for i in range(10):
        trovati_interni = 0
        for j in range(len(num_utente)):
            if num_utente[j] in num_vincenti[i]:
                trovati_interni += 1
        if trovati_interni >= modalita:
            trovati += 1
    return trovati


def controlloVinciteEstrazioniSecche(num_utente, ruota, modalita, num_vincenti):
    trovati = 0
    for i in range(len(num_utente)):
        if num_utente[i] in num_vincenti[ruota - 1]:
            trovati += 1
    if trovati >= modalita - 5:
        return 1
    else:
        return 0


def controlloVincite(num_estratti, mod_scelta, num_scelti, r_scelta,
                     punt_scelta):  # Vengono confrontati i numeri inseriti dall'utente con quelli dell'estrazione:
    if mod_scelta < 6:
        indovinati = controlloVinciteEstrazioni(num_scelti, mod_scelta, num_estratti)
    else:
        indovinati = controlloVinciteEstrazioniSecche(num_scelti, r_scelta, mod_scelta, num_estratti)
    if indovinati > 0:
        return calcoloVincita(indovinati, mod_scelta, punt_scelta)
    else:
        return 0


def stampaVincita(vincita):
    if vincita > 0:
        print("\nHai vinto: %d€!" % vincita)
    else:
        print("\nMi spiace non hai vinto.\nRitenta con dei nuovi numeri!")


def giocoDelLotto():
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
    return vincita_utente


def vuoiRigiocare():
    ritenta = -1
    while not (ritenta == 0 or ritenta == 1):
        print("Premi 0 se vuoi uscire oppure 1 se vuoi effetturare un'altra giocata.")
        ritenta = int(input())
    return ritenta


def verificaEtà(anni):
    if anni >= 18:
        return 1
    else:
        print("Mi dispiace non hai un'età sufficiente per giocare.")
        return 0


def autenticaGiocatore(cod_fisc):
    dataNascita = getDataNascita(cod_fisc)
    dataNascita[2] = convertiAnno(dataNascita[2])
    età = calcolaEtà(int(dataNascita[0]), int(dataNascita[1]), int(dataNascita[2]))
    return verificaEtà(età)


def aggiornaFileGiocatori(cod_fisc, ammontare):
    file_utenti = open("giocatori.txt", "a")
    file_utenti.write(f"{cod_fisc}, {ammontare}\n")
    file_utenti.close()


continua = -1
codice_fiscale = calcoloCodiceFiscale()
if autenticaGiocatore(codice_fiscale):
    while continua:
        vincita_attuale = giocoDelLotto()
        aggiornaFileGiocatori(codice_fiscale, vincita_attuale)
        continua = vuoiRigiocare()
