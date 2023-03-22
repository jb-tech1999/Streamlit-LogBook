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
from Tests.apiv2 import Api

warnings.filterwarnings('ignore')
st.set_page_config(page_title='Petrol Price', page_icon='🚗', layout='wide', initial_sidebar_state='auto')

#set up authentication
st.header('Login')
with st.form('Login'):
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submit = st.form_submit_button('Login')

if submit:
    api = Api(username, password)
    try:
        token = api.get_token()['token']
        #set environment variable
        st.session_state['token'] = token
        st.session_state['username'] = username
        st.session_state['password'] = password

        st.success('Logged in successfully')
    except KeyError:
        st.error('Invalid credentials')
        st.stop()




