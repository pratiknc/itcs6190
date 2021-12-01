import streamlit as st
import pandas as pd
from datetime import datetime
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
    
    st.header("Crypto vs Stock Index Price")
    
    sel1 = st.selectbox('Choose a Crypto Currency',cryptos.keys(),index = 0)
    sel2 = st.selectbox('Choose a Stock Index',indexes.keys(),index = 0)
    
    selected_crypto = cryptos.get(sel1)
    selected_index = indexes.get(sel2)
    
    base = alt.Chart(df_merged).encode(
        alt.X('yearmonthdate(Date_BSE):T', axis=alt.Axis(title="Date")
          )
    )
    
    
    area_1 = base.mark_area(opacity=1, color='#70FF00').encode(
    alt.Y('average(High_'+selected_crypto+')',
          axis=alt.Axis(title='Average Price of '+sel1, titleColor='#70FF00')),
    alt.Y2('average(Low_'+selected_crypto+')')
    ,tooltip = [alt.Tooltip('average(High_'+selected_crypto+')', title=sel1 + ' HIGH'),alt.Tooltip('average(Low_'+selected_crypto+')',title = sel1 + ' LOW')]
    )
    
    area_2 = base.mark_area(opacity=0.8, color='#AD00FF').encode(
    alt.Y('average(High_'+selected_index+')',
          axis=alt.Axis(title='Average Price of '+sel2, titleColor='#AD00FF')),
    alt.Y2('average(Low_'+selected_index+')')
    ,tooltip = [alt.Tooltip('average(High_'+selected_index+')',title = sel2+' HIGH'),alt.Tooltip('average(Low_'+selected_index+')',title = sel2+ ' LOW')]
    )
    
        
    chart = alt.layer(area_1, area_2).resolve_scale(
        y = 'independent'
    ).interactive().properties(
        width = 600
        ,height = 600
    ).configure_axis(
        titleFontSize=16
    )
    
    
    st.altair_chart(chart)

    
if __name__ == '__main__':
    write()

