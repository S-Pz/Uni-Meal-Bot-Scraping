import pandas as pd
import numpy as np
import pdfplumber, re

months:dict = {
    
    'janeiro': '01',
    'fevereiro': '02',
    'março': '03',
    'abril': '04',
    'maio': '05',
    'junho': '06',
    'julho': '07',
    'agosto': '08',
    'setembro': '09',
    'outubro': '10',
    'novembro': '11',
    'dezembro': '12'
}

def read_pdf(file_path: str) -> list:
    
    content:list = []

    with pdfplumber.open(file_path) as f:
        for i in f.pages:
            table = i.extract_table()
            if table:
                content.extend(table)
    
    return content

def formating_df(df:pd.DataFrame, columns:list) -> pd.DataFrame:

    #remove \n
    df = df.replace(r'\n', '', regex = True)
    
    #remove empty cells
    df[columns] = df[columns].replace("", np.nan)
    df.dropna(how = 'all', inplace = True)

    #remove whitespaces in the column
    df['DATA'] = df['DATA'].replace(r'\s+', '', regex = True)
    df['OVOS'] = df['OVOS'].replace(r'\s+', '', regex = True)
    df['ARROZ'] = df['ARROZ'].replace(r'\s+', '', regex = True)

    #drop last row
    df.drop(df.index[len(df) - 1], inplace = True)

    return df

def removing_lines(df:pd.DataFrame, columns:list) -> pd.DataFrame:
     
    df = df.dropna(subset=['PRATOPRINCIPAL'], how = 'all')

    return df

def formating_date_without_time(df:pd.DataFrame, content:list)-> pd.DataFrame: # formata a data quando não vem do pdf

    mon = content[0][0].split(' ')[1].lower()

    for index in df.index:
        #pattern = r'[A-z]|[^\x00-\x7F]'
        
        if (df.loc[index, 'DATA'] != '' and df.loc[index, 'DATA'] != None):
            data:str = str(df.loc[index, 'DATA'])
            df.loc[index, 'DATA'] = re.sub(r'[^0-9]+', '/' + months[mon], data)
        else:
            df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']

    return df

def formating_time_column(df:pd.DataFrame) -> pd.DataFrame: #Formata a coluna de horário quando o pdf não vem
    
    for index in df.index:

        data:str = str(df.loc[index, 'DATA'])
        lun = re.search(r'[j]\w+', data.lower())
        
        if (lun):
            df.loc[index,'HORARIO'] = 'JANTAR'
        else:
            df.loc[index,'HORARIO'] = 'ALMOÇO'
        
    return df

def formating_date(df:pd.DataFrame):
    
    for index in df.index:

        pattern = r'[A-z]|[^\x00-\x7F]'
        string = df.loc[index, 'DATA']
        
        if (string is not None):
            
            #removing the text and let only date dd/mm
            only_date = re.sub(pattern, '', string)
            df.loc[index, 'DATA'] = only_date

    return df

def formating_time_column_2(df):

    for index in df.index:

        if (df.loc[index, 'DATA'] == '' or df.loc[index, 'DATA'] == None):
            df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']

    return df

def csa_ctan_maker(pdf_file: str):
    
    content = read_pdf(pdf_file)

    if (len(content[1]) == 11):
        
        columns = [
            'DATA', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO', 'GUARNICAO',
            'ARROZ', 'FEIJAO', 'SALADA1', 'SALADA2', 'SUCO','SOBREMESA'
        ]
        
        df = pd.DataFrame(content[3:], columns = columns)
        
        df = formating_df(df, columns)
        df = formating_time_column(df)

        df = formating_date_without_time(df, content)
        df = removing_lines(df, columns)

    elif(len(content[1]) == 12):

        columns = [
            'DATA', 'HORARIO', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO', 'GUARNICAO',
            'ARROZ', 'FEIJAO', 'SALADA1', 'SALADA2', 'SUCO','SOBREMESA'
        ]
   
        df = pd.DataFrame(content[3:], columns = columns)
        
        df = formating_df(df, columns)
        df = formating_date(df)

        df = formating_time_column_2(df)
        df = removing_lines(df, columns)

    
    dic_format = df.to_dict('index')
    
    #print(dic_format[1])

    return dic_format

    #df.to_csv('../csv/csa_menu.csv', index = False)
    
csa_ctan_maker("../Menus/csa_ctan.pdf")