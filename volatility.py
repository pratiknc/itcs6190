import streamlit as st
import pandas as pd
import datetime
import altair as alt
from altair import datum

def write():
    cryptos = {
    'Bitcoin': 'BTC'
    ,'Ethereum': 'ETH'
    ,'Ripple': 'XRP'
    ,'Doge Coin': 'DOG'
    ,'Binance Coin': 'BNY'
    }
    
    indexes = {
    'BSE Sensex' : 'BSE'
    ,'EuroNext 100' : 'EUR'
    ,'Hang Seng' : 'HDK'
    ,'Shanghai Composite' : 'CNY'
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
    
    df_merged = df_merged[df_merged['Date_BSE'] >= pd.to_datetime('01/01/2019')]
    st.header("Price Volatility")
    inv_start = datetime.date(2019, 1, 1)
    
    inv_start = st.date_input("Start Date of 14-day period", value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1), 
    max_value=datetime.date(2021, 7, 1))
    
    inv_end = st.date_input("End Date of 14-day period", value=inv_start+datetime.timedelta(days=13), min_value=inv_start, max_value=inv_start+datetime.timedelta(days=13))
    
    
    df_filtered = df_merged.copy()
    
    df_filtered = df_filtered[df_filtered['Date_BSE'] >= pd.to_datetime(inv_start)]
    df_filtered = df_filtered[df_filtered['Date_BSE'] <= pd.to_datetime(inv_end)]
    
    
    
    sel1 = st.selectbox('Choose a Crypto Currency',cryptos.keys(),index = 0)
    sel2 = st.selectbox('Choose a Stock Index',indexes.keys(),index = 0)
    
    selected_crypto = cryptos.get(sel1)
    selected_index = indexes.get(sel2)
    
    
    open_close_color_index = alt.condition("datum.Open_"+selected_index+" <= datum.Price_"+selected_index,
                                     alt.value("#06982d"),
                                     alt.value("#ae1325"))
    
    base_index = alt.Chart(df_filtered).encode(
        alt.X('Date_'+selected_index+':T',
              axis=alt.Axis(
                  format='%m/%d',
                  labelAngle=-45,
                  title='14 Day Volatility'
              )
        ),
        color=open_close_color_index
    )
    
    rule_index = base_index.mark_rule().encode(
        alt.Y(
            'Low_'+selected_index+':Q',
            title='Price',
            scale=alt.Scale(zero=False),
        ),
        alt.Y2('High_'+selected_index+':Q')
    )
    
    bar_index = base_index.mark_bar().encode(
        alt.Y('Open_'+selected_index+':Q'),
        alt.Y2('Price_'+selected_index+':Q')
    )
    
    chart_index = alt.layer(rule_index, bar_index).interactive().properties(
        width = 600
        ,height = 600
        ,title = sel2 +' Volatility'
    )
    
    ###
    
    open_close_color_crypto = alt.condition("datum.Open_"+selected_crypto+" <= datum.Close_"+selected_crypto,
                                     alt.value("#06982d"),
                                     alt.value("#ae1325"))
    
    base_crypto = alt.Chart(df_filtered).encode(
        alt.X('Date_'+selected_crypto+':T',
              axis=alt.Axis(
                  format='%m/%d',
                  labelAngle=-45,
                  title='14 Day Volatility'
              )
        ),
        color=open_close_color_crypto
    )
    
    rule_crypto = base_crypto.mark_rule().encode(
        alt.Y(
            'Low_'+selected_crypto+':Q',
            title='Price',
            scale=alt.Scale(zero=False),
        ),
        alt.Y2('High_'+selected_crypto+':Q')
    )
    
    bar_crypto = base_crypto.mark_bar().encode(
        alt.Y('Open_'+selected_crypto+':Q'),
        alt.Y2('Close_'+selected_crypto+':Q')
    )
    
    chart_crypto = alt.layer(rule_crypto, bar_crypto).interactive().properties(
        width = 600
        ,height = 600
        ,title = sel1 +' Volatility'
    )
    
    st.altair_chart(chart_index)
    st.altair_chart(chart_crypto)

if __name__ == '__main__':
    write()