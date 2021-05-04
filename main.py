import codicefiscale
from datetime import datetime
import numpy as np
from setuptools.launch import run

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari", "Ruota Nazionale"]


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
    year = datetime.now().strftime("%y")  # Assegna alla varibiale "year" solo le ultime due cifre dell'anno corrente (2021 --> 21).
    if int(anno) < int(year):
        return int(anno) + 2000
    else:
        return int(anno) + 1900


def calcolaEta(giorno, mese, anno):  # Ritorna l'età in base al codice fiscale inserito:
    today = datetime.today()
    return today.year - anno - ((today.month, today.day) < (mese, giorno))


def generaNumeriRuote():  # Genera 5 numeri compresi tra 0 e 90 per ogni ruota
    mat = np.zeros((11, 5))
    for i in range(len(mat)):
        mat[i] = np.random.choice(89, 5, replace=False) + 1
    mat = mat + 1
    print("Matrice\n", mat)
    return mat


def scriviFile(matrice):  # Viene salvata la matrice su un file con la data del giorno corrente:
    now = datetime.now()
    filename = now.strftime("NumeriVincenti_%m-%d-%Y")
    filename = f'{filename}.txt'
    file = open(filename, 'w')
    np.savetxt(file, matrice, fmt='%i', delimiter=';', newline='n')
    file.close()


def scegliModalita():  # L'utente sceglie la modalità con la quale vuole fare la sua puntata:
    modalita = 0
    while (modalita < 1) or (modalita > 10):
        print("Premi 1 per la modalita 'ESTRATTO'\nPremi 2 per la modalita 'AMBO'\nPremi 3 per la modalita 'TERNO'\nPremi 4 per la modalita 'QUATERNA'\nPremi 5 per la modalita 'CINQUINA'")
        print("Premi 6 per la modalita 'ESTRATTO SECCO'\nPremi 7 per la modalita 'AMBO SECCO'\nPremi 8 per la modalita 'TERNO SECCO'\nPremi 9 per la modalita 'QUATERNA SECCO'\nPremi 10 per la modalita 'CINQUINA SECCO'\n")
        print("Seleziona la modalità con cui vuoi fare la tua puntata:")
        modalita = int(input())
    return modalita


def stampaRoute():  # Stampa i nomi delle ruote:
    for i in range(11):
        print(i+1, "Ruota", nomiRuote[i])


def scegliRuota():  # L'utente sceglie la ruota du cui vuole fare la sua puntata:
    stampaRoute()
    ruota = -1
    while (ruota < 1) or (ruota > 11):
        print("Scegliere la ruota su cui puntare")
        ruota = int(input())
    return ruota


def scegliNumeri(numeri_da_giocare):
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


def scegliPuntata():
    puntata = -1
    while (puntata < 1) or (puntata > 200):
        print("\nInsersci l'importo della puntata, compreso tra 1€ e 200€: ")
        puntata = int(input())
    return puntata


def calcoloVincita(trovati, mod_scelta, punt_scelta):
    vincita = 0
    if mod_scelta == 1:
        vincita = 5*trovati
    elif mod_scelta == 2:
        vincita = 25*trovati
    elif mod_scelta == 3:
        vincita = 450*trovati
    elif mod_scelta == 4:
        vincita = 12000*trovati
    elif mod_scelta == 5:
        vincita = 600000*trovati
    elif (mod_scelta == 6) and (trovati >= mod_scelta-5):
        vincita = 55
    elif (mod_scelta == 7) and (trovati >= mod_scelta-5):
        vincita = 250
    elif (mod_scelta == 8) and (trovati >= mod_scelta-5):
        vincita = 4500
    elif (mod_scelta == 9) and (trovati >= mod_scelta-5):
        vincita = 120000
    elif (mod_scelta == 10) and (trovati >= mod_scelta-5):
        vincita == 6000000
    return vincita*punt_scelta


def controlloVincite(num_estratti, mod_scelta, num_scelti, r_scelta, punt_scelta):
    trovati = 0
    if mod_scelta < 6:
        for i in range(10):
            trovati_interni = 0
            for j in range(len(num_scelti)):
                if num_scelti[j] in num_estratti[i]:
                    trovati_interni += 1
            if trovati_interni >= mod_scelta:
                trovati += 1
    else:
        for i in range(len(num_scelti)):
            if num_scelti[i] in num_estratti[r_scelta-1]:
                trovati += 1
    print("\nBravo hai indovinato", trovati, "numeri")
    if trovati > 0:
        return calcoloVincita(trovati, mod_scelta, punt_scelta)
    else:
        return 0


codice_fiscale = calcoloCodiceFiscale()
dataNascita = getDataNascita(codice_fiscale)
dataNascita[2] = convertiAnno(dataNascita[2])
eta = calcolaEta(int(dataNascita[0]), int(dataNascita[1]), int(dataNascita[2]))
if eta >= 18:
    numeri_estratti = generaNumeriRuote()
    scriviFile(numeri_estratti)
    modalita_scelta = scegliModalita()
    ruota_scelta = 0
    if modalita_scelta > 5:
        ruota_scelta = scegliRuota()
    numeri_scelti = scegliNumeri(modalita_scelta)
    puntata_scelta = scegliPuntata()
    vincita_utente = controlloVincite(numeri_estratti, modalita_scelta, numeri_scelti, ruota_scelta, puntata_scelta)
    print("Hai vinto:", vincita_utente)
