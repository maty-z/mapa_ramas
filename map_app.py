import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')
#data = pd.read_csv(r'C:\Users\mzylb\Documents\Geoinfo\Repositorios\mapa_ramas\distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')

st.set_page_config(layout='wide')

ramas_agrupadas = {}
ramas_agrupadas['Transporte'] = ['Transporte terrestre',
                                 'Transporte acuático',
                                 'Transporte aéreo',
                                 'Transporte por tuberías']
ramas_agrupadas['Salud y educacion'] = ['Enseñanza','Servicios de salud humana']
ramas_agrupadas['Alimentacion'] = ['Elaboración de productos alimenticios']
ramas_agrupadas['Energia'] = [ 'Suministro de electricidad',
                               'Suministro de gas']
ramas_agrupadas['Mensajeria'] = ['Almacenamiento y actividades de apoyo al transporte',
                                'Servicio de correo y mensajería']
ramas_agrupadas['Metal'] = ['Fabricación de productos elaborados del metal, excepto maquinaria y equipo',
                            'Fabricación de metales comunes']
ramas_agrupadas['Vehiculos'] = ['Fabricación de vehículos automotores, remolques y semirremolques',
                                'Fabricación de productos de caucho y vidrio']
ramas_agrupadas['Hidrocarburos'] = ['Fabricación de productos de refinación de petróleo',
                                    'Extracción de petróleo crudo y gas natural',
                                    'Actividades de apoyo al petróleo y <la minería']
ramas_agrupadas['Quimica'] = ['Fabricación de sustancias químicas']
ramas_agrupadas['Telecomunicaciones'] = ['Telecomunicaciones']


st.title('Mapa: fuerza obrera en el AMBA')

filtro_sup = st.multiselect('Seleccione grupo de ramas',ramas_agrupadas,['Transporte'])
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
