import streamlit as st
import pandas as pd
import numpy as np
from Tests.api import *
import requests
from dotenv import load_dotenv
import os
from cache_helper import *

load_dotenv()

username = os.getenv('username')
password = os.getenv('password')
col1, col2 = st.columns([1,4],gap='large')
with open('pages/style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

@st.cache
def logs(car, time):
    logs = get_logs(get_token(username, password), car)
    return logs

@st.cache
def cars(time):
    cars = get_cars(get_token(username, password))
    return cars

car = cars(truncate_time(datetime.datetime.now(),5))
cars_df = pd.DataFrame(car)
car_choice = col2.selectbox('Select a car', cars_df['registration'])
try:
    log = logs(car_choice, truncate_time(datetime.datetime.now(),5))
    logs_df = pd.DataFrame(log)
    logs_df = logs_df[['date', 'odometer', 'distance', 'totalcost', 'garage', 'litersPurchase']]
    logs_df['date'] = logs_df['date'].apply(str_to_date)
    date_range = col2.slider('Select a date range', min_value=logs_df['date'].min(), max_value=logs_df['date'].max(), value=(logs_df['date'].min(), logs_df['date'].max()))
    logs_df_filtered = logs_df[(logs_df['date'] >= date_range[0]) & (logs_df['date'] <= date_range[1])]
    logs_df_filtered['KM/L'] = logs_df['distance'] / logs_df['litersPurchase']
    avg_km_per_liter = round(logs_df_filtered['KM/L'].mean(),2)
    total_cost = round(logs_df_filtered['totalcost'].sum(),2)
    total_liters = round(logs_df_filtered['litersPurchase'].sum(),2)
    total_distance = round(logs_df_filtered['distance'].sum(),2)
    price_per_km = round(total_cost / total_distance,2)
    col1.metric(label='Total Cost', value=f'R{total_cost}')
    col1.metric(label='Total Distance', value=f'{total_distance} km')
    col1.metric(label='Total Liters', value=f'{total_liters} L')
    col1.metric(label='Average Economy', value=f'{avg_km_per_liter} km/L')
    col1.metric(label='Price per km', value=f'R{price_per_km}')
    #set date as index
    logs_df_filtered.set_index('date', inplace=True)
    logs_df_filtered['Average Economy'] = avg_km_per_liter
    col2.line_chart(logs_df_filtered[['KM/L','Average Economy']])
except Exception as e:
    col2.error('No logs for this car')


