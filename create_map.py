# coding: UTF-8

import folium
from folium import plugins
import pandas as pd
import branca.colormap as cm
import math
import webbrowser



def asakusa_map():
    zoom_asakusa = 13
    center_asakusa = [35.716677, 139.796637]

    map_asakusa = folium.Map(center_asakusa, zoom_start=zoom_asakusa)


    df = pd.read_csv("./asakusa.csv", header=0)

    df_sweets = df[df['category'] == 'スイーツ']
    fg_sweets = folium.FeatureGroup(name = 'スイーツ')

    df_gohan = df[df['category'] == 'ご飯']
    fg_gohan = folium.FeatureGroup(name='ご飯')

    df_kanko = df[df['category'] == '観光']
    fg_kanko = folium.FeatureGroup(name='観光')

    for n in df_sweets.index:
        lat_sw = df_sweets['latitude_raw'][n]
        lon_sw = df_sweets['longitude_raw'][n]
        name_sw = '<span style="white-space: nowrap;">' + str(df_sweets['name'][n]) + '</span>'

        
        x = folium.Marker(
            location=[lat_sw, lon_sw],
            popup= name_sw,
            icon=folium.Icon(color='red', icon='heart')
        )
        fg_sweets.add_child(x)
    map_asakusa.add_child(fg_sweets)

    for m in df_gohan.index:
        lat_gh = df_gohan['latitude_raw'][m]
        lon_gh = df_gohan['longitude_raw'][m]
        name_gh = '<span style="white-space: nowrap;">' + str(df_gohan['name'][m]) + '</span>'

        
        y = folium.Marker(
            location=[lat_gh, lon_gh],
            popup= name_gh,
            icon=folium.Icon(color='green', icon='glass')
        )
        fg_gohan.add_child(y)
    map_asakusa.add_child(fg_gohan)

    for l in df_kanko.index:
        lat_kk = df_kanko['latitude_raw'][l]
        lon_kk = df_kanko['longitude_raw'][l]
        url = str(df_kanko['image_url'][l])
        # flash(url)
        if 'https' in url:
            name_kk = '<span style="white-space: nowrap;">' + str(df_kanko['name'][l]) + '</span>' + '<img width="240" src=' + str(df_kanko['image_url'][l]) +'>'
        else:
            name_kk = '<span style="white-space: nowrap;">' + str(df_kanko['name'][l]) + '</span>'

        z = folium.Marker(
            location=[lat_kk, lon_kk],
            popup= name_kk,
            icon=folium.Icon(color='blue', icon='search')
        )
        fg_kanko.add_child(z)
    map_asakusa.add_child(fg_kanko)

    folium.LayerControl().add_to(map_asakusa)
    plugins.LocateControl().add_to(map_asakusa)

    map_asakusa.save('map.html')
    webbrowser.open('map.html')
    

    


if __name__ == "__main__":
    asakusa_map()
