import folium
import pandas as pd
import branca.colormap as cm
from flask import Flask, render_template, flash
import math

app = Flask(__name__)
app.config["SECRET_KEY"] = "sample1203"

@app.route('/asakusa/')
def asakusa_map():
    zoom_asakusa = 15
    center_asakusa = [35.716677, 139.796637]

    map_asakusa = folium.Map(center_asakusa, zoom_start=zoom_asakusa)


    df = pd.read_csv("./asakusa.csv", header=0)

    df_sweets = df[df['category'] == 'スイーツ']
    df_gohan = df[df['category'] == 'ご飯']
    df_kanko = df[df['category'] == '観光']

    for n in df_sweets.index:
        lat_sw = df_sweets['latitude_raw'][n]
        lon_sw = df_sweets['longitude_raw'][n]
        name_sw = '<span style="white-space: nowrap;">' + str(df_sweets['name'][n]) + '</span>'

        #flash(name_sw)
        
        folium.Marker(
            location=[lat_sw, lon_sw],
            popup= name_sw,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(map_asakusa)
        
    for m in df_gohan.index:
        lat_gh = df_gohan['latitude_raw'][m]
        lon_gh = df_gohan['longitude_raw'][m]
        name_gh = '<span style="white-space: nowrap;">' + str(df_gohan['name'][m]) + '</span>'

        #flash(name_sw)
        
        folium.Marker(
            location=[lat_gh, lon_gh],
            popup= name_gh,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map_asakusa)

    for l in df_kanko.index:
        lat_kk = df_kanko['latitude_raw'][l]
        lon_kk = df_kanko['longitude_raw'][l]
        url = str(df_kanko['image_url'][l])
        # flash(url)
        if 'https' in url:
            name_kk = '<span style="white-space: nowrap;">' + str(df_kanko['name'][l]) + '</span>' + '<img width="240" src=' + str(df_kanko['image_url'][l]) +'>'
        else:
            name_kk = '<span style="white-space: nowrap;">' + str(df_kanko['name'][l]) + '</span>'

        
        folium.Marker(
            location=[lat_kk, lon_kk],
            popup= name_kk,
            icon=folium.Icon(color='blue', icon='cloud')
        ).add_to(map_asakusa)


    '''
    for i in range(1, len(df.index)-1):

        lat = df['latitude_raw'][i]
        lon = df['longitude_raw'][i]
        kanko_name = '<span style="white-space: nowrap;">' + str(df['name'][i]) + '</span>'

        if not math.isnan(lat) :
            folium.Marker(location = [lat, lon], 
            popup=kanko_name,
            icon =folium.Icon(icon='cloud')).add_to(map_asakusa)
            '''

    return render_template('index.html', map=map_asakusa._repr_html_())
    
@app.route('/')
def visualize_map():
    zoom = 10
    center = [35.181389, 136.906389]
    canvas = folium.Figure(width=1000, height=500)

    map = folium.Map(center, zoom_start=zoom).add_to(canvas)

    colorscale = cm.LinearColormap(
        ['#e6e6fa', '#b0c4de', '#4682b4', '#4169e1'],
        vmin=0, vmax=300000,
        caption='Color Scale for Map'
    )

    # add polygons from geoJson on the map
    geoJson = './aichi_2017.json'
    folium.GeoJson(geoJson,
                    popup = folium.GeoJsonPopup(fields=['CITYNAME', 'JINKO']),
                    style_function = lambda feature : {
                        'fillcolor' : colorscale(feature['properties']['JINKO']),
                        'color' : 'blue',
                        'weight' : 2,
                        'fillOpacity' : 0.7,
                        'lineOpacity' : 1.0,
                    },
                    ).add_to(map)
    colorscale.add_to(map)
    return render_template('index.html', map=map._repr_html_())
    


if __name__ == "__main__":
    app.run(debug=True)
