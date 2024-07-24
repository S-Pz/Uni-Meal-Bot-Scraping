import sqlite3, pandas as pd

TABLES = {

    'CTAN':(

        """CREATE TABLE IF NOT EXISTS CTAN(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            data TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            arroz TEXT,
            feijao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            suco TEXT,
            sobremesa TEXT
        )"""
    ),
    'CSA':(

        """CREATE TABLE IF NOT EXISTS CSA(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            data TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            arroz TEXT,
            feijao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            suco TEXT,
            sobremesa TEXT
        )"""
    ),
    'CDB':(

        """CREATE TABLE IF NOT EXISTS CDB(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            data TEXT,
            horario TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            arroz TEXT,
            feijao TEXT,
            sobremesa TEXT,
            suco TEXT
        )"""
    ),
    'CCO':(

        """CREATE TABLE IF NOT EXISTS CCO(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            data TEXT,
            horario TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            arroz TEXT,
            feijao TEXT,
            sobremesa TEXT,
            suco TEXT
        )"""
    ),
    'CSL':(

        """CREATE TABLE IF NOT EXISTS CSL(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            data TEXT,
            horario TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            arroz TEXT,
            feijao TEXT,
            sobremesa TEXT,
            suco TEXT
        )"""
    ),
    'CAP':(

        """CREATE TABLE IF NOT EXISTS CAP(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT,
            pratoprincipal TEXT,
            ovos TEXT,
            vegetariano TEXT,
            guarnicao TEXT,
            arroz TEXT,
            feijao TEXT,
            salada1 TEXT,
            salada2 TEXT,
            suco TEXT,
            sobremesa TEXT
        )"""
    ),
}

def create_database():

    try:
        conn = sqlite3.connect('cardapio.db')
        return conn
    except(sqlite3.OperationalError) as error:
        print(error)

def create_table(conn: sqlite3.Connection):

    c = conn.cursor()

    for i in TABLES:
        try:
            c.execute(TABLES[i])
        except(sqlite3.OperationalError) as error:
            print(f"Error to create table {i}", error)
    
    c.close()

def drop_tables(conn: sqlite3.Connection):

    c = conn.cursor()

    for i in TABLES.keys():
        try:
            c.execute(f"DROP TABLE IF EXISTS {i}")
        except(sqlite3.OperationalError) as error:
            print(f"Error to drop table {i}", error)
    
    c.close()

def insert_data_CTAN(conn: sqlite3.Connection, dF:pd.DataFrame):

    c = conn.cursor()

    try:
        insert = """INSERT INTO CTAN(
            data,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            arroz,
            feijao,
            salada1,
            salada2,
            suco,
            sobremesa
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = dF.loc[index,'DATA']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            SUCO = dF.loc[index, 'SUCO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']

            data:tuple = (DATA, PRATOPRINCIPAL, OVOS,
                        VEGETARIANO, GUARNICAO, ARROZ,
                        FEIJAO, SALADA1, SALADA2,
                        SUCO, SOBREMESA)     
            
            c.execute(insert, data)
            conn.commit()

    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CTAN table", error)
    
    finally:
        c.close()

def insert_data_CSA(conn: sqlite3.Connection, dF:pd.DataFrame):
    
    c = conn.cursor()

    try:
        insert = """INSERT INTO CSA(
            data,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            arroz,
            feijao,
            salada1,
            salada2,
            suco,
            sobremesa
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = dF.loc[index,'DATA']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            SUCO = dF.loc[index, 'SUCO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']

            data:tuple = (DATA, PRATOPRINCIPAL, OVOS,
                        VEGETARIANO, GUARNICAO, ARROZ,
                        FEIJAO, SALADA1, SALADA2,
                        SUCO, SOBREMESA)    
            
            c.execute(insert, data)
            conn.commit()
    
    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CSA table", error)
    
    finally:
        c.close()

def insert_data_CSL(conn: sqlite3.Connection, dF:pd.DataFrame):

    c = conn.cursor()

    try:
        insert = """INSERT INTO CSL(
            data,
            horario,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            salada1,
            salada2,
            arroz,
            feijao,
            sobremesa,
            suco
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = dF.loc[index, 'DATA']
            HORARIO = dF.loc[index, 'HORARIO']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']
            SUCO = dF.loc[index, 'SUCO']

            data:tuple = (DATA, HORARIO, PRATOPRINCIPAL,
                        OVOS, VEGETARIANO, GUARNICAO,
                        SALADA1, SALADA2, ARROZ,
                        FEIJAO, SOBREMESA, SUCO)
            
            c.execute(insert,data)
            conn.commit()
    
    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CSL table", error)

    finally:
        c.close()

def insert_data_CDB(conn: sqlite3.Connection, dF:pd.DataFrame):

    c = conn.cursor()

    try:
        insert = """INSERT INTO CDB(
            data,
            horario,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            salada1,
            salada2,
            arroz,
            feijao,
            sobremesa,
            suco
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = dF.loc[index, 'DATA']
            HORARIO = dF.loc[index, 'HORARIO']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']
            SUCO = dF.loc[index, 'SUCO']

            data:tuple = (DATA, HORARIO, PRATOPRINCIPAL,
                        OVOS, VEGETARIANO, GUARNICAO,
                        SALADA1, SALADA2, ARROZ,
                        FEIJAO, SOBREMESA, SUCO)
            
            c.execute(insert,data)
            conn.commit()
    
    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CDB table", error)

    finally:
        c.close()

def insert_data_CCO(conn: sqlite3.Connection, dF:pd.DataFrame):

    c = conn.cursor()

    try:
        insert = """INSERT INTO CDB(
            data,
            horario,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            salada1,
            salada2,
            arroz,
            feijao,
            sobremesa,
            suco
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = dF.loc[index, 'DATA']
            HORARIO = dF.loc[index, 'HORARIO']
            PRATOPRINCIPAL = dF.loc[index, 'PRATOPRINCIPAL']
            OVOS = dF.loc[index, 'OVOS']
            VEGETARIANO = dF.loc[index, 'VEGETARIANO']
            GUARNICAO = dF.loc[index, 'GUARNICAO']
            SALADA1 = dF.loc[index, 'SALADA1']
            SALADA2 = dF.loc[index, 'SALADA2']
            ARROZ = dF.loc[index, 'ARROZ']
            FEIJAO = dF.loc[index, 'FEIJAO']
            SOBREMESA = dF.loc[index, 'SOBREMESA']
            SUCO = dF.loc[index, 'SUCO']

            data:tuple = (DATA, HORARIO, PRATOPRINCIPAL,
                        OVOS, VEGETARIANO, GUARNICAO,
                        SALADA1, SALADA2, ARROZ,
                        FEIJAO, SOBREMESA, SUCO)
            
            c.execute(insert,data)
            conn.commit()
    
    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CCO table", error)

    finally:
        c.close()

def insert_data_CAP(conn:sqlite3.Connection, dF:pd.DataFrame):

    c = conn.cursor()

    try:
        insert = """INSERT INTO CAP(
            data,
            pratoprincipal,
            ovos,
            vegetariano,
            guarnicao,
            arroz,
            feijao,
            salada1,
            salada2,
            suco,
            sobremesa
        )VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        for index in dF.index:

            DATA = str(dF.loc[index, 'DATA'])
            PRATOPRINCIPAL = str(dF.loc[index, 'PRATOPRINCIPAL'])
            OVOS = str(dF.loc[index, 'OVOS'])
            VEGETARIANO = str(dF.loc[index, 'VEGETARIANO'])
            GUARNICAO = str(dF.loc[index, 'GUARNICAO'])
            ARROZ = str(dF.loc[index, 'ARROZ'])
            FEIJAO = str(dF.loc[index, 'FEIJAO'])
            SALADA1 = str(dF.loc[index, 'SALADA1'])
            SALADA2 = str(dF.loc[index, 'SALADA2'])
            SUCO = str(dF.loc[index, 'SUCO'])
            SOBREMESA = str(dF.loc[index, 'SOBREMESA'])       

            data:tuple = (DATA, PRATOPRINCIPAL, OVOS,
                       VEGETARIANO, GUARNICAO, ARROZ,
                       FEIJAO, SALADA1, SALADA2,
                       SUCO, SOBREMESA)
            
            c.execute(insert,data)
            conn.commit()

    except(sqlite3.OperationalError) as error:
        print("Error to insert data in CAP table", error)
    
    finally:
        c.close()