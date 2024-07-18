
import data_base as db

from screpping import obtain_menus
from cap_maker import cap_maker
from cdb_cco_csl_maker import cdb_cco_csl_maker
from csa_ctan_maker import  csa_ctan_maker

urls:dict = {

    'csa_ctan': 'https://ufsj.edu.br/proae/ru-ctan.php',
    'cco': 'https://ufsj.edu.br/proae/r-cco.php',
    'cap': 'https://ufsj.edu.br/proae/r-cap.php',
    'cdb': 'http://www.ufsj.edu.br/proae/ru_cdb.php',
    'csl': 'https://ufsj.edu.br/proae/r-csl.php'
}

if __name__ == '__main__':

    for i in urls:
       Return = obtain_menus(urls[i], str(i))
       
       if (Return == "error"):
           continue
    
    
    conn = db.create_database()
    db.create_table(conn)
    db.insert_data_CAP(conn, cap_maker("../Menus/cap.pdf"))
    
    conn.close()
