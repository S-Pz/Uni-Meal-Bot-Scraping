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

    df = df.replace(r'\n', '', regex = True)
    
    #remove empty cells
    df[columns] = df[columns].replace("", np.nan)
    df.dropna(how = 'all', inplace = True)

    #remove space beetwen numbers
    df['OVOS'] = df['OVOS'].replace(r'\s+', '', regex = True)
    df['ARROZ'] = df['ARROZ'].replace(r'\s+', '', regex = True)

    return df

def removing_lines(df:pd.DataFrame) -> pd.DataFrame:#remove empty cells

    for index in df.index:

        if (df.loc[index, 'PRATOPRINCIPAL'] == None or df.loc[index, 'PRATOPRINCIPAL'] == ''):
            df = df.drop(index)
    
    return df

def formating_time_column(df:pd.DataFrame) -> pd.DataFrame: # Making the column 'HORARIO' and fill with 'ALMOCO' or 'JANTAR'
  
    for index in df.index:
        data:str = str(df.loc[index, 'DATA'])
        lun = re.search(r'[j]\w+', data.lower())
        
        if (lun):
            df.loc[index,'DATA'] = ''
            df.loc[index,'HORARIO'] = 'JANTAR'
        else:
            df.loc[index,'HORARIO'] = 'ALMOÇO'

    return df

def formating_data(df:pd.DataFrame, content:list) -> pd.DataFrame: #Obtain the month and format the data colum
    
    mon = content[0][0].split(' ')[7].lower()
    
    for index in df.index:

        if (df.loc[index, 'DATA'] != '' and df.loc[index, 'DATA'] != None):

            data:str = str(df.loc[index, 'DATA'])
            df.loc[index, 'DATA'] = re.sub(r'[^0-9]+', '/' + months[mon], data)

        else:
            df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']
    
    return df

def cap_maker(pdf_file: str) -> pd.DataFrame:

    content = read_pdf(pdf_file)
    
    columns = [
        'DATA', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO', 'GUARNICAO',
        'ARROZ', 'FEIJAO', 'SALADA1', 'SALADA2', 'SUCO', 'SOBREMESA'
    ]

    df = pd.DataFrame(content[2:], columns = columns)
    
    df = formating_df(df, columns)
    df = removing_lines(df)

    df = formating_time_column(df)
    df = formating_data(df, content)

    #putting the columuns in a specifc order to visualizate
    df = df[['DATA', 'HORARIO', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO', 'GUARNICAO',
            'ARROZ', 'FEIJAO', 'SALADA1', 'SALADA2', 'SUCO','SOBREMESA']]
    
    df.to_csv('../csv/cap_menu.csv', index = False)
    #df.to_csv('~/Documents/bot_ru/csv/cap_menu.csv', index = False)
    
    return df