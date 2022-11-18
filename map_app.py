# Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Import processed data
data = pd.read_csv(r'https://raw.githubusercontent.com/maty-z/mapa_ramas/main/distribucion_establecimientos_productivos_descripciones_AMBA_filtro.csv')

# Config page style in wide mode
st.set_page_config(layout='wide')

# Set title page
st.title('Establecimientos productivos en el AMBA')

# Custom data filter. Config "Rama" of interest dictionary
ramas_agrupadas = {}
ramas_agrupadas['Transporte y almacenamiento (logística)'] = ['Transporte terrestre',
                                 'Transporte acuático',
                                 'Transporte aéreo',
                                 'Transporte por tuberías',
                                 'Almacenamiento y actividades de apoyo al transporte',
                                 'Servicio de correo y mensajería']
ramas_agrupadas['Salud y educación privada'] = ['Enseñanza','Servicios de salud humana']
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


# Select from url "Rama" of interest
try: 
    user_input = st.experimental_get_query_params()
    mapa_inicial = user_input['Rama']
except:
    mapa_inicial = ['Transporte y almacenamiento (logística)']

# Make filter from group of "Rama" of interest
filtro_sup = st.multiselect('Seleccione grupo de ramas',ramas_agrupadas,mapa_inicial)
filtro = []
for k in filtro_sup:
    filtro = filtro+ramas_agrupadas[k]

# Minimal data preprocess, for clarity in labels and in marker's size
data.empleo = data.empleo.apply(lambda x: x.split('.')[1][1:])
data['empleo_rep']=data.empleo_rep.map({5:6,25:10,125:15,350:21,500:28})
df = pd.DataFrame({'empleo': {0: '1-9', 1: '10-49', 2: '50-199', 3: '200-499', 4: '500+'},
                   'empleo_rep': {0: 6, 1: 10, 2: 15, 3: 21, 4: 28}})

# Make figure
fig = px.scatter_mapbox(data[data.clae2_desc.isin(filtro)],lat = 'lat',lon = 'lon',  color='clae2_desc', 
                size = 'empleo_rep', 
                hover_data={'empleo':True,'empleo_rep':False,'lat':False,'lon':False,'clae2_desc':False},
                hover_name='clae2_desc',
                labels={'clae2_desc':'Rama', 'empleo':'Cantidad de trabajadores'},
                )

fig.update_layout(mapbox_style = 'open-street-map', legend ={'orientation':'h'} )
fig.update_traces(marker={'sizemode':'diameter','sizeref':1})

# Make annotations for reference of markers' size. The parameters were setted after a trial and error process
y0 = 10
x0 = 15
for ref in df.empleo_rep:
    fig.add_shape(type="circle",
        xref="paper", yref="paper",
        xsizemode='pixel',ysizemode='pixel',
        xanchor = 0, yanchor=0,
        x0=x0-ref/2, y0=y0, x1=ref/2+x0, y1=ref+y0,
        line_width=0,
        fillcolor="black",  opacity=0.5
    )
    y0 += ref+10

fig.add_annotation(xref="paper", yref="paper",x =.03, y =0.01, text='1-9 trabajadores',showarrow=False)
fig.add_annotation(xref="paper", yref="paper",x =.03, y =0.08, text='10-49 trabajadores',showarrow=False)
fig.add_annotation(xref="paper", yref="paper",x =.03, y =0.145, text='50-199 trabajadores',showarrow=False)
fig.add_annotation(xref="paper", yref="paper",x =.03, y =0.24, text='200-499 trabajadores',showarrow=False)
fig.add_annotation(xref="paper", yref="paper",x =.03, y =0.39, text='+500 trabajadores',showarrow=False)

# Make plot in page
st.plotly_chart (fig,use_container_width=True)

# Make histogram
fig = px.histogram(data[data.clae2_desc.isin(filtro)],x='empleo',color='clae2_desc', orientation='v',
        text_auto = True, 
        labels = {'clae2_desc':'Rama', 'empleo':'Trabajadores por establecimiento','%{x}':'Cantidad'},
        category_orders={'empleo':['1-9','10-49','50-199','200-499','500+']},
        barmode = 'group')
fig.update_traces(textposition='outside')
fig.update_layout(xaxis_title='<b>Cantidad de trabajadores por establecimiento</b>', 
                    yaxis_title= '<b>Cantidad de establecimientos</b>',
                    legend ={'orientation':'h', 'y': -0.155})

# Make histogram in page
st.plotly_chart(fig,use_container_width=True)

# Write credits in page
st.write('Datos obtenidos a partir del **Mapa productivo-laboral argentino** elaborado por:  \n * _Ministerio de Economía_  \n * _Ministerio de Trabajo, Empleo, y Seguridad social_')
