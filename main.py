import codicefiscale
from datetime import datetime
import numpy as np

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari", "Ruota Nazionale"]


def calcoloCodiceFiscale():  # Controlla che che il codice fiscale inserito sia corrtetto:
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
    for i in range(11):
        mat = np.random.choice(90, (i, 5), replace=False)
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


def stampaRoute():  # Stampa i nomi delle ruote:
    for i in range(11):
        print(i+1, "Ruota", nomiRuote[i])


def scegliRuota():
    stampaRoute()
    ruota = 0
    while (ruota < 1) or (ruota > 11):
        print("Scegliere la ruota su cui puntare")
        ruota = int(input())
    return ruota


def inserisciNumeri():
    numeriScelti = []
    print('Inserisci i 5 numeri da puntare')
    for i in range(5):
        elemento = int(input())
        numeriScelti.insert(i, elemento)


codice_fiscale = calcoloCodiceFiscale()
dataNascita = getDataNascita(codice_fiscale)
dataNascita[2] = convertiAnno(dataNascita[2])
eta = calcolaEta(int(dataNascita[0]), int(dataNascita[1]), int(dataNascita[2]))
if eta >= 18:
    numeri_estratti = generaNumeriRuote()
    scriviFile(numeri_estratti)
    ruota_scelta = scegliRuota()
