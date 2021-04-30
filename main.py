import codicefiscale
from datetime import date


def calcoloEta(giorno, mese, anno):
    today = date.today()
    return date.year - anno - ((today.month, today.day) < (mese, giorno))


dataNascita = (codicefiscale.get_birthday('CNRMTT02L16I441L'))
dataNascitaArray = (dataNascita.split('-'))
