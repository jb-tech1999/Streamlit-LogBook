import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit_authenticator as stauth
from Tests.api import *
from dotenv import load_dotenv
import os
load_dotenv()
from cache_helper import *
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title='Petrol Price', page_icon='🚗', layout='wide', initial_sidebar_state='auto')
username = os.getenv('username')
password = os.getenv('password')
col1, col2 = st.columns([1,4],gap='large')




#create login page that will be used to authenticate users



@st.cache
def cars():
    cars = get_cars(get_token(username, password))
    return cars

@st.cache
def logs(car, time):
    logs = get_logs(get_token(username, password), car)
    return logs

def main():
    data = False
    car = cars()
    cars_df = pd.DataFrame(car)
    car_choice = col2.selectbox('Select a car', cars_df['registration'])
    try:
        log = logs(car_choice, truncate_time(datetime.datetime.now(),5))
        logs_df = pd.DataFrame(log)
        logs_df['date'] = logs_df['date'].apply(str_to_date)
        data = True
    except Exception as e:
        st.error('No logs for this car')

    if data:

        date_range = col2.slider('Select a date range', min_value=logs_df['date'].min(), max_value=logs_df['date'].max(), value=(logs_df['date'].min(), logs_df['date'].max()))
        logs_df_filtered = logs_df[(logs_df['date'] >= date_range[0]) & (logs_df['date'] <= date_range[1])]
        #set date as index
        logs_df_filtered.set_index('date', inplace=True)
        logs_df_filtered['Price per Liter'] = logs_df_filtered['totalcost'] / logs_df_filtered['litersPurchase']
        min_price_per_liter = round(logs_df_filtered['Price per Liter'].min(),2)
        max_price_per_liter = round(logs_df_filtered['Price per Liter'].max(),2)
        with st.container():
            
            #get average price per liter
            avg_price_per_liter = logs_df_filtered['Price per Liter'].mean()
            col1.metric(label='Minimum price per liter', value=f'R{min_price_per_liter}', delta=round(avg_price_per_liter-min_price_per_liter,2))
            col1.metric(label='Maximum price per liter', value=f'R{max_price_per_liter}',delta=round(avg_price_per_liter-max_price_per_liter,2))
            col1.metric(label='Average price per liter', value=f'R{round(avg_price_per_liter,2)}')
            #plot price per liter over average price per liter
            logs_df_filtered['Average Price per Liter'] = avg_price_per_liter
            col2.line_chart(logs_df_filtered[['Price per Liter', 'Average Price per Liter']])









if __name__ == '__main__':
    main()