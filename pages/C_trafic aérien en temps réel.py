import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

with st.sidebar:
    st.image('jumbo-jet-flying.jpg')

st.title("Cartographie des vols à travers le monde")


st.write("OpenFlights est un outil qui vous permet de cartographier vos vols à travers le monde, de les rechercher et de les filtrer de toutes sortes de manières intéressantes, de calculer automatiquement des statistiques et de partager vos vols et voyages avec vos amis et dans le monde entier (si vous le souhaitez). Vous pouvez également consulter les cartes routières de presque tous les aéroports du monde et découvrir quelles compagnies aériennes volent et où.")

st.write("C'est aussi le nom du projet open source pour construire cet outil. Pour voir plus d'informations sur l'utilisation de cet outil, consulter la Foire aux Questions : https://openflights.org/faq")

components.iframe('https://openflights.org/', width=1000, height=1300)