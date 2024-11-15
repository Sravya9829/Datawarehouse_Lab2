from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
import requests
import snowflake.connector
import logging


def get_snowflake_conn():
    conn = BaseHook.get_connection('my_snowflake_conn')
    return snowflake.connector.connect(
        user=conn.login,
        password=conn.password,
        account=conn.extra_dejson['account'],
        warehouse=conn.extra_dejson.get('warehouse', 'COMPUTE_WH'),
        database=conn.extra_dejson.get('database', 'DEV'),
        schema='RAW_DATA'
    )

def transform(data, symbol):
    transformed_data = []
    for stock_info_date, stock_info in data.get('Time Series (Daily)', {}).items():
        transformed_data.append({
            'date': datetime.strptime(stock_info_date, "%Y-%m-%d").strftime('%Y-%m-%d'),
            'open': float(stock_info.get('1. open', 0)),
            'high': float(stock_info.get('2. high', 0)),
            'low': float(stock_info.get('3. low', 0)),
            'close': float(stock_info.get('4. close', 0)),
            'volume': int(stock_info.get('5. volume', 0)),
            'symbol': symbol
        })
    return transformed_data

def incremental_load(snowflake_connection, transformed_data, target_table):
    try:
        snowflake_connection.cursor().execute("Begin")
        for each_record in transformed_data:
            merge_query = f"""
            MERGE INTO {target_table} AS t
            USING (SELECT 
                    '{each_record['date']}' AS date,
                    {each_record['open']} AS open,
                    {each_record['high']} AS high,
                    {each_record['low']} AS low,
                    {each_record['close']} AS close,
                    {each_record['volume']} AS volume,
                    '{each_record['symbol']}' AS symbol) AS s
            ON t.date = s.date AND t.symbol = s.symbol
            WHEN MATCHED THEN
                UPDATE SET
                    t.open = s.open,
                    t.high = s.high,
                    t.low = s.low,
                    t.close = s.close,
                    t.volume = s.volume
            WHEN NOT MATCHED THEN
                INSERT (date, open, high, low, close, volume, symbol)
                VALUES (s.date, s.open, s.high, s.low, s.close, s.volume, s.symbol);
            """
            snowflake_connection.cursor().execute(merge_query)
        snowflake_connection.cursor().execute("Commit")
    except Exception as e:
        snowflake_connection.cursor().execute("Rollback")
        logging.error(f"Error during incremental load: {str(e)}")
        raise

@dag(default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'start_date': datetime(2024, 10, 10),
    }, schedule_interval='@daily', catchup=False, tags=['stock-data-loading'])
def data_loading_dag():
    @task
    def fetch_data(symbol: str) -> dict:
        api_key = Variable.get("api_key")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f"Failed to fetch data for {symbol}: {response.text}")
            return {}
        return response.json()

    @task
    def process_and_load_data(data: dict, symbol: str):
        if not data:
            logging.info(f"No data fetched for {symbol}")
            return
        transformed_data = transform(data, symbol)
        conn = get_snowflake_conn()
        try:
            incremental_load(conn, transformed_data, 'NPS')
        finally:
            conn.close()

    symbols = ['AAPL', 'WMT']
    for symbol in symbols:
        data = fetch_data(symbol)
        process_and_load_data(data, symbol)

load_data_dag = data_loading_dag()