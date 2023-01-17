import streamlit as st
import pandas as pd
import numpy as np
from Tests.api import *
st.title('Data input')
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv('username')
password = os.getenv('password')
#create fields for date, speedometer, distance, totalcost, garage, liters purchased


car = get_cars(get_token(username, password))
cars_df = pd.DataFrame(car)
car_choice = st.selectbox('Select a car', cars_df['registration'])
try:
    log = get_logs(get_token(username, password), car_choice)
    logs_df = pd.DataFrame(log)
    st.write(logs_df.tail(1))
except Exception as e:
    st.error('No logs for this car')

date = st.date_input('Date')
speedometer = st.number_input('Speedometer')
distance = st.number_input('Distance')
garage = st.text_input('Garage')
totalcost = st.number_input('Total cost')
liters = st.number_input('Liters purchased')

if st.button('Add log'):
    try:
        add_log(get_token(username, password), car_choice, date, speedometer, distance, totalcost, garage, liters)
        st.success('Log added')
        #clear fields
        date = ''
        speedometer = ''
        distance = ''
        totalcost = ''
        garage = ''
        liters = ''
    except Exception as e:
        st.error('Error adding log')
        st.error(e)


