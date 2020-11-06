import pandas as pd
import geopandas as gpd
import json
from bokeh.io import output_notebook, show, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, row, column

shapefile = './assets/countries/ne_110m_admin_0_countries.shp'
datafiles = []
PATH = '../../../datasets/Positionwise/{}.csv'
for position in 'full_backs', 'centre_backs', 'midfielders', 'wingers', 'free_roamers', 'strikers':
    datafiles.append(pd.read_csv(PATH.format(position))['nationality'])

df = pd.concat(datafiles).reset_index()

gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']
new = []
for country in gdf['country']:
    value = 0
    for nationality in df['nationality']:
        if country == nationality:
            value+=1
    new.append(value)    
gdf['Number'] = new

# print(gdf[gdf['country'] == 'Antarctica'])
gdf = gdf.drop(gdf.index[159])

#Perform left merge to preserve every row in gdf.
merged = gdf.merge(df, left_on = 'country_code', right_on = 'nationality', how = 'left')

#Replace NaN values to string 'No data'.
merged.fillna('No data', inplace = True)

#Read data to json
merged_json = json.loads(merged.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40)

#Define custom tick labels for color bar.
tick_labels = {'0': '0', '5': '50', '10':'100', '15':'150', '20':'200', '25':'250', '30':'300','35':'350', '40': '400'}

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

#Create figure object.
p = figure(title = 'Number of players from each country', plot_height = 600 , plot_width = 950, toolbar_location = None)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'Number', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

#Specify figure layout.
p.add_layout(color_bar, 'below')

#Display figure inline in Jupyter Notebook.
output_notebook()

#Display figure.
show(p)

merged = gdf.merge(df, left_on = 'country_code', right_on = 'nationality', how = 'left')
merged.fillna('No data', inplace = True)
merged_json = json.loads(merged.to_json())
json_data = json.dumps(merged_json)

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]

#Reverse color order so that dark blue is highest obesity.
palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 400, nan_color = '#d9d9d9')

#Define custom tick labels for color bar.
tick_labels = {'0': '0', '5': '50', '10':'100', '15':'150', '20':'200', '25':'250', '30':'300','35':'350', '40': '400'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Country/Region','@country'),('Number of Players', '@Number')])


#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)


#Create figure object.
p = figure(title = 'Number of players from each country', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :'Number', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)


p.add_layout(color_bar, 'below')
p.title.text = 'Nationalities of Football Players'


layout = column(p)
curdoc().add_root(layout)

#Display plot inline in Jupyter notebook
output_notebook()

#Display plot
show(layout)