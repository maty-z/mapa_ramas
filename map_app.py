import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')
#data = pd.read_csv(r'C:\Users\mzylb\Documents\Geoinfo\Repositorios\mapa_ramas\distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')

st.set_page_config(layout='wide')

ramas_agrupadas = {}
ramas_agrupadas['Transporte y almacenamiento (logística)'] = ['Transporte terrestre',
                                 'Transporte acuático',
                                 'Transporte aéreo',
                                 'Transporte por tuberías',
                                 'Almacenamiento y actividades de apoyo al transporte',
                                 'Servicio de correo y mensajería']
ramas_agrupadas['Salud y educació privada'] = ['Enseñanza','Servicios de salud humana']
ramas_agrupadas['Alimentación'] = ['Elaboración de productos alimenticios']
ramas_agrupadas['Energía'] = [ 'Suministro de electricidad',
                               'Suministro de gas']
ramas_agrupadas['Metalurgia'] = ['Fabricación de productos elaborados del metal, excepto maquinaria y equipo',
                            'Fabricación de metales comunes']
ramas_agrupadas['Neumático y automotriz'] = ['Fabricación de vehículos automotores, remolques y semirremolques',
                                'Fabricación de cubiertas y cámaras']
ramas_agrupadas['Petróleo y combustible'] = ['Fabricación de productos de refinación de petróleo',
                                    'Extracción de petróleo crudo y gas natural',
                                    'Actividades de apoyo al petróleo y la minería']
ramas_agrupadas['Química'] = ['Fabricación de sustancias químicas']
ramas_agrupadas['Telecomunicaciones'] = ['Telecomunicaciones']


st.title('Mapa: fuerza obrera en el AMBA')
try: 
    user_input = st.experimental_get_query_params()
    mapa_inicial = user_input['Rama']
except:
    mapa_inicial = ['Transporte y almacenamiento (logística)']

filtro_sup = st.multiselect('Seleccione grupo de ramas',ramas_agrupadas,mapa_inicial)
filtro = []
for k in filtro_sup:
    filtro = filtro+ramas_agrupadas[k]

data.empleo = data.empleo.apply(lambda x: x.split('.')[1][1:])

fig = px.scatter_mapbox(data[data.clae2_desc.isin(filtro)],lat = 'lat',lon = 'lon',  color='clae2_desc', 
                size = 'empleo_rep', 
                hover_data={'empleo':True,'empleo_rep':False,'lat':False,'lon':False,'clae2_desc':False},
                hover_name='clae2_desc',
                labels={'clae2_desc':'Rama', 'empleo':'Cantidad de trabajadores'},
                )
fig.update_layout(mapbox_style = 'open-street-map', legend ={'orientation':'h'} )

st.plotly_chart (fig,use_container_width=True)

with st.expander("Cantidad de establecimientos"):
    fig = px.histogram(data[data.clae2_desc.isin(filtro)],y='empleo',color='clae2_desc', orientation='h',
            text_auto = True, 
            labels = {'clae2_desc':'Rama', 'empleo':'Trabajadores por establecimiento','%{x}':'Cantidad'},
            category_orders={'empleo':['1-9','10-49','50-199','200-499','500+']},
            barmode = 'group')
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_title='<b>Cantidad de trabajadores por establecimiento</b>', 
                      xaxis_title= '<b>Cantidad de establecimientos</b>',
                      legend ={'orientation':'h'})

    #st.write(fig.data)
    st.plotly_chart(fig,use_container_width=True)

#st.write('Fuente de datos: Mapa productivo laboral argentino  \n _Ministerio de Economía_  \n _Ministerio de Trabajo, Empleo, y Seguridad social_')
