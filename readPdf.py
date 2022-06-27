import fitz
import pprint
import re
import json
from datetime import datetime
from srbai.Alati.Transliterator import transliterate_cir2lat, transliterate_lat2cir

# file_location = './watch_folder/oon.pdf'

 
def readPdf(file_location):
    text = ''
    podaci = {}

    # with fitz.open(file_location) as fajl:
    document = fitz.open(file_location)
    print('reading PDF...')
    for i in document:
        text += i.get_text()

    niz_redova = text.split('\n')
    niz_redova = [i for i in niz_redova if i != ' ']
    niz_redova = [i for i in niz_redova if not re.match(r'\d\s/\s\d', i)]

    osnovni_podaci = {
        'assignedUserId': '1'
    }
    uo = {}

    ind = 0

    for j in niz_redova:
        j = transliterate_cir2lat(j)
        if j.startswith('II 4.a.'):
            osnovni_podaci['name'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('II 3.c.') or j.startswith('II 6.a.'):
            osnovni_podaci['procjenjenaVrijednostPostupka'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('II 2. '):
            osnovni_podaci['podjelaNaLotove'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('OBAVJEŠTENJE O NABAVCI'):
            osnovni_podaci['brojPostupka'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('IV 7.'):
            rok_predaje = datetime.strptime(niz_redova[ind+2], '%d.%m.%Y. %H:%M')
            rok_predaje = json.dumps(rok_predaje, indent=4, sort_keys=True, default=str).strip('"')
            osnovni_podaci['rokZaPredajuSaVremenom'] = rok_predaje
            ind += 1
        elif j.startswith('IV 8.'):
            otvaranje = datetime.strptime(niz_redova[ind+4], '%d.%m.%Y. %H:%M')
            otvaranje = json.dumps(otvaranje, indent=4, sort_keys=True, default=str).strip('"')
            osnovni_podaci['datumVrijemeOtvaranja'] = otvaranje
            ind += 1
        elif j.startswith('IV 5.'):
            osnovni_podaci['isEaukcija'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('IDB/JIB'):
            uo['jib'] = transliterate_cir2lat(niz_redova[ind+1])
            ind += 1
        elif j.startswith('I 1.'):
            uo['name'] = transliterate_cir2lat(niz_redova[ind+2])
            ind += 1
        else:
            ind += 1

    podaci['osnovni_podaci'] = osnovni_podaci
    podaci['uo'] = uo

    # pprint.pprint(podaci)
    return podaci

# readPdf(file_location)