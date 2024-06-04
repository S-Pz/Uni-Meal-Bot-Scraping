
from screpping import obtain_menus

urls:dict = {

    'csa_ctan': 'https://ufsj.edu.br/proae/ru-ctan.php',
    'cco': 'https://ufsj.edu.br/proae/r-cco.php',
    'cap': 'https://ufsj.edu.br/proae/r-cap.php',
    'cdb': 'http://www.ufsj.edu.br/proae/ru_cdb.php',
    'csl': 'https://ufsj.edu.br/proae/r-csl.php'

}

if __name__ == '__main__':

    for i in urls:
       obtain_menus(urls[i], str(i))
    # obtain_menus(urls['csa_ctan'], 'csa_ctan')
    # obtain_menus(urls['cco'], 'cco')
    # obtain_menus(urls['cap'], 'cap')
    # obtain_menus(urls['cdb'], 'cdb')
    # obtain_menus(urls['csl'], 'csl')

