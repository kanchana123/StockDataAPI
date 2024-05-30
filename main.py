from fastapi import FastAPI
import yfinance as yf
import random
from finta import TA
import pandas as pd

# stocks list
stocks_list = ["RELIANCE.NS", "LT.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "HEROMOTOCO.NS", "TATACONSUM.NS",
               "BRITANNIA.NS", "COALINDIA.NS", "INDUSINDBK.NS", "BAJAJ-AUTO.NS", "NTPC.NS", "HINDALCO.NS",
               "MARUTI.NS", "ULTRACEMCO.NS", "ITC.NS", "TCS.NS", "CIPLA.NS", "ONGC.NS", "HDFCLIFE.NS",
               "ADANIENT.NS", "LTIM.NS", "APOLLOHOSP.NS", "BAJFINANCE.NS", "NESTLEIND.NS", "BAJAJFINSV.NS", "SHRIRAMFIN.NS",
               "WIPRO.NS", "TITAN.NS", "TATASTEEL.NS"]

No_Of_Candles = 200

def get_data():
    data = pd.DataFrame({})

    count = 0
    while (data.shape[0] < 300 and count < 50):
        random_stock = random.choice(stocks_list)

        data = yf.download(random_stock, period="1y", start="2023-01-01")

        count += 1

    data[['BB_UPPER', 'BB_MIDDLE', 'BB_LOWER']] = TA.BBANDS(data)

    data = data.dropna()
    ls_cols = ['Open', 'High', 'Low', 'Close', 'BB_UPPER', 'BB_MIDDLE', 'BB_LOWER']
    data = data[ls_cols]

    start_index = random.randint(0, data.shape[0]-No_Of_Candles)


    return data[start_index:start_index+No_Of_Candles]

def format_data(data):
    data_max = data[data.columns].max()
    data_max = data_max.max()

    data_min = data[data.columns].min()
    data_min = data_min.min()

    data['Open'] = data['Open'] - data_min
    data['High'] = data['High'] - data_min
    data['Low'] = data['Low'] - data_min
    data['Close'] = data['Close'] - data_min
    data['BB_UPPER'] = data['BB_UPPER'] - data_min
    data['BB_MIDDLE'] = data['BB_MIDDLE'] - data_min
    data['BB_LOWER'] = data['BB_LOWER'] - data_min

    data['Open'] = -100*data['Open']/data_max
    data['High'] = -100*data['High']/data_max
    data['Low'] = -100*data['Low']/data_max
    data['Close'] = -100*data['Close']/data_max
    data['BB_UPPER'] = -100*data['BB_UPPER']/data_max
    data['BB_MIDDLE'] = -100*data['BB_MIDDLE']/data_max
    data['BB_LOWER'] = -100*data['BB_LOWER']/data_max

    data = data.round(3)

    data['values'] = data[['Open', 'High', 'Low', 'Close', 'BB_UPPER', 'BB_MIDDLE', 'BB_LOWER']].apply(lambda x: f"{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]},{x[6]}", axis=True)
    
    json_data = "\"{values\": "+f"{data['values'].tolist()}"+"}"

    return json_data


app = FastAPI()

@app.get("/")
def read_root():
    data = get_data()
    json_data = format_data(data)
    return {"data": json_data}
