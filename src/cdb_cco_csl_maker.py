import pandas as pd
import pdfplumber,re

months:dict = {'jan': '01',
            'fev': '02', 
            'mar': '03',
            'abr': '04',
            'mai': '05', 
            'jun': '06', 
            'jul': '07', 
            'ago': '08', 
            'set': '09', 
            'out': '10', 
            'nov': '11', 
            'dez': '12'
            }

def cdb_cco_csl_maker(url: str):

    content = read_pdf(url)

    columns:list = ['DATA',
            'DIA',
            'HORARIO',
            'PRATOPRINCIPAL',
            'OVOS',
            'VEGETARIANO',
            'GUARNICAO',
            'SALADA1',
            'SALADA2',
            'ARROZ',
            'FEIJAO',
            'SOBREMESA',
            'SUCO'
            ]
    
    df = pd.DataFrame(content[2:], columns = columns)

    df = formating_df(df, columns)
    df = removing_lines(df)

    df = formating_data(df)
    df = formating_time_column(df)

    df.to_csv('../csv/cdb_cco_csl_menu.csv', index = False)

def read_pdf(url: str)-> list:
    
    content:list = []

    with pdfplumber.open(url) as f:
        for i in f.pages:
            table = i.extract_table()
            if table:
                content.extend(table)
    
    return content

def formating_df(df, columns:list):

    #dopp the column 'DIA'
    df = df.drop('DIA', axis = 1)
    df = df.replace(r'\n', '', regex = True)
    #remove space beetwen numbers
    df['OVOS'] = df['OVOS'].replace(r'\s+','', regex= True)
    df['ARROZ'] = df['ARROZ'].replace(r'\s+','', regex= True)

    return df

def removing_lines(df):#remove empty cells

    for index in df.index:

        if (df.loc[index, 'PRATOPRINCIPAL'] == None or df.loc[index, 'PRATOPRINCIPAL'] == ''):
            df = df.drop(index)
    
    return df

def formating_data(df):#Obtain the month and format the data colum

    for index in df.index:

        if (df.loc[index, 'DATA'] != '' and df.loc[index, 'DATA'] != None):

            data:str = str(df.loc[index, 'DATA'])      

            mon:str = re.findall(r'\w[a-z]+', data.lower())[0]
            day:str = re.findall(r'^\d+', data)[0]
            
            if (int(day) < 10):
                day = '0' + str(day)

            formatted_date:str = day + '/' + months[mon]

            df.loc[index, 'DATA'] = formatted_date
    
    return df

def formating_time_column(df):

    for index in df.index:

        if(df.loc[index,'DATA'] == '' or df.loc[index,'DATA'] == None):
            if (df.loc[index, 'HORARIO'] == 'Almoço'):
                df.loc[index, 'DATA'] = df.loc[index + 1, 'DATA']
            else:
                df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']
    
    return df

cdb_cco_csl_maker('../Menus/Cdb_menu_march.pdf')