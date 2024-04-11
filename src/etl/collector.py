import requests
import pandas as pd
import datetime

from sqlalchemy import create_engine, text

class Collector:
    def __init__(self, start_date, end_date, coin, dbuser, dbpass, dbname, dblocal, dbtable):
        self.start_date = start_date
        self.end_date = end_date
        self.coin = coin
        self.dataframe = None
        self.collector_checkin = False
        self.transform_checkin = False
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbname = dbname
        self.dblocal = dblocal
        self.dbtable = dbtable
        self.conn_postgres = None

    def collector_data(self):
        try:
            api_url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{self.coin}'&@dataInicial='{self.start_date}'&@dataFinalCotacao='{self.end_date}'&$top=10000&$filter=tipoBoletim%20eq%20'Fechamento'&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
            response = requests.get(api_url)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                if not df.empty:
                    self.dataframe = pd.json_normalize(df['value'])
                    self.collector_checkin = True
            else:
                print('Failed to get data from API.')
                
        except requests.exceptions.RequestException as e:
            print(f'Failed to get data from API. Error: {e}')
        
        finally:
            if 'response' in locals():
                response.close()

    def transform_data(self):
        try:
            datetime_now = datetime.datetime.now()
            self.dataframe['SK_DATA'] = pd.to_datetime(self.dataframe['dataHoraCotacao']).dt.strftime('%Y%m%d')
            
            drop_columns = ['dataHoraCotacao','tipoBoletim']
            self.dataframe = self.dataframe.drop(columns=drop_columns)

            df_buy = pd.DataFrame({'SK_DATA':self.dataframe['SK_DATA'],'INDICADOR':'Euro/Compra',
                            'VALOR_DIA':self.dataframe['cotacaoCompra'],'DTA_CADASTRO':datetime_now})

            df_sell = pd.DataFrame({'SK_DATA':self.dataframe['SK_DATA'],'INDICADOR':'Euro/Venda',
                            'VALOR_DIA':self.dataframe['cotacaoVenda'],'DTA_CADASTRO':datetime_now})

            df_final = pd.concat([df_buy, df_sell], ignore_index=False)
            self.dataframe = df_final.sort_values(by='SK_DATA') 
            self.transform_checkin = True

        except Exception as e:
            print(f'Error when applying transformations: {e}')

    def authenticate_database(self):
        try:   
            engine = create_engine(f'postgresql+psycopg2://{self.dbuser}:{self.dbpass}@{self.dblocal}/{self.dbname}')
            self.conn_postgres = engine.connect()

        except Exception as e:
                    print(f'An error occurred while connecting to the database: {e}')    

    def load_data(self):
        try:  
            conn = self.conn_postgres
            table_name = self.dbtable

            for index, row in self.dataframe.iterrows():
                query = text(f"""
                    INSERT INTO {table_name} (sk_data, indicador, valor_dia, dt_cadastro) VALUES ('{row['SK_DATA']}', '{row['INDICADOR']}', '{row['VALOR_DIA']}', '{row['DTA_CADASTRO']}')
                    ON CONFLICT (sk_data, indicador) DO UPDATE 
                    SET valor_dia = EXCLUDED.valor_dia,
                        dt_cadastro = EXCLUDED.dt_cadastro
                    WHERE {table_name}.valor_dia <> EXCLUDED.valor_dia;
                    """)
                conn.execute(query)
                conn.commit()

        except Exception as e:
            print(f'Error when inserting: {e}')
            conn.rollback()

        finally:
            if self.conn_postgres is not None():
                self.conn_postgres.close()               

def main():
    # Collector class configs
    start_date = '01-01-2024'
    end_date = '04-08-2024'
    coin = 'EUR'
    dbuser = 'teste'
    dbpass = 'teste'
    dbname = 'teste_db'
    dblocal = 'localhost:5437'
    dbtable = 'public.ptax'

    # Collector class
    obj_collector = Collector(start_date, end_date, coin, dbuser, dbpass, dbname, dblocal, dbtable)    
    obj_collector.collector_data()
    obj_collector.authenticate_database()

    #
    if obj_collector.collector_checkin and obj_collector.conn_postgres:
        obj_collector.transform_data()

        if obj_collector.transform_checkin:
            obj_collector.load_data()

if __name__ == "__main__":
    main()