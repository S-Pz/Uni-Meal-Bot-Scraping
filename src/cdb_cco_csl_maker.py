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


def read_pdf(file_path: str)-> list:
    
    content:list = []

    with pdfplumber.open(file_path) as f:
        for i in f.pages:
            table = i.extract_table()
            if table:
                content.extend(table)
    
    return content

def formating_df(df:pd.DataFrame, columns:list) -> pd.DataFrame:

    #dopp the column 'DIA'
    df = df.drop('DIA', axis = 1)
    df = df.replace(r'\n', '', regex = True)
    #remove space beetwen numbers
    df['OVOS'] = df['OVOS'].replace(r'\s+','', regex= True)
    df['ARROZ'] = df['ARROZ'].replace(r'\s+','', regex= True)

    return df

def removing_lines(df:pd.DataFrame) -> pd.DataFrame:#remove empty cells

    for index in df.index:

        if (df.loc[index, 'PRATOPRINCIPAL'] == None or df.loc[index, 'PRATOPRINCIPAL'] == '' or df.loc[index, 'ARROZ'] == None):
            df = df.drop(index)
    
    return df

def format_dates(df:pd.DataFrame) -> pd.DataFrame:#Obtain the month and format the data colum

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

def fill_missing_date(df:pd.DataFrame) -> pd.DataFrame:

    for index in df.index:

        if(df.loc[index,'DATA'] == '' or df.loc[index,'DATA'] == None):
            if (df.loc[index, 'HORARIO'] == 'Almoço'):
                df.loc[index, 'DATA'] = df.loc[index + 1, 'DATA']
            else:
                df.loc[index, 'DATA'] = df.loc[index - 1, 'DATA']
    
    return df

def adding_schedule(df:pd.DataFrame) -> pd.DataFrame:
    
    for index in df.index:
        if(index%2 == 0):
            df.loc[index,'HORARIO'] = 'Almoço'
        else:
            df.loc[index,'HORARIO'] = 'Jantar'
        
    return df

def cdb_cco_csl_maker(pdf_file: str) -> pd.DataFrame:

    content:list = read_pdf(pdf_file)
    if(len(content[1]) == 13):

        columns:list = [
                'DATA', 'DIA', 'HORARIO', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO',
                'GUARNICAO', 'SALADA1', 'SALADA2', 'ARROZ', 'FEIJAO', 'SOBREMESA',
                'SUCO']
    
        df = pd.DataFrame(content[2:], columns = columns)

        df = formating_df(df, columns)
        df = removing_lines(df)

        df = format_dates(df)
        df = fill_missing_date(df)

        df = df[['DATA','HORARIO','PRATOPRINCIPAL',
                 'OVOS','VEGETARIANO','GUARNICAO','SALADA1',
                 'SALADA2','ARROZ','FEIJAO','SOBREMESA','SUCO']]
    
    elif(len(content[1])== 12):
        
        columns = [
            'DATA', 'DIA', 'PRATOPRINCIPAL', 'OVOS', 'VEGETARIANO', 'GUARNICAO',
            'SALADA1', 'SALADA2','ARROZ', 'FEIJAO', 'SUCO','SOBREMESA'
        ]

        df = pd.DataFrame(content[2:], columns = columns)
        print(df)
        df = formating_df(df, columns)
        df = removing_lines(df) #remove empty cells
        
        df = format_dates(df) #format the date column
        
        df = adding_schedule(df) #add the schedule column
        df = fill_missing_date(df) #fill the missing date

        df = df[['DATA','HORARIO','PRATOPRINCIPAL',
                 'OVOS','VEGETARIANO','GUARNICAO','SALADA1',
                 'SALADA2','ARROZ','FEIJAO','SOBREMESA','SUCO']]
    
    namefile = pdf_file.split("/")
    name_file_csv = namefile[2].split(".")

    df.to_csv(f'../csv/{name_file_csv[0]}_menu.csv', index = False)
    #df.to_csv(f'~/Documents/bot_ru/csv/{name_file_csv[0]}_menu.csv', index = False)

    return df
cdb_cco_csl_maker("../Menus/csl.pdf")