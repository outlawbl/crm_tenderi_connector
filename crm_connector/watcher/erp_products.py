from configparser import ConfigParser
from crm_connector.settings import BASE_DIR
import os
import pyodbc as pyodbc

# data_file = './config.ini'
data_file = os.path.join(BASE_DIR, 'config.ini')
config = ConfigParser()
config.read(data_file)

pantheon_driver = config['db_config']['pantheon_driver']
pantheon_server = config['db_config']['pantheon_server']
pantheon_database = config['db_config']['pantheon_database']
pantheon_username = config['db_config']['pantheon_username']
pantheon_password = config['db_config']['pantheon_password']

db = pyodbc.connect(driver=pantheon_driver, server=pantheon_server, database=pantheon_database, user=pantheon_username, password=pantheon_password, charset='UTF-8')


# db = pyodbc.connect(driver=driver, server=server, database=database, user=username, password=password, charset='UTF-8')
cur = db.cursor()

def query_db(query, args=(), one=False):
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        return (r[0] if r else None) if one else r

select_direktno = "select S.acIdent, S.acName, S.acFieldSF, sum(K.anStock) as anStock,  S.acClassif2, C.acName as acClassif2Name, S.acCode, S.anRTPrice, S.anSalePrice, S.acFieldSA, S.acFieldSE, LTrim(RTrim(S.acTechProcedure)) As acTechProcedure, LTrim(RTrim(S.acDescr)) As acDescr from tHE_SetItem S join tHE_Stock K on S.acIdent=K.acIdent join tHE_SetItemCateg C on C.acClassif = S.acClassif2 where (K.acWarehouse='Skladište VP1 BL' or K.acWarehouse='Skladište VP SA' or K.acWarehouse='Skladište VP2 BL') and Upper(LTrim(RTrim(S.acFieldSF))) = 'DA' group by S.acIdent, S.acName, S.acFieldSF, S.acClassif2, C.acName, S.acCode, S.anRTPrice, S.anSalePrice, S.acFieldSA, S.acFieldSE, S.acTechProcedure, S.acDescr order by acIdent"

cur.execute(select_direktno)
pantheon_artikli_raw = query_db(select_direktno)

print(pantheon_artikli_raw)