import streamlit as st
from add_data import fetch_data
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from main_page import load_data

def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                                                                                             order='ascending')),
                                                  y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)


def stBarChart():
    df = load_data()
    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['clean_text'].count()}).reset_index()
    dfCount["original_author"] = dfCount["original_author"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "original_author", "Tweet_count")



def langPie():
    df = load_data()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['lang'])['clean_text'].count()}).reset_index()
    dfLangCount["language"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)






st.title("Data Visualizations")
stBarChart()
langPie()
