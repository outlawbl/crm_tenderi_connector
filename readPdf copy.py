import fitz
import pprint
import re

 
def readPdf(file_location):
    text = ''

    podaci = {}

    with fitz.open(file_location) as fajl:
        for i in fajl:
            text += i.get_text()

        niz_redova = text.split('\n')
        niz_redova = [i for i in niz_redova if i != ' ']
        niz_redova = [i for i in niz_redova if not re.match(r'\d\s/\s\d', i)]
    
        osnovni_podaci = {
            'assignedUserId': '1'
        }

        ind = 0

        for j in niz_redova:
            if j.startswith('II 4.a.'):
                osnovni_podaci['name'] = niz_redova[ind+1]
                ind += 1
            elif j.startswith('II 3.c.') or j.startswith('II 6.a.'):
                osnovni_podaci['procjenjenaVrijednostPostupka'] = niz_redova[ind+1]
                ind += 1
            elif j.startswith('OBAVJEŠTENJE O NABAVCI'):
                osnovni_podaci['brojPostupka'] = niz_redova[ind+1]
                ind += 1
            elif j.startswith('IV 7.'):
                osnovni_podaci['rokZaPredaju'] = niz_redova[ind+2]
                ind += 1
            elif j.startswith('IV 8.'):
                osnovni_podaci['datumVrijemeOtvaranja'] = niz_redova[ind+4]
                ind += 1
            elif j.startswith('IV 5.'):
                osnovni_podaci['isEaukcija'] = niz_redova[ind+1]
                ind += 1
            else:
                ind += 1

        podaci['osnovni_podaci'] = osnovni_podaci

    pprint.pprint(podaci)
    return podaci