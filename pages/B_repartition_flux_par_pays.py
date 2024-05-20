import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from shapely.geometry import shape, Point
from streamlit_folium import folium_static
import json
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#Partis a remplacer avec votre propre chemin de avion_clean
chemin_csv = 'avion_clean.csv'
chemin_geojson = 'europe.geojson'

############################################ Class Pays ###################################################

class Pays:

    #Variables global propre à la classe
    instances = {}
    nbr_pays = 0

    #Init de la class
    def __init__(self, iso, nom_vf):
        '''
        Cette fonction sert à initialiser les fonctions qui seront plus tard appelé dans le code
        '''

        self.iso = iso
        self.nom_vf = nom_vf
        
        #Récupération des coordonnée et le centre du pays grace au fichier europe.geojson
        for pays in data["features"]:
            if pays["properties"]["ISO2"] == self.iso:
                 self.nom = pays["properties"]["NAME"]
                 self.coordonee = shape(pays['geometry'])
                 self.lon = pays["properties"]["LON"]
                 self.lat = pays["properties"]["LAT"]
                 break
        
        #Récuperation des voyageurs (df_voyageur_depart non utilisé finalement dans le code)
        self.df_voyageur_arrive = df_avion[['geo','nom_anglais','2023 ']][(df_avion['partner'] == iso + " ") & 
                                                            (df_avion['tra_meas'] ==   'PAS_BRD_ARR ')].dropna()
        self.df_voyageur_depart = df_avion[['geo','nom_anglais','2023 ']][(df_avion['partner'] == iso + " ") & 
                                                            (df_avion['tra_meas'] ==   'PAS_BRD_DEP ')].dropna()
        
        self.pourcentage = self.df_voyageur_arrive['2023 '].sum() / total_voya

        #Sert a avoir un dictionnaire avec comme clé le nom du pays et en valeur l'instance du pays (object qui contient mes variables)
        Pays.instances[self.nom_vf] = self
        Pays.nbr_pays += 1

#################################################################################################################

#Ouverture de la base de donnée des voyageurs
df_avion = pd.read_csv('avion_clean.csv')
df_avion = df_avion.replace(': ', value= None) #Ligne plus utile, je crois

#Définition de variables utilisé dans les graphiques
total_voya = round(df_avion['2023 '][(df_avion['tra_meas'] ==   'PAS_BRD_ARR ')].sum(),2)
total_voyageur = str(round(df_avion['2023 '][(df_avion['tra_meas'] ==   'PAS_BRD_ARR ')].sum() /1000000,2)) + "M"

#Ouverture du fichier europe.geojson
with open(chemin_geojson, 'r') as f:
    data = json.load(f)


#Définiton des instances
france = Pays('FR', 'France')
italie = Pays('IT', 'Italie')
belgique = Pays('BE', 'Belgium')
espagne = Pays('ES', 'Espagne')
allemagne = Pays('DE', 'Germany')
portugal = Pays('PT', 'Portugal')

suisse = Pays('CH', 'Suisse')
suede = Pays('SE', 'Suède')
pologne = Pays('PL', 'Pologne')
malte = Pays('MT', 'Malte')
danemark = Pays('DK', 'Danemark')
roumanie = Pays('RO', "Roumanie")
croatie = Pays("HR","Croatie")
grece = Pays("GR","Greece")

############################################ Définition fonction ###################################################


def quel_pays(point):
    '''
    Fonction qui prend en entrée un point (un objet geometry) qui contient longitude et latitude.
    Test si ce point est dans un des pays instancié plus haut
    '''
    #Test pour chaque pays: pays = instance
    for pays in Pays.instances.values():
        #Regarde si point est dans coordonnee, si oui retourne le nom du pays
        if pays.coordonee.contains(point):
            return pays.nom_vf
    
    #Si non trouvé renvoit False
    return False

def get_pos(lat: float, lng: float):
    '''
    Fonction pour convertir longitude et latitude en tuple, utile pour travailler avec des objet de type geometry
    '''
    return lat, lng

#Définition des variables utilisé dans le cache du site.
if 'clic_pays' not in st.session_state:
    st.session_state.clic_pays = False

if 'trigger' not in st.session_state:
    st.session_state.trigger = False

###################################################################################################################

############################################ Début du site ########################################################

#Configuration wide -> Affichage plus large
st.set_page_config(layout="wide")
st.title('Visualisation des transit aérien intra-européen')

#Sert à avoir un peu d'expace a gauche et droite, tout en ayant deux case carte et center2 ou se trouvera les infos
left, carte, graphique_droite, right = st.columns([1, 18, 18, 1])

#Parti sur la Carte
with carte:
    st.write('<span style="font-size:35px;">Carte de l\'europe</span>', unsafe_allow_html=True)


############################################ Création du map ###################################################

    pays_clic = False
    clic = [0,0]

    #Création de l'objet map (carte vierge)
    m = fl.Map(
            tiles='cartodbpositron',
            max_zoom=21,
        )

    #Définition des objet dynamiques, ils sont vide pour le moment
    pays_selection = fl.FeatureGroup(name = "pays")
    france_fe = fl.FeatureGroup(name = "france") 
    autre = fl.FeatureGroup(name = "autre") 

    #Si le pays cliqué est reconnu comme un pays présent dans la Class Pays
    if st.session_state.clic_pays != False:

        pays_choisis = Pays.instances[st.session_state.clic_pays]
        ici = (pays_choisis.lat, pays_choisis.lon)

        #Ligne pour afficher la frontière du pays
        pays_selection.add_child(fl.features.GeoJson(pays_choisis.coordonee))

        #Partis pour l'affichage des cercles
        #Regarder toutes les instance de Pays
        for pays in Pays.instances.values():
            #Condition pour ne pas prendre le pays sur lequel on a cliqué
            if not pays.iso == pays_choisis.iso:
                ici = (pays.lat, pays.lon)
                voyage_arrive = pays_choisis.df_voyageur_arrive['2023 '][pays_choisis.df_voyageur_arrive['geo'] == pays.iso]

                #Si on a un chiffre sur le nombre de voyageur
                if not voyage_arrive.empty:
                    #Récupere le nombre de voyageur, divise par 50 pour ne pas avoir des cercle trop grand, totalement arbitraire
                    nombre = int(voyage_arrive.iloc[0] /50)
                    #Actualise l'objet autre.
                    autre.add_child(fl.Circle(ici, 
                                              radius = nombre,
                                              tooltip= f"Personne allant en {pays_choisis.nom_vf} : {voyage_arrive.iloc[0]}"))

    #Ajoute sur la carte vuerge (m) les paramètres souhaité, taille, zoom, center pour savoir ce que la carte affichera par défaut
    carte = st_folium(
            m,
            width=1000,
            height=600,
            zoom= 4,
            center= [50, 20],
            feature_group_to_add = [pays_selection, autre], #Partis dynamique de la carte, objet qui se charge a chaque rafraichissement de la page streamlit
        )

#################################################################################################################

########################################### Detection clic ######################################################

    clic = None
    #Si l'utilisateur clique sur la carte
    if carte.get("last_clicked"):
        #récuperation des coorodnnées
        clic = get_pos(carte["last_clicked"]["lng"], carte["last_clicked"]["lat"])
        #Mise dans un objet geometry pour pouvoir faire la comparaison plus haut
        point = Point(clic)

    #Si l'utilisateur clique sur la carte
    if clic is not None and st.session_state.trigger != point:
        #Met a jour les variables dans le cache pour conserver les informations entre deux rafraichissement
        pays_clic = quel_pays(point)
        st.session_state.clic_pays = pays_clic
        st.session_state.trigger = point
        st.experimental_rerun() #Sert a rafraichir manuellement la page internet

#################################################################################################################

############################################ Partie Graphique ###################################################
    
    with graphique_droite:
        #Si clic_pays ne vaut pas False -> Si l'utilisateur a cliqué sur un pays EU
        if st.session_state.clic_pays != False:
            
            #Récuperation des variables clé pour le graphique
            instance_pays = Pays.instances[st.session_state.clic_pays]
            df = instance_pays.df_voyageur_arrive
            df_avion['somme'] = total_voyageur
            df_petit = df.sort_values(by = '2023 ', ascending=True)
            df_petit = df_petit.tail(10)
            
            total = str(round(int(df['2023 '].sum()) / 1000000,2)) + "M"
            pourcentage = round(float(total[:-2]) / float(total_voyageur[:-2])*100,2)

            #Affichage sur le site
            st.write('<br><br><span style="font-size:35px;">Représentation du % des parts du traffic aérien</span>', unsafe_allow_html=True)
            progress_bar = st.progress(round(pourcentage)) #Barre progression

            st.write(f'<span style="font-size:25px;">{pourcentage} %</span>', unsafe_allow_html=True)
            st.write(f'<span style="font-size:35px;">Top 10 des pays venant en {pays_choisis.nom_vf}</span>', unsafe_allow_html=True)

            #Définition du fraphique top 10
            fig = px.bar(df_petit, x= '2023 ', y='nom_anglais', orientation='h')
            fig.update_yaxes(title_text='')

            #Affichage du graphique
            st.plotly_chart(fig)


left2, bas, right2 = st.columns([1, 18, 1])
with bas:
    #Si clic_pays ne vaut pas False -> Si l'utilisateur a cliqué sur un pays EU
    if st.session_state.clic_pays != False:

        #Comme un st.write mais j'ai retiré la marge et le padding pour un affichage plus esthétique
        st.markdown(
        """
        <div style="margin: 00px; padding: 0px; border: 0px solid black">
            <span style="font-size:35px;">Répartition traffic par pays</span>
        </div>
        """,
        unsafe_allow_html=True)

        #Variable pour le for
        l_pourcentage_pays = []
        somme_pourcentage_pays = 0
        nom_pays = []
        #Regarde tout les pays présente dans Class Pays
        for pays in Pays.instances.values():

            l_pourcentage_pays.append(pays.pourcentage)
            somme_pourcentage_pays += l_pourcentage_pays[-1]
            nom_pays.append(pays.nom_vf)

        #Création du df pour le graphique proportion (tout en bas)
        df_pourcentage = {'nom' : nom_pays,
                          'pourcentage' : l_pourcentage_pays,
                          'total' : somme_pourcentage_pays }

        #Définition du graphique     
        fig = px.bar(df_pourcentage, x = 'pourcentage', y = 'total', color="nom", orientation='h')
        fig.update_layout(xaxis_visible=False, yaxis_visible=False, #Cacher les axes
                          bargap=0.0, width=1800, height=200, #Réglage taille graphique et taille bar
                          legend_orientation='h', legend=dict(font=dict(size=20), yanchor='bottom', y=-1, xanchor='left', x=0.0)) #paramètre pour la légende
        
        #Affichage du graphique
        st.plotly_chart(fig)


###################################################################################################################

