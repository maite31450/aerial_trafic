import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

with st.sidebar:
    st.image('jumbo-jet-flying.jpg')

st.title("Quels sont les aéroports européens les plus importants")

trafic_passengers = pd.read_csv(r'C:\Users\MAITE\Wild Code School\hack\trafic_passengers.csv')

#create second temporari df to highlight 10 best european airport according yearly sum of passagers carried
trafic_by_airport = trafic_passengers.groupby(['YEAR', 'airport', 'country_name']).agg(NB_PAS_carried = ('OBS_VALUE','sum'))
trafic_by_airport = trafic_by_airport.reset_index()

st.subheader('Classement des 10 aéroports européens générant le plus de trafic')

years = st.selectbox("Sélectionner l'année de départ que vous souhaitez analyser", trafic_by_airport['YEAR'].unique())
if years:
    apt_trafic_yearly = trafic_by_airport.loc[trafic_by_airport['YEAR'] == years, :].sort_values('NB_PAS_carried', ascending=False).iloc[:10]
    st.dataframe(apt_trafic_yearly)
else:
    st.dataframe(trafic_by_airport)

st.subheader("visualisation des aéroports selon le pays")

#second plot
fig2 = plt.figure(figsize=(15,12))
ax = sns.barplot(data=trafic_by_airport.loc[trafic_by_airport['YEAR'] == years, :].sort_values('NB_PAS_carried', ascending=False).head(10), x='airport', y='NB_PAS_carried', hue='country_name', dodge=False)
plt.title("TOP 10 des plus gros aéroports en Europe", fontsize = 20)
plt.xlabel('AEROPORTS', fontsize=13)
plt.ylabel('NB PASSAGERS TRANSPORTES', fontsize=13)
#plt.ylim(0, 170000000)
plt.ticklabel_format(axis='y', style='plain')
plt.xticks(rotation='vertical')
plt.margins(0.2);

st.pyplot(fig2.figure)