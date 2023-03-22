import streamlit as st
import pandas as pd
import numpy as np
from Tests.api import *
st.title('Data input')
import os
from dotenv import load_dotenv
load_dotenv()
from Tests.apiv2 import Api


try:
    token = st.session_state.token
    username = st.session_state.username
    password = st.session_state.password
except AttributeError:
    st.error('Please login in first')
    token = None
    username = None
    password = None
#create fields for date, speedometer, distance, totalcost, garage, liters purchased

api = Api(username, password)




car = api.get_cars(token)
cars_df = pd.DataFrame(car)
car_choice = st.selectbox('Select a car', cars_df['registration'])
try:
    log = api.get_logs(token, car_choice)
    logs_df = pd.DataFrame(log)
    st.write(logs_df.tail(1))
except Exception as e:
    st.error('No logs for this car')
with st.form('Data input'):
    date = st.date_input('Date')
    speedometer = st.number_input('Speedometer')
    distance = st.number_input('Distance')
    garage = st.text_input('Garage')
    totalcost = st.number_input('Total cost')
    liters = st.number_input('Liters purchased')
    submitted = st.form_submit_button('Submit')


if submitted:
    try:
        api.add_log(token, car_choice, date, speedometer, distance, totalcost, garage, liters)
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


