import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# title
st.title("Aplikasi Visualisasi Data Covid-19")

# Sidebar
st.sidebar.subheader("Pengaturan Grafik")


# @st.cache(allow_output_mutation=True)
@st.experimental_memo()
def load_data(data, sheet_name):
    df = pd.read_excel(data, sheet_name=sheet_name)
    return df


dataset = 'data/COVID-19 Indonesia.xlsx'


df_total = load_data(dataset, 'Statistik Harian')
daily_cases = load_data(dataset, 'Kasus Aktif')
data_sembuh = load_data(dataset, 'Sembuh Harian')
data_meninggal = load_data(dataset, 'Meninggal Harian')
day_statistic = load_data(dataset, 'Statistik Harian')


# READ DATASET AND PROCESSING
daily_cases.fillna(0, inplace=True)
daily_cases.set_index('Date', inplace=True)
daily_cases.abs()
daily_cases.loc[(daily_cases['DIY'] < 0)] = 1.0
daily_cases.loc[(daily_cases['Riau'] < 0)] = 1.0
daily_cases['Kasus_Aktif_Nasional'] = daily_cases.sum(axis=1)
# data sembuh
data_sembuh.fillna(0, inplace=True)
data_sembuh.set_index('Date', inplace=True)
# data meninggal
data_meninggal.fillna(0, inplace=True)
data_meninggal.set_index('Date', inplace=True)
# data nasional
data_sembuh['Nasional'] = data_sembuh.sum(axis=1)
data_meninggal['Nasional'] = data_meninggal.sum(axis=1)
daily_cases['Sembuh_Harian_Nasional'] = data_sembuh['Nasional']
daily_cases['Meninggal_Harian_Nasional'] = data_meninggal['Nasional']
daily_cases.fillna(0, inplace=True)
# Data Vaksin
data_vaksin = df_total[[
    'Date', 'Dosis pertama (harian)', 'Dosis kedua (harian)']]
data_vaksin.rename({'Dosis pertama (harian)': 'Dosis 1',
                   'Dosis kedua (harian)': 'Dosis 2'}, axis=1, inplace=True)
data_vaksin['Dosis 1'].fillna(0, inplace=True)
data_vaksin['Dosis 2'].fillna(0, inplace=True)
data_vaksin.dropna(inplace=True)
data_vaksin.set_index('Date', inplace=True)
# Data Vaksin Pie Chart
day_statistic.set_index('Date', inplace=True)
# Data vaksin berdasarkan dosis
dosis_pertama_kesehatan = day_statistic.loc[
    '2021-08-23']['Dosis pertama (SDM kesehatan)'].values[0]
dosis_kedua_kesehatan = day_statistic.loc[
    '2021-08-23']["Dosis kedua (SDM kesehatan)"].values[0]
dosis_ketiga_kesehatan = day_statistic.loc[
    '2021-08-23']["Dosis ketiga (SDM kesehatan)"].values[0]
dosis_pertama_publik = day_statistic.loc[
    '2021-08-23']["Dosis pertama (petugas publik)"].values[0]
dosis_kedua_publik = day_statistic.loc[
    '2021-08-23']["Dosis kedua (petugas publik)"].values[0]
dosis_pertama_lansia = day_statistic.loc[
    '2021-08-23']["Dosis pertama (lansia)"].values[0]
dosis_kedua_lansia = day_statistic.loc['2021-08-23']["Dosis kedua (lansia)"].values[0]
dosis_pertama_umum = day_statistic.loc[
    '2021-08-23']["Dosis pertama (warga umum)"].values[0]
dosis_kedua_umum = day_statistic.loc['2021-08-23']["Dosis kedua (warga umum)"].values[0]
dosis_pertama_remaja = day_statistic.loc[
    '2021-08-23']["Dosis pertama (remaja)"].values[0]
dosis_kedua_remaja = day_statistic.loc['2021-08-23']["Dosis kedua (remaja)"].values[0]
dosis_pertama_vakgor = day_statistic.loc[
    '2021-08-23']["Dosis pertama (Vakgor)"].values[0]
dosis_kedua_vakgor = day_statistic.loc['2021-08-23']["Dosis kedua (Vakgor)"].values[0]
# jumlah total vaksin masing_masing bidang
dosis_kesehatan = dosis_pertama_kesehatan + \
    dosis_kedua_kesehatan + dosis_ketiga_kesehatan
dosis_publik = dosis_pertama_publik + dosis_kedua_publik
dosis_lansia = dosis_pertama_lansia + dosis_kedua_lansia
dosis_umum = dosis_pertama_umum + dosis_kedua_umum
dosis_remaja = dosis_pertama_remaja + dosis_kedua_remaja
dosis_vakgor = dosis_pertama_vakgor + dosis_kedua_vakgor
vaksin_pertama_total = dosis_pertama_kesehatan + dosis_pertama_publik + \
    dosis_pertama_lansia + dosis_pertama_umum + \
    dosis_pertama_remaja + dosis_pertama_vakgor
vaksin_kedua_total = dosis_kedua_kesehatan + dosis_kedua_publik + \
    dosis_kedua_lansia + dosis_kedua_umum + dosis_kedua_remaja + dosis_kedua_vakgor
dosis_total = dosis_kesehatan + dosis_publik + \
    dosis_lansia + dosis_umum + dosis_remaja + dosis_vakgor


# Membuat checkbox untuk menampilkan data atau tidak
show_dataframe = st.sidebar.checkbox("Tampilkan dataframe")
show_data_covid = st.sidebar.radio("Data Covid-19 Indonesia", ("Data Covid-19 Harian",
                                                               "Data Covid-19 per provinsi", "Data vaksinasi"))
# st.radio(
# ...     "What's your favorite movie genre",
# ...     ('Comedy', 'Drama', 'Documentary'))
# show_data_province = st.sidebar.checkbox("Data Covid-19 per provinsi")
# show_data_vaksin = st.sidebar.checkbox("Data vaksinasi")


if show_dataframe:
    st.write(data_sembuh)

# data harian covid-19
if show_data_covid == "Data Covid-19 Harian":
    column_select = st.sidebar.selectbox(
        label="Pilih Kolom",
        options=['Kasus Harian Nasional',
                 'Data Pasien Sembuh', 'Data Pasien Meninggal', 'Semua Data', "PPKM"])
    if column_select == 'Kasus Harian Nasional':
        fig = px.line(daily_cases, x=daily_cases.index, y='Kasus_Aktif_Nasional',
                      labels={
                          "Kasus_Aktif_Nasional": "Jumlah Kasus Harian Nasional"},
                      title="Kasus Harian Covid-19 di Indonesia")
        fig.update_layout(
            title_font_size=35,
            title={'y': 0.9,
                   'x': 0.5})

        st.plotly_chart(fig)

    # Data pasien sembuh
    elif column_select == 'Data Pasien Sembuh':
        fig = px.line(daily_cases, x=daily_cases.index, y=['Sembuh_Harian_Nasional'],
                      labels={"value": "Jumlah",
                              "Date": "Tanggal"},
                      title="Data Pasien Sembuh Covid-19 di Indonesia")
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)

    # Data pasien Meninggal
    elif column_select == 'Data Pasien Meninggal':
        fig = px.line(daily_cases, x=daily_cases.index, y=['Meninggal_Harian_Nasional'],
                      labels={"value": "Jumlah",
                              "Date": "Tanggal"},
                      title="Data Pasien Meninggal di Indonesia")
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)

    # Semua Data
    elif column_select == 'Semua Data':
        fig = px.line(daily_cases, x=daily_cases.index, y=['Kasus_Aktif_Nasional', 'Sembuh_Harian_Nasional', 'Meninggal_Harian_Nasional'],
                      labels={"value": "Jumlah",
                              "Date": "Tanggal"},
                      title="Pergerakan Kasus Aktif, Sembuh dan Meninggal Covid-19 di Indonesia",
                      color_discrete_map={
            "Kasus_Aktif_Nasional": "#42adf5",
            "Sembuh_Harian_Nasional": "#42f58d",
            "Meninggal_Harian_Nasional": "red"})

        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)

    # PPKM Darurat
    elif column_select == 'PPKM':
        jumlah_tertinggi = daily_cases['Kasus_Aktif_Nasional'].max()
        kasus_tertinggi = daily_cases.loc[(
            daily_cases['Kasus_Aktif_Nasional'] == jumlah_tertinggi)]
        fig = px.line(daily_cases, x=daily_cases.index, y='Kasus_Aktif_Nasional',
                      labels={
                          "Kasus_Aktif_Nasional": "Jumlah Kasus Harian Nasional"},
                      title="Efek PPKM terhadap Kasus Covid-19")
        fig.update_layout(
            title_font_size=35,
            title={'y': 0.9,
                   'x': 0.5})

        fig.update_xaxes(
            rangeslider_visible=True,
            tickformatstops=[
                dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                dict(dtickrange=["M12", None], value="%Y Y")
            ]
        )

        fig.add_vrect(
            x0="2021-01-11", x1="2021-02-08",
            fillcolor="#ebb134", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="PPKM",
            annotation_position="top left",

        )
        fig.add_vrect(
            x0="2021-02-09", x1="2021-06-28",
            fillcolor="#ebcc34", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="PPKM Mikro",
            annotation_position="top left"
        )
        fig.add_vrect(
            x0="2021-07-03", x1="2021-07-25",
            fillcolor="#eb7734", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="PPKM darurat",
            annotation_position="top left"
        )
        fig.add_vrect(
            x0="2021-07-26", x1="2021-08-23",
            fillcolor="#eb4934", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="PPKM Level 4",
            annotation_position="top left"
        )

        fig.update_annotations(textangle=90)
        st.plotly_chart(fig)


# Data Provinsi
if show_data_covid == "Data Covid-19 per provinsi":
    color_plot = st.sidebar.selectbox(
        label="Pilih Warna Chart",
        options=['blue', 'red', 'green', 'black'])
    value = st.sidebar.slider('Tampilkan Jumlah Provinsi ', 1, 34, 5)
    if color_plot == 'blue':
        data_provinsi = daily_cases.drop(columns=['Kasus_Aktif_Nasional', 'Sembuh_Harian_Nasional', 'Meninggal_Harian_Nasional']).sum(
        ).sort_values(ascending=False)[:value]
        fig = px.bar(data_provinsi, labels={
                     "value": "Jumlah", "index": "Provinsi"}, title="{} Provinsi Kasus Covid Terbanyak".format(value))
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)
    elif color_plot == 'red':
        data_provinsi = daily_cases.drop(columns=['Kasus_Aktif_Nasional', 'Sembuh_Harian_Nasional', 'Meninggal_Harian_Nasional']).sum(
        ).sort_values(ascending=False)[:value]
        fig = px.bar(data_provinsi, labels={
                     "value": "Jumlah", "index": "Provinsi"},  color_discrete_sequence=['red'],  title="{} Provinsi Kasus Covid Terbanyak".format(value))
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)
    elif color_plot == 'green':
        data_provinsi = daily_cases.drop(columns=['Kasus_Aktif_Nasional', 'Sembuh_Harian_Nasional', 'Meninggal_Harian_Nasional']).sum(
        ).sort_values(ascending=False)[:value]
        fig = px.bar(data_provinsi, labels={
                     "value": "Jumlah", "index": "Provinsi"},  color_discrete_sequence=['green'],   title="{} Provinsi Kasus Covid Terbanyak".format(value))
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)
    elif color_plot == 'black':
        data_provinsi = daily_cases.drop(columns=['Kasus_Aktif_Nasional', 'Sembuh_Harian_Nasional', 'Meninggal_Harian_Nasional']).sum(
        ).sort_values(ascending=False)[:value]
        fig = px.bar(data_provinsi, labels={
                     "value": "Jumlah", "index": "Provinsi"},  color_discrete_sequence=['black'],   title="{} Provinsi Kasus Covid Terbanyak".format(value))
        fig.update_layout(
            title_font_size=25,
            title={'y': 0.9, 'x': 0.5})
        st.plotly_chart(fig)

# DATA VAKSIN
if show_data_covid == "Data vaksinasi":
    chart_select = st.sidebar.selectbox(label="Pilih Jenis Data Vaksin",
                                        options=['Line Plot', 'Piechart'])
    if chart_select == "Line Plot":
        line_chart_select = st.sidebar.selectbox(
            label="Pilih Jenis Data Vaksin",
            options=[
                'Data Vaksin Nasional (Dosis 1 dan 2)', 'Data Vaksin Harian (Dosis 1, 2 dan 3)']
        )
        if line_chart_select == 'Data Vaksin Nasional (Dosis 1 dan 2)':
            fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(16, 20))

            data_vaksin['Dosis 1'].rolling(window=7).mean().plot(
                kind='line', label='Vaksin Dosis 1', ax=ax[0])
            data_vaksin['Dosis 2'].rolling(window=7).mean().plot(
                kind='line', label='Vaksin Dosis 2', ax=ax[0], color="green")
            daily_cases['Kasus_Aktif_Nasional'].plot(
                kind='line', label='Kasus Harian Nasional', ax=ax[0], color="#eb5e34")

            ax[0].set_title('Vaksinasi Total = Dosis pertama :{} orang | Dosis kedua :{} orang'.format(
                data_vaksin['Dosis 1'].sum(), data_vaksin['Dosis 2'].sum()))
            ax[0].legend()
            ax[0].set_xlim('2021-01-01', '2021-08-23')

            ax[0].axvline(x='2021-07-15', color='r',
                          linewidth=4, label='Puncak Kasus')

            ax[0].set_title('Vaksinasi Harian, Dosis1:{} orang, Dosis2:{} orang'.format(
                data_vaksin['Dosis 1'].sum(), data_vaksin['Dosis 2'].sum()))
            ax[0].legend()
            ax[0].set_xlim('2021-01-01', '2021-08-23')

            data_vaksin['Dosis 1'].cumsum().plot(
                kind='line', ax=ax[1], label='Vaksin Dosis 1')
            data_vaksin['Dosis 2'].cumsum().plot(
                kind='line', ax=ax[1], label='Vaksin Dosis 2')
            ax[1].set_xlim('2021-01-01', '2021-08-23')
            ax[1].set_ylabel('Jumlah Vaksinasi (Puluh Juta Orang)')
            ax[1].set_title('Vaksinasi Kumulatif per Tanggal 23 Agustus 2021')
            ax[1].legend()
            ax[1].set_xlim('2021-01-01', '2021-08-23')

            fig.suptitle("Data Vaksin Nasional", fontsize=20)
            st.pyplot(plt)

        elif line_chart_select == 'Data Vaksin Harian (Dosis 1, 2 dan 3)':
            fig = go.Figure(layout_title_text="Data Vaksin Harian")
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (SDM kesehatan)'],
                name='Dosis pertama (SDM kesehatan)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (SDM kesehatan)'],
                name='Dosis kedua (SDM kesehatan)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis ketiga (SDM kesehatan)'],
                name='Dosis ketiga (SDM kesehatan)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (petugas publik)'],
                name='Dosis pertama (petugas publik)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (petugas publik)'],
                name='Dosis kedua (petugas publik)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (lansia)'],
                name='Dosis pertama (lansia)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (lansia)'],
                name='Dosis kedua (lansia)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (warga umum)'],
                name='Dosis pertama (warga umum)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (warga umum)'],
                name='Dosis kedua (warga umum)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (remaja)'],
                name='Dosis pertama (remaja)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (remaja)'],
                name='Dosis kedua (remaja)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis pertama (Vakgor)'],
                name='Dosis pertama (vakgor)'
            ))
            fig.add_trace(go.Scatter(
                x=day_statistic.index,
                y=day_statistic['Dosis kedua (Vakgor)'],
                name='Dosis kedua (vakgor)'
            ))
            # Update layout properties
            fig.update_layout(
                title_font_size=35,
                title={'y': 0.9,
                       'x': 0.5})
            fig.update_layout(xaxis_range=["2021-01-01", "2021-08-23"])
            fig.update_xaxes(
                rangeslider_visible=True,
                tickformatstops=[
                    dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                    dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                    dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                    dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                    dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                    dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                    dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                    dict(dtickrange=["M12", None], value="%Y Y")
                ]
            )
            st.plotly_chart(fig)

    elif chart_select == "Piechart":
        pie_chart_select = st.sidebar.selectbox(
            label="Pilih Jenis Data Vaksin",
            options=['Dosis 1', 'Dosis 2', 'Total Vaksin',
                     'Distribusi Vaksin Dosis 1, 2, 3']
        )
        if pie_chart_select == 'Dosis 1':
            # Vaksin Pertama
            labels = 'Petugas Kesehatan', 'Petugas Publik', 'Lansia', 'warga umum', 'remaja', 'gotong royong'
            data = [dosis_pertama_kesehatan, dosis_pertama_publik, dosis_pertama_lansia,
                    dosis_pertama_umum, dosis_pertama_remaja, dosis_pertama_vakgor]
            # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots(figsize=(16, 9))
            ax1.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.axis('equal')
            ax1.legend()
            ax1.set_title('jumlah total vaksin pertama = {}'.format(
                vaksin_pertama_total), fontsize=20)
            st.pyplot(plt)

        elif pie_chart_select == 'Dosis 2':
            # vaksin kedua
            labels = 'Petugas Kesehatan', 'Petugas Publik', 'Lansia', 'warga umum', 'remaja', 'gotong royong'
            data = [dosis_kedua_kesehatan, dosis_kedua_publik, dosis_kedua_lansia,
                    dosis_kedua_umum, dosis_kedua_remaja, dosis_kedua_vakgor]
            # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots(figsize=(16, 9))
            ax1.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.axis('equal')
            ax1.legend()
            ax1.set_title('jumlah total vaksin kedua = {}'.format(
                vaksin_kedua_total), fontsize=20)
            st.pyplot(plt)

        elif pie_chart_select == 'Total Vaksin':
            # Dosis vaksin di tiap kategori
            labels = 'Petugas Kesehatan', 'Petugas Publik', 'Lansia', 'warga umum', 'remaja', 'gotong royong'
            data = [dosis_kesehatan, dosis_publik, dosis_lansia,
                    dosis_umum, dosis_remaja, dosis_vakgor]
            # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots(figsize=(16, 9))
            ax1.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.axis('equal')
            ax1.legend()
            ax1.set_title('jumlah total vaksin = {}'.format(
                dosis_total), fontsize=20)
            st.pyplot(plt)

        elif pie_chart_select == 'Distribusi Vaksin Dosis 1, 2, 3':
            # Perbandingan vaksin pertama, kedua dan ketiga
            labels = 'vaksin pertama', 'vaksin kedua', 'vaksin ketiga'
            data = [vaksin_pertama_total,
                    vaksin_kedua_total, dosis_ketiga_kesehatan]
            # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots(figsize=(16, 9))
            ax1.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.axis('equal')
            ax1.legend()
            ax1.set_title('Perbandingan distribusi vaksin',  fontsize=20)
            st.pyplot(plt)
