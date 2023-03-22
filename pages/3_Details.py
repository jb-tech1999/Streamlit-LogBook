import streamlit as st
import pandas as pd
import numpy as np
from Tests.api import *
import requests
from dotenv import load_dotenv
import os
from cache_helper import *
from Tests.apiv2 import Api

load_dotenv()

try:
    token = st.session_state.token
    username = st.session_state.username
    password = st.session_state.password
except AttributeError:
    st.error('Please login in first')
    token = None
    username = None
    password = None


api = Api(username, password)

col1, col2 = st.columns([1,4],gap='large')
with open('pages/style.css') as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

@st.cache
def logs(car, time):
    logs = api.get_logs(token, car)
    return logs

@st.cache
def car(time, token):
    car = api.get_cars(token)
    return car

if token != None:
    try:
        car = car(truncate_time(datetime.datetime.now(),5), token)
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
            logs_df_filtered['Price/Km'] = logs_df['totalcost'] / logs_df['distance']
            avg_km_per_liter = round(logs_df_filtered['KM/L'].mean(),2)
            total_cost = round(logs_df_filtered['totalcost'].sum(),2)
            total_liters = round(logs_df_filtered['litersPurchase'].sum(),2)
            total_distance = round(logs_df_filtered['distance'].sum(),2)
            price_per_km = round(total_cost / total_distance,2)
            col2.write(logs_df_filtered)

        except Exception as e:
            col2.error('No logs for this car')
    except Exception as e:
        st.error(e)
else:
    col2.error('No token found')