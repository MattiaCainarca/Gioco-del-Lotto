import codicefiscale
from datetime import datetime
import numpy as np

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari", "Ruota Nazionale"]


def calcoloCodiceFiscale():
    codice_fiscale_inserito = -1
    while not codicefiscale.isvalid(codice_fiscale_inserito):
        print("\n\nInserisci il tuo codice fiscale: ")
        codice_fiscale_inserito = input()
        codice_fiscale_inserito = codice_fiscale_inserito.upper()
    return codice_fiscale_inserito


def getDataNascita(codice):
    data = (codicefiscale.get_birthday(codice))
    return data.split('-')


def convertiAnno(anno):
    if int(anno) < 21:
        anno = int(anno) + 2000
    else:
        anno = int(anno) + 1900
    return anno


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


codice_fiscale = calcoloCodiceFiscale()
dataNascita = getDataNascita(codice_fiscale)
dataNascita[2] = convertiAnno(dataNascita[2])
eta = calcolaEta(int(dataNascita[0]), int(dataNascita[1]), int(dataNascita[2]))
print(eta)
mat = np.random.randint(1, 91, (11, 5))  # Matrice delle ruote
print(mat)
scriviFile(mat)
