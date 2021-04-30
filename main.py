import codicefiscale
from datetime import datetime
import numpy as np

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari", "Ruota Nazionale"]


def calcoloCodiceFiscale():
    codice_fiscale_inserito = -1
    while not codicefiscale.isvalid(codice_fiscale_inserito):
        codice_fiscale_inserito = leggiCodiceFiscale()
    return codice_fiscale_inserito


def leggiCodiceFiscale():
    print("\nInserisci il tuo codice fiscale: ")
    stringa = input()
    return stringa.upper()


def getDataNascita(codice):
    data = (codicefiscale.get_birthday(codice))
    return data.split('-')


def convertiAnno(anno):
    if int(anno) < 21:
        return int(anno) + 2000
    else:
        return int(anno) + 1900


def calcolaEta(giorno, mese, anno):
    today = datetime.today()
    return today.year - anno - ((today.month, today.day) < (mese, giorno))


def scriviFile(matrice):
    now = datetime.now()
    filename = now.strftime("NumeriVincenti_%m-%d-%Y")
    filename = f'{filename}.txt'
    file = open(filename, 'w')
    np.savetxt(file, matrice, fmt='%i', delimiter=';', newline='n', )
    file.close()


def stampaMenu():
    for i in range(11):
        print(i+1, "Ruota", nomiRuote[i])


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
    mat = np.random.choice(90, (11, 5), replace=False)
    print(mat)
    mat = mat + 1
    print(mat)
    scriviFile(mat)
    stampaMenu()
    ruotaScelta = 0
    while (ruotaScelta < 1) or (ruotaScelta > 11):
        print("Scegliere la ruota su cui puntare")
        ruotaScelta = int(input())
