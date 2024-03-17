#Import library yang diperlukan
import streamlit as st
import pandas as pd
import folium as fm
from streamlit_folium import st_folium

#Input judul dan subjudul peta
APP_TITLE = 'DISTRIBUSI FUNGSIONAL PRANATA KOMPUTER BADAN PUSAT STATISTIK'
APP_SUB_TITLE = 'Sumber: Pengolahan Data Internal Kepegawaian BPS RI, 14 Maret 2024'

#FUNGSI UNTUK MENAMPILKAN PETA TEMATIK
def display_map(df):
    map = fm.Map(location=[0.4948, 117.1436], zoom_start=4.5, scrollWheelZoom=False, tiles='CartoDB positron')

    choropleth = fm.Choropleth(
        geo_data='data/indonesia-prov.geojson',
        data=df,
        name='choroplet',
        columns=['satuan_kerja', 'jumlah'],
        key_on='feature.properties.Propinsi',
        fill_color="YlGn",
        legend_name="Jumlah Pejabat Fungsional (pegawai)",
        line_opacity=0.2,
        fill_opacity=0.7,
        highlight=True
    )

    choropleth.geojson.add_to(map)

    #Mengatur format tampilan tooltip
    for feature in choropleth.geojson.data['features']:
        prov_name = feature['properties']['Propinsi']

        total_prakom = df[df["satuan_kerja"] == prov_name]['jumlah'].sum()
        prakom_utama = df[(df["jabatan"] == "Pranata Komputer Ahli Utama") & (df["satuan_kerja"] == prov_name)]
        prakom_madya = df[(df["jabatan"] == "Pranata Komputer Ahli Madya") & (df["satuan_kerja"] == prov_name)]
        prakom_muda = df[(df["jabatan"] == "Pranata Komputer Ahli Muda") & (df["satuan_kerja"] == prov_name)]
        prakom_pertama = df[(df["jabatan"] == "Pranata Komputer Ahli Pertama") & (df["satuan_kerja"] == prov_name)]
        prakom_penyelia = df[(df["jabatan"] == "Pranata Komputer Penyelia") & (df["satuan_kerja"] == prov_name)]
        prakom_mahir = df[(df["jabatan"] == "Pranata Komputer Mahir") & (df["satuan_kerja"] == prov_name)]
        prakom_terampil = df[(df["jabatan"] == "Pranata Komputer Terampil") & (df["satuan_kerja"] == prov_name)]
        
        feature['properties']['total_prakom']     = prov_name + ': ' + str(total_prakom) + ' Pegawai' if not total_prakom == 0      else prov_name + ': 0 Pegawai'
        feature['properties']['prakom_utama']     = 'Ahli Utama  : ' + str(prakom_utama.iloc[0]["jumlah"]) if not prakom_utama.empty       else 'Ahli Utama  : 0'
        feature['properties']['prakom_madya']     = 'Ahli Madya  : ' + str(prakom_madya.iloc[0]["jumlah"]) if not prakom_madya.empty       else 'Ahli Madya  : 0'
        feature['properties']['prakom_muda']      = 'Ahli Muda   : ' + str(prakom_muda.iloc[0]["jumlah"]) if not prakom_muda.empty         else 'Ahli Muda   : 0'
        feature['properties']['prakom_pertama']   = 'Ahli Pertama: ' + str(prakom_pertama.iloc[0]["jumlah"]) if not prakom_pertama.empty   else 'Ahli Pertama: 0'
        feature['properties']['prakom_penyelia']  = 'Penyelia    : ' + str(prakom_penyelia.iloc[0]["jumlah"]) if not prakom_penyelia.empty else 'Penyelia    : 0'
        feature['properties']['prakom_mahir']     = 'Mahir       : ' + str(prakom_mahir.iloc[0]["jumlah"]) if not prakom_mahir.empty       else 'Mahir       : 0'
        feature['properties']['prakom_terampil']  = 'Terampil    : ' + str(prakom_terampil.iloc[0]["jumlah"]) if not prakom_terampil.empty else 'Terampil    : 0'

    #Menampilkan tooltip
    choropleth.geojson.add_child(
        fm.features.GeoJsonTooltip([
            'total_prakom',
            'prakom_utama',
            'prakom_madya',
            'prakom_muda',
            'prakom_pertama',
            'prakom_penyelia',
            'prakom_mahir',
            'prakom_terampil',
        ], 
        labels=False)
    )
    
    st_map = st_folium(map, width=1200, height=600)

    prov_name = ''
    if st_map['last_active_drawing']:
        st.write("**Detail Propinsi " + prov_name + ":**")
        st.write('Total Pejabat  : ' + str(total_prakom) + ' Pegawai' if not total_prakom == 0             else '0 Pegawai')
        st.write('1. Ahli Utama  : ' + str(prakom_utama.iloc[0]["jumlah"]) if not prakom_utama.empty       else '1. Ahli Utama  : 0')
        st.write('2. Ahli Madya  : ' + str(prakom_madya.iloc[0]["jumlah"]) if not prakom_madya.empty       else '2. Ahli Madya  : 0')
        st.write('3. Ahli Muda   : ' + str(prakom_muda.iloc[0]["jumlah"]) if not prakom_muda.empty         else '3. Ahli Muda   : 0')
        st.write('4. Ahli Pertama: ' + str(prakom_pertama.iloc[0]["jumlah"]) if not prakom_pertama.empty   else '4. Ahli Pertama: 0')
        st.write('5. Penyelia    : ' + str(prakom_penyelia.iloc[0]["jumlah"]) if not prakom_penyelia.empty else '5. Penyelia    : 0')
        st.write('6. Mahir       : ' + str(prakom_mahir.iloc[0]["jumlah"]) if not prakom_mahir.empty       else '6. Mahir       : 0')
        st.write('7. Terampil    : ' + str(prakom_terampil.iloc[0]["jumlah"]) if not prakom_terampil.empty else '7. Terampil    : 0')
        prov_name = st_map['last_active_drawing']['properties']['Propinsi']

    return prov_name

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Memuat Data
    df_prakom = pd.read_excel('data/rekap_prakom_17032024.xlsx')

    #Menampilkan Peta Tematik
    display_map(df_prakom)  


if __name__ == "__main__":
    main()
