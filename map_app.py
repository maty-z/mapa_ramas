import streamlit as st
import pandas as pd
import plotly.express as px

data0 = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_salud_educacion_grupo0.csv')
data1 = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_salud_educacion_grupo1.csv')
data = pd.concat([data0,data1])[['ID','lat','lon','clae2_desc','empleo','empleo_rep']]

'''data0_ = st.file_uploader('Data0')
if data0_ is not None:
    data0 = pd.read_csv(data0_)

data1_ = st.file_uploader('Data1')
if data1_ is not None:
    data1 = pd.read_csv(data1_)


data = pd.concat([data0,data1])[['ID','lat','lon','clae2_desc','empleo','empleo_rep']]
'''
fig = px.scatter_mapbox(data,lat = 'lat',lon = 'lon',  color='clae2_desc', size='empleo_rep', hover_data=['empleo'])
fig.update_layout(mapbox_style = 'open-street-map')

st.write('mapa')
st.plotly_chart(fig)
