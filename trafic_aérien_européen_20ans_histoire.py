import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title="Etude sur l'évolution du trafic aérien européen",
    page_icon="🛫",
    layout = "wide"
)

with st.sidebar:
    st.image('jumbo-jet-flying.jpg')

st.title("Etude sur l'évolution du trafic aérien européen")

#st.markdown("<h1 style='text-align: center; color: teal;'>Etude sur l'évolution du trafic aérien européen</h1>", unsafe_allow_html=True)

trafic_passengers = pd.read_csv(r'C:\Users\MAITE\Wild Code School\hack\trafic_passengers.csv')


#creer temporari df group by years to follow evolution of global trafic year after year
yearly_evo_full = trafic_passengers.groupby('YEAR').agg(NB_PAS_carried = ('OBS_VALUE','sum'))
yearly_evo_full = yearly_evo_full.reset_index()

#suppress scientific notation
pd.options.display.float_format = '{:.0f}'.format

#create first plot
fig = px.line(yearly_evo_full, x='YEAR', y='NB_PAS_carried', 
        #title="Evolution temporelle du nombre de passagers transportés à l'échelle européenne",
        labels={'YEAR':'ANNEES', 'NB_PAS_carried':'NBRE PASSAGERS TRANSPORTES'},
        log_x = True ,  range_x = [1998 , 2023],  range_y = [2500000 , 2500000000]) ;
fig.update_layout(
    title=dict(text="Evolution temporelle du nombre de passagers transportés à l'échelle européenne", font=dict(size=18)),
    title_font_color="lightseagreen"
)
fig.update_traces(line_color='lightseagreen', line_width=5)
st.plotly_chart(fig, use_container_width=True)


st.header("les faits expliquant les diverses baisses du trafic")

st.subheader('2001')
st.image('11sep01.jpg', caption='attentat du 11 septembre à New York')
st.write("Des avions de ligne s'écrasent sur le Pentagone et le World Trade Center. Face à la catastrophe les U.S.A décident de clouer tous les avions aux sols pendant 4 jours. En France, dès le soir des attentats, le gouvernement met en place le plan « Vigipirate renforcé » sur l’ensemble du territoire. Des mesures antiterroristes sont prises partout dans le monde. Entre le 11 septembre et le 4 novembre 2001, les voyages ont diminué de  26 % sur l’Atlantique du Nord et de 10 % en Europe.")

st.subheader('2009')
st.image('RIO-PAR.jpg', caption="recherches en mer des dépris du vol AF447")
st.write("Le vol AIR FRANCE AF447 Rio de Janeiro / Paris disparait en mer. En Afrique, l'OMS déclare la pandémie du H1N1.")

st.subheader('2010')
st.image('islande.jpg', caption="volcan EYJAFJALLAJÖKULL crachant un épais nuage de cendres")
st.write("Du 14 avril au 24 mai : l'éruption du volcan islandais EYJAFJALLAJÖKULL provoque un nuage de cendres qui paralyse le trafic aérien en Europe. Quelque 100'000 vols annulés en une semaine, soit une perte de chiffre d'affaires de 1,8 milliard de dollars pour le secteur.")

st.subheader('2014')
st.image('ebola.jpg', caption="Une femme se fait prendre la température dans le cadre de la prévention d'Ebola, à Freetown, en Sierra Leone")
st.write("Le virus Ebola décime l'Afrique.")
st.write("Le 8 mars le vol Malaysia Airlines MH370 se volatilise.")

st.subheader('2020')
st.image('covid.jpg', caption="")
st.write("Le COVID-19 confine le monde.")
st.write("En 2020, la crise sanitaire mondiale porte un coup d'arrêt au trafic aérien pourtant bien orienté en 2019, avec un record de plus de deux millions de passagers. Mouvements d'avions commerciaux, fret commercial, trafic de La Poste et trafic de passagers, tous sont en baisse.")