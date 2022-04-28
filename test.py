# import srbai
from srbai.Alati.Transliterator import transliterate_cir2lat, transliterate_lat2cir

lat = transliterate_cir2lat("IV 2.б. Трајање оквирног споразума bgf")
print(lat)