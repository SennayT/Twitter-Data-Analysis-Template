import streamlit as st
from add_data import fetch_data
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px

st.set_page_config(page_title='Day 5', layout='wide')


def load_data():
    df = fetch_data()
    return df


def select_loc_and_lang():
    df = load_data()
    location = st.multiselect("Choose Location of Tweets",
                              list(df['place'].unique())
                              )
    lang = st.multiselect("choose Language of tweets", list(df['lang'].unique()))
    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)



def wordCloud():
    df = load_data()
    cleanText = ''
    for text in df['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())


st.title("Data Display")



st.title("Data Visualizations")

st.header('Tweets by location and language')

select_loc_and_lang()

wordCloud()
