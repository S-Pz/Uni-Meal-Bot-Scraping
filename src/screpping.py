import requests
from bs4 import BeautifulSoup

H = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'}

def extract_pdf(url:str, file_name:str):
    
    file_path = '../Menus/' + file_name + '.pdf'
    
    response = requests.get(url, headers=H, timeout = 25, verify=False)
    
    if (response.status_code == 200):    
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"{response.status_code}")

def obtain_menus(url:str, file_name:str):#file name without extension (pdf)
    
    try:
        response = requests.get(url, headers = H, timeout = 25, verify=False)

        if (response.status_code == 200):
            print("ok")
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            
            menu_url:str = 'https:' + table.find('a').get('href')
            
            extract_pdf(menu_url, file_name)
    
    except:
        print(url)
        return "error"