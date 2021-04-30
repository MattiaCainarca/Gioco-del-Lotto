import codicefiscale
from datetime import datetime
import numpy as np

nomiRuote = ["Torino", "Milano", "Venezia", "Genova", "Firenze", "Roma", "Napoli", "Bari", "Palermo", "Cagliari", "Ruota Nazionale"]


def calcolaEta(giorno, mese, anno):
    today = datetime.today()
    return today.year - anno - ((today.month, today.day) < (mese, giorno))


def scriviFile(mat):
    now = datetime.now()
    filename = now.strftime("NumeriVincenti_%m-%d-%Y")
    filename = f'{filename}.txt'
    file = open(filename, 'w')
    np.savetxt(file, mat, fmt='%i', delimiter=';', newline='n', )
    file.close()


dataNascita = (codicefiscale.get_birthday('CNRMTT02L16U441L'))
dataNascitaArray = (dataNascita.split('-'))
if int(dataNascitaArray[2]) < 21:
    dataNascitaArray[2] = int(dataNascitaArray[2]) + 2000
eta = calcolaEta(int(dataNascitaArray[0]), int(dataNascitaArray[1]), int(dataNascitaArray[2]))
print(eta)

mat = np.random.randint(1, 91, (11, 5))  # Matrice delle ruote
print(mat)
scriviFile(mat)
