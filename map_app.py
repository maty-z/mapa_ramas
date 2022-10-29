import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')

ramas_agrupadas = {}
ramas_agrupadas['Transporte'] = ['Transporte terrestre y por tuberías',
                                 'Transporte acuático',
                                 'Transporte aéreo',]
ramas_agrupadas['Salud y educacion'] = ['Enseñanza','Servicios de salud humana']
ramas_agrupadas['Alimentacion'] = ['Elaboración de productos alimenticios']
ramas_agrupadas['Energia'] = [ 'Suministro de electricidad, gas, vapor y aire acondicionado',
                                'Captación, tratamiento y distribución de agua']    

st.title('Mapa: fuerza obrera en el AMBA')

filtro_sup = st.multiselect('Seleccione grupo de ramas',ramas_agrupadas,['Transporte'])
filtro = []
for k in filtro_sup:
    filtro = filtro+ramas_agrupadas[k]

data.empleo = data.empleo.apply(lambda x: x.split('.')[1])

fig = px.scatter_mapbox(data[data.clae2_desc.isin(filtro)],lat = 'lat',lon = 'lon',  color='clae2_desc', 
                size = 'empleo_rep', 
                hover_data={'empleo':True,'empleo_rep':False,'lat':False,'lon':False,'clae2_desc':False},
                hover_name='clae2_desc',
                labels={'clae2_desc':'Rama', 'empleo':'Cantidad de trabajadores'},
                )
fig.update_layout(mapbox_style = 'open-street-map', legend ={'orientation':'h'} )

st.plotly_chart (fig,use_container_width=True)
