import requests
import schedule 
import time

from bs4 import BeautifulSoup

urls:dict = {

    'csa_ctan': 'https://ufsj.edu.br/proae/ru-ctan.php',
    'cco': 'https://ufsj.edu.br/proae/r-cco.php',
    'cap': 'https://ufsj.edu.br/proae/r-cap.php',
    'cdb': 'http://www.ufsj.edu.br/proae/ru_cdb.php',
    'csl': 'https://ufsj.edu.br/proae/r-csl.php'

}

def extract_pdf(url:str, file_name:str):
    
    file_path = '../Menus/' + file_name + '.pdf'
    response = requests.get(url)
    if (response.status_code == 200):    
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"{response.status_code}")

def obtain_menus(url:str, file_name:str):#file name without extension (pdf)

    response = requests.get(url)

    if (response.status_code == 200):

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        menu_url:str = 'https:' + table.find('a').get('href')
        
        extract_pdf(menu_url, file_name)

    else:
       print(f"{response.status_code}")


###1
# SEPAR OS CÓDIGOS: EXTRAIR DADOS E MONTAR O CSV 
# SEPARAR OS CÓDIGOS: PARA O A APLICACAO DO BOT

###2
###OBS 2.1:
#SALVAR OS ARQUIVOS EM DISCO, USANDO O SQLITE E REALIZAR  SEU CONSUMO

###2.2
#VER OS ENDPOINTS DA APLICAÇÃO DA BILBLITECA DO BOT

###2.3
#USAR O RENDER PARA UPAR O BOT, E O CORON JOB AMARADO A UM WEBHOOK DO GITHUB

# def making_csv():
#     t=0
#     while True:
        
#         print(t)
#         for i in urls:
#             print(f'Obtaining {i} menu...')
#             #obtain_menus(str(urls[i]), str(i))

#         time.sleep(1800)
#         t+=1
obtain_menus(urls['csa_ctan'], 'csa_ctan')