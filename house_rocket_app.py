import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import geopandas
from datetime import datetime

pd.set_option('display.float_format', lambda x: '%.5f' % x)
st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile


# get geofile
url = 'https://gisdata.seattle.gov/server/rest/services/COS/Seattle_City_Limits/MapServer/2/query?outFields=*&where=1%3D1&f=geojson'
geofile = get_geofile(url)

path = 'kc_house_data.csv'
data = get_data(path)

data['date_map'] = pd.to_datetime(data['date']).dt.strftime('%Y-%B')
data['date'] = pd.to_datetime( data['date']).dt.strftime('%Y-%m-%d')
st.title('Dataframe head')
st.dataframe(data.head())

# add new features

data['price_m2'] = data['price'] / data['sqft_lot']


# overview


f_attributtes = st.sidebar.multiselect('Enter colluns', data.columns)
f_zipcode = st.sidebar.multiselect('Enter Zip Code', data['zipcode'].unique())

if f_attributtes != [] and f_zipcode != []:
    df_filter = data[data['zipcode'].isin(f_zipcode)][f_attributtes]
    data = data[data['zipcode'].isin(f_zipcode)]
elif f_attributtes == [] and f_zipcode != []:
    df_filter = data[data['zipcode'].isin(f_zipcode)]
    data = data[data['zipcode'].isin(f_zipcode)]
elif f_attributtes != [] and f_zipcode == []:
    df_filter = data[f_attributtes]
else:
    df_filter = data.copy()

st.title('Filtered Data Frame')
st.dataframe(df_filter)
st.markdown(f'Found Houses: {len(df_filter)}')

c1, c2 = st.columns((1, 1))
container = st.container()
# Statistic Descriptive

num_atributes = data.select_dtypes(include=['int64', 'float64'])
media = pd.DataFrame(num_atributes.apply(np.mean))
mediana = pd.DataFrame(num_atributes.apply(np.median))
std = pd.DataFrame(num_atributes.apply(np.std))
min_ = pd.DataFrame(num_atributes.apply(np.min))
max_ = pd.DataFrame(num_atributes.apply(np.max))
df_descriptive = pd.concat([media, mediana, std, min_, max_], axis=1).reset_index()
df_descriptive.columns = ['atributes', 'media', 'mediana', 'std', 'min', 'max']

# average metrics
df1 = data[['zipcode', 'id']].groupby('zipcode').count().reset_index()
df2 = data[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
df3 = data[['zipcode', 'price_m2']].groupby('zipcode').mean().reset_index()
df4 = data[['zipcode', 'sqft_living']].groupby('zipcode').mean().reset_index()

m1 = pd.merge(df1, df2, on='zipcode', how='inner')
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
df = pd.merge(m2, df4, on='zipcode', how='inner')

c1.title('Descritive')
c2.title('Average Metric')
c1.dataframe(df_descriptive)
c2.dataframe(df)

# density_map

density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                         zoom_start=9)

make_cluster = MarkerCluster().add_to(density_map)
for index, row in data.iterrows():
    folium.Marker([row['lat'], row['long']], popup=f'Sold {row["price"]} on {row["date"]}. Features:'
                                                   f'{row["sqft_lot"]}SQFT Lot,'
                                                   f'{row["bedrooms"]} Bedrooms,'
                                                   f'{row["bathrooms"]} Bathrooms,'
                                                   f'{row["yr_built"]} Year Built.').add_to(make_cluster)


c1.header('Locations')
with c1:
    folium_static(density_map)

c2.header('Price density')
zip_price = data[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
zip_price.columns = ['ZIP', 'PRICE']
zip_price = zip_price
geofile = geofile[geofile['ZIP'].isin(zip_price['ZIP'].tolist())]
region_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                        zoom_start=9)

folium.Choropleth(
    data=zip_price,
    geo_data=geofile,
    columns=['ZIP', 'PRICE'],
    key_on='feature.properties.ZIP',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='AVG Price',
    name='Choropleth'

).add_to(region_map)
folium.LayerControl().add_to(region_map)
with c2:
    folium_static(region_map)

#--------------------
# Distribuiçao dos imoveis por categoria comerciais
st.sidebar.title('Comercial Options')
st.title('Comercial Attributes')

#average price by year
yr_built_max = int(data['yr_built'].max())
yr_built_min = int(data['yr_built'].min())
st.sidebar.subheader('Select Max year build:')
f_year_built = st.sidebar.slider('Year build',yr_built_min,yr_built_max,yr_built_max)

year_built_data =  data.loc[data['yr_built'] <= f_year_built][['price','yr_built']].groupby('yr_built').mean().reset_index()
graph_yr_built = px.line(year_built_data, x = 'yr_built', y='price')
st.header('Average price per year built')
st.plotly_chart(graph_yr_built, use_container_width=True)
#average price by year

date_max = datetime.strptime(data['date'].max(), '%Y-%m-%d')
date_min = datetime.strptime(data['date'].min(), '%Y-%m-%d')
st.sidebar.subheader('Select Max date:')

f_date = st.sidebar.slider('Date', date_min, date_max, date_max)

data['date'] = pd.to_datetime(data['date'])
date_price =  data.loc[data['date'] <= f_date][['date','price']].groupby('date').mean().reset_index()
graph_date_price = px.line(date_price, x = 'date', y='price')
st.header('Average price per day')
st.plotly_chart(graph_date_price, use_container_width=True)

#-------HISTOGRAMA

st.header('Price Distribution')
st.sidebar.subheader('Select Max price')

max_price = int(data['price'].max())
min_price = int(data['price'].min())
avg_price = int(data['price'].mean())
f_price = st.sidebar.slider('Price', min_price,max_price,avg_price)

data_price = data.loc[data['price'] <= f_price]
fig = px.histogram(data_price, x='price', nbins=50)
st.plotly_chart(fig, use_container_width=True)

#--------Distribuiton

st.sidebar.title('Atributes options')
st.title('Houses attributes')
#_____filters

f_bedroooms = st.sidebar.selectbox('Max numbers of bedrooms',
                                   sorted(set(data['bedrooms']),reverse=True)
                                    )

f_bathrooms = st.sidebar.selectbox('Max numbers of bathrooms',
                                   sorted(set(data['bathrooms']), reverse=True)
                                    )

f_floors = st.sidebar.selectbox('Max numbers of floors',
                                    sorted(set(data['floors']),reverse=True)
                                    )
f_waterview = st.sidebar.checkbox('Only houses with Water view')


c1,c2 = st.columns((1,1))

#date_filtered
data_bedrroms_filtered = data.loc[data['bedrooms'] <= f_bedroooms]
data_bathroms_filtered = data.loc[data['bathrooms'] <= f_bedroooms]
data_floors_filtered = data.loc[data['floors'] <= f_bedroooms]
data_waterview_filtered = data['waterfront'].copy()
if f_waterview:
    data_waterview_filtered = data.loc[data['waterfront'] == 1]

#histograns
his_bedrooms = px.histogram(data_bedrroms_filtered,x = 'bedrooms', nbins= 19)
c1.plotly_chart(his_bedrooms, use_container_width=True)

his_bathrooms= px.histogram(data_bathroms_filtered,x = 'bathrooms', nbins= 19)
c2.plotly_chart(his_bathrooms, use_container_width=True)

his_floors= px.histogram(data_floors_filtered,x = 'floors', nbins= 19)
c1.plotly_chart(his_floors, use_container_width=True)

his_waterview= px.histogram(data_waterview_filtered,x = 'waterfront', nbins= 10)
c2.plotly_chart(his_waterview, use_container_width=True)

