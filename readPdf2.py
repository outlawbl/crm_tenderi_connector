import PyPDF2
import pprint
import re
import regex
import json
from datetime import datetime, timedelta
from srbai.Alati.Transliterator import transliterate_cir2lat, transliterate_lat2cir
from pdfminer.high_level import extract_text

# file_location = './watch_folder/5d3e8bbe-ca97-4083-9ffb-31df14877013'
# def textract_read(file_location):
#     with open('example.pdf', 'rb') as f:
#     pdf_reader = PyPDF2.PdfFileReader(f)
#     for page_number in range(pdf_reader.numPages):
#         page = pdf_reader.getPage(page_number)
#         print(page.extractText())
 
def readPdf(file_location):
    text = ''
    podaci = {}

    document = extract_text(file_location)
    print(text)

    for i in document:
        text += i

    niz_redova = text.split('\n')
    # for red in niz_redova:
    #     if red == '':
    #         niz_redova.remove(red)
    niz_redova = [i for i in niz_redova if i != ' ']
    niz_redova = [i for i in niz_redova if not re.match(r'\d\s/\s\d', i)]

    osnovni_podaci = {
        'assignedUserId': '1',
        'procjenjenaVrijednostPostupka':'1'
    }
    uo = {}
    ind = 0

    for j in niz_redova:
        j = transliterate_cir2lat(j)
        if j.startswith('OBAVJEŠTENJE O NABAVCI') or j.startswith('OBAVJEŠTENjE O NABAVCI') or j.startswith('OBAVIJEST O NABAVI'):
            podaci['tip_dokumenta'] = 'Obavjestenje o nabavci'
        elif j.startswith('IZVJEŠTAJ O TOKU I ZAVRŠETKU E-AUKCIJE'):
            podaci['tip_dokumenta'] = 'Izvjestaj e-aukcije'

    if podaci['tip_dokumenta'] == 'Obavjestenje o nabavci':
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
            elif j.startswith('OBAVJEŠTENJE O NABAVCI') or j.startswith('OBAVJEŠTENjE O NABAVCI') or j.startswith('OBAVIJEST O NABAVI'):
                osnovni_podaci['brojPostupka'] = transliterate_cir2lat(niz_redova[ind+1])
                ind += 1
            elif j.startswith('IV 7.'):
                rok_predaje = datetime.strptime(niz_redova[ind+2], '%d.%m.%Y. %H:%M') - timedelta(hours=2)
                rok_predaje = json.dumps(rok_predaje, indent=4, sort_keys=True, default=str).strip('"')
                osnovni_podaci['rokZaPredajuSaVremenom'] = rok_predaje
                ind += 1
            elif j.startswith('IV 8.'):
                if niz_redova[ind+4][0].isdigit():
                    otvaranje = datetime.strptime(niz_redova[ind+4], '%d.%m.%Y. %H:%M') - timedelta(hours=2)
                elif niz_redova[ind+5][0].isdigit():
                    otvaranje = datetime.strptime(niz_redova[ind+5], '%d.%m.%Y. %H:%M') - timedelta(hours=2)
                elif niz_redova[ind+6][0].isdigit():
                    otvaranje = datetime.strptime(niz_redova[ind+6], '%d.%m.%Y. %H:%M') - timedelta(hours=2)
                otvaranje = json.dumps(otvaranje, indent=4, sort_keys=True, default=str).strip('"')
                osnovni_podaci['datumVrijemeOtvaranja'] = otvaranje
                ind += 1
            elif j.startswith('IV 5.'):
                osnovni_podaci['isEaukcija'] = transliterate_cir2lat(niz_redova[ind+1])
                ind += 1
            elif j.startswith('IDB/JIB'):
                if regex.search(r'\d{13}', niz_redova[ind+2]) != None:
                    uo['jib'] = transliterate_cir2lat(niz_redova[ind+2])
                    ind += 1
                elif regex.search(r'\d{13}', niz_redova[ind+3]) != None:
                    uo['jib'] = transliterate_cir2lat(niz_redova[ind+3])
                    ind += 1
                elif regex.search(r'\d{13}', niz_redova[ind+4]) != None:
                    uo['jib'] = transliterate_cir2lat(niz_redova[ind+4])
                    ind += 1
            elif j.startswith('I 1. Podaci o ugovornom'):
                uo_name = transliterate_cir2lat(niz_redova[ind+3])
                if not niz_redova[ind+4].isdigit():
                    uo_name += ' ' + niz_redova[ind+4]
                uo['name'] = uo_name
                ind += 1
            elif regex.search(r'(?<=^((\d*-){4}))\d+', j) != None:
                # podaci['tip_dokumenta'] = (regex.search(r'(?<=^((\d*-){4}))\d+', j)[0])
                ind += 1
            else:
                ind += 1

        podaci['osnovni_podaci'] = osnovni_podaci
        podaci['uo'] = uo

        pprint.pprint(podaci)
        return podaci
    elif podaci['tip_dokumenta'] == 'Izvjestaj e-aukcije':
        pocetna_rang_lista = []
        for j in niz_redova:
            j_orig = j
            j = transliterate_cir2lat(j)
            if j.startswith('POČETNA RANG LISTA'):
                index_pocetna_rang_lista = niz_redova.index(j_orig)
                trenutna_pozicija = 3
                while niz_redova[ind+trenutna_pozicija].isdigit() or niz_redova[ind+trenutna_pozicija] == '':
                    print(niz_redova[ind+trenutna_pozicija])
                    trenutna_pozicija += 1
                    if niz_redova[ind+trenutna_pozicija].isdigit():
                        podaci['broj_ponudjaca'] = int(niz_redova[ind+trenutna_pozicija])
               

                redni_broj = 1
                i = 0
                while i <= podaci['broj_ponudjaca']:
                    ponudjac = {}
                    ponudjac['redni broj'] = niz_redova[i+ind]
                    ponudjac['Naziv ponudjaca'] = niz_redova[i+ind+podaci['broj_ponudjaca']]
                    ponudjac['IDB/JIB'] = niz_redova[i+ind+((+podaci['broj_ponudjaca'])*2)]
                    pocetna_rang_lista.append(ponudjac)
                    i+=1

            elif j.startswith('II 3.c.') or j.startswith('II 6.a.'):
                osnovni_podaci['procjenjenaVrijednostPostupka'] = transliterate_cir2lat(niz_redova[ind+1])
                ind += 1
            else:
                ind += 1
        return podaci
    else:
        pass

# readPdf(file_location)