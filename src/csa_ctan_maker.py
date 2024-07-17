import pandas as pd
import numpy as np
import pdfplumber, re

def csa_ctan_maker(url: str) -> pd.DataFrame:
    
    content = read_pdf(url)

    columns = ['DATA',
            'HORARIO',
            'PRATOPRINCIPAL',
            'OVOS',
            'VEGETARIANO',
            'GUARNICAO',
            'ARROZ',
            'FEIJAO',
            'SALADA1',
            'SALADA2',
            'SUCO',
            'SOBREMESA'
            ]

    df = pd.DataFrame(content[3:], columns = columns)

    df = formating_df(df, columns)
    df = formating_data(df)
    df = formating_time_column(df)

    return df
    
    #df.to_csv('../csv/Ctan-Csa_menu.csv', index = False, encoding = 'utf-8')

def read_pdf(url: str) -> list:
    
    content:list = []

    with pdfplumber.open(url) as f:
        for i in f.pages:
            table = i.extract_table()
            if table:
                content.extend(table)
    
    return content

def formating_df(df:pd.DataFrame, columns:list)-> pd.DataFrame:

    #remove \n
    df[columns] = df[columns].replace(r'\n', '', regex = True)
    
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

def formating_data(df:pd.DataFrame)-> pd.DataFrame:

    for index in df.index:

        pattern = r'[A-z]|[^\x00-\x7F]'
        string = df.loc[index, 'DATA']
        
        if (string != None):
            teste = re.sub(pattern, '', string)
            df.loc[index, 'DATA'] = teste

    return df

def formating_time_column(df:pd.DataFrame) -> pd.DataFrame:
    
    for index in df.index:

        if (df.loc[index, 'DATA'] == '' or df.loc[index, 'DATA'] == None):
            df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']

    return df

csa_ctan_maker("../Menus/Ctan_menu_march.pdf")