import streamlit as st
import pandas as pd
import datetime
import altair as alt
from altair import datum

def write():
    columns = {
    'Bitcoin': 'High_BTC'
    ,'Ethereum': 'High_ETH'
    ,'Ripple': 'High_XRP'
    ,'Doge Coin': 'High_DOG'
    ,'Binance Coin': 'High_BNY'
    ,'BSE Sensex' : 'High_BSE'
    ,'EuroNext 100' : 'High_EUR'
    ,'Hang Seng' : 'High_HDK'
    ,'Shanghai Composite' : 'High_CNY'
    }
    
    df_bse = pd.read_csv('./Datasets/BSE_cleaned.csv')
    df_eur = pd.read_csv('./Datasets/Euro_cleaned.csv')
    df_hdk = pd.read_csv('./Datasets/Hang_cleaned.csv')
    df_cny = pd.read_csv('./Datasets/Shangai_cleaned.csv')
    
    df_bse['Date'] = pd.to_datetime(df_bse['Date']).dt.date
    df_eur['Date'] = pd.to_datetime(df_eur['Date']).dt.date
    df_hdk['Date'] = pd.to_datetime(df_hdk['Date']).dt.date
    df_cny['Date'] = pd.to_datetime(df_cny['Date']).dt.date
    
    df_btc = pd.read_csv('./Datasets/bitcoin_rounded.csv')
    df_eth = pd.read_csv('./Datasets/ethereum_rounded.csv')
    df_xrp = pd.read_csv('./Datasets/XRP_rounded.csv')
    df_dog = pd.read_csv('./Datasets/dogecoin_rounded.csv')
    df_bny = pd.read_csv('./Datasets/binance_rounded.csv')
    
    df_btc['Date'] = pd.to_datetime(df_btc['Date']).dt.date
    df_eth['Date'] = pd.to_datetime(df_eth['Date']).dt.date
    df_xrp['Date'] = pd.to_datetime(df_xrp['Date']).dt.date
    df_dog['Date'] = pd.to_datetime(df_dog['Date']).dt.date
    df_bny['Date'] = pd.to_datetime(df_bny['Date']).dt.date
    
    df_btc = df_btc.add_suffix('_BTC')
    df_eth = df_eth.add_suffix('_ETH')
    df_xrp = df_xrp.add_suffix('_XRP')
    df_dog = df_dog.add_suffix('_DOG')
    df_bny = df_bny.add_suffix('_BNY')
    
    df_bse = df_eur.add_suffix('_BSE')
    df_eur = df_eur.add_suffix('_EUR')
    df_hdk = df_hdk.add_suffix('_HDK')
    df_cny = df_cny.add_suffix('_CNY')
    
    df_merged = pd.merge(df_bse, df_eur, left_on='Date_BSE', right_on='Date_EUR').merge(df_hdk, left_on='Date_BSE', right_on='Date_HDK').merge(df_cny,left_on='Date_BSE', right_on='Date_CNY')
    
    df_merged = pd.merge(df_merged,df_btc, left_on='Date_BSE', right_on='Date_BTC').merge(df_eth, left_on='Date_BSE', right_on='Date_ETH')\
    .merge(df_xrp, left_on='Date_BSE', right_on='Date_XRP').merge(df_dog, left_on='Date_BSE', right_on='Date_DOG').merge(df_bny, left_on='Date_BSE', right_on='Date_BNY')
    
    df_merged['Date_BSE'] =  pd.to_datetime(df_merged['Date_BSE'])
    
    st.header("Profit Calculator")
    
    inv_start = datetime.date(2019, 1, 1)
    
    inv_start = st.date_input("Investment Start Date", value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1), max_value=datetime.date(2021, 7, 1))
    inv_end = st.date_input("Investment End Date", value=datetime.date(2021, 7, 1), min_value=inv_start, max_value=datetime.date(2021, 7, 1))
    
    df_investment = df_merged[df_merged['Date_BSE'] >= pd.to_datetime(inv_start)]
    df_investment = df_investment[df_investment['Date_BSE'] <= pd.to_datetime(inv_end)]
    
    sel1 = st.multiselect('Choose a Crypto Currency',(columns.keys()),default=["Bitcoin"])
    
    crypto_cols = [columns.get(key) for key in sel1]
    
    
    inv_val = st.number_input('Investment Amount', min_value=10, max_value=100000000, value=10000, step=1)
    
    df_investment = df_investment.sort_values('Date_BSE')
    units_assigned = df_investment.head(1)
    units_assigned = inv_val /  units_assigned[units_assigned.select_dtypes(exclude=['object', 'datetime','datetime64[ns]']).columns]
    units_assigned = units_assigned[columns.values()]
    
    df_investment['High_BTC'] = df_investment['High_BTC'] * units_assigned.iloc[0]['High_BTC']
    df_investment['High_ETH'] = df_investment['High_ETH'] * units_assigned.iloc[0]['High_ETH']
    df_investment['High_XRP'] = df_investment['High_XRP'] * units_assigned.iloc[0]['High_XRP']
    df_investment['High_DOG'] = df_investment['High_DOG'] * units_assigned.iloc[0]['High_DOG']
    df_investment['High_BNY'] = df_investment['High_BNY'] * units_assigned.iloc[0]['High_BNY']
    df_investment['High_BSE'] = df_investment['High_BSE'] * units_assigned.iloc[0]['High_BSE']
    df_investment['High_EUR'] = df_investment['High_EUR'] * units_assigned.iloc[0]['High_EUR']
    df_investment['High_HDK'] = df_investment['High_HDK'] * units_assigned.iloc[0]['High_HDK']
    df_investment['High_CNY'] = df_investment['High_CNY'] * units_assigned.iloc[0]['High_CNY']
    
    
    df_profit = df_investment.copy()
    df_profit[df_profit.select_dtypes(exclude=['object', 'datetime','datetime64[ns]']).columns] -= int(inv_val)
    
    keep_cols = crypto_cols.copy()
    keep_cols.append("Date_BSE")
    df_investment = df_investment[keep_cols]
    
    multi_lc = alt.Chart(df_investment).transform_fold(
        crypto_cols,
    ).mark_line().encode(
        x='yearmonthdate(Date_BSE):T',
        y=alt.Y('value:Q', title='Profit in USD'),
        color='key:N'
    ).properties(
        title='Profit Estimates',
        width=800,
        height=600
    ).interactive()
    
    
    st.altair_chart(multi_lc)


if __name__ == '__main__':
    write()

