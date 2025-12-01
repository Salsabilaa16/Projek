import streamlit as st
import pandas as pd
import os
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import json

st.set_page_config(layout="wide", page_title="Dashboard Kemiskinan")

st.markdown("""
    <style>

    body {
        background-color: #f5f7fb;
    }

    .metric-card {
        background: white;
        padding: 8px;
        text-align: center;
    }

    .chart-card {
        background: white;
        padding: 8px;
        text-align: center;
    }

    h2, h3, h4 {
        font-family: "Arial";
    }
            
    .simpan {
    display: flex;
    justify-content: flex-end;
    }
            
    </style>
""", unsafe_allow_html=True)

st.title("Analisis Kemiskinan Kabupaten Tulungagung")

df = pd.read_excel("Kemiskinan.xlsx")
df.columns = df.columns.str.strip()
df_kemiskinan = df[df["Tahun"].between(2014, 2024)]
df_lain = df[df["Tahun"] >= 2020]

df_kab = pd.read_excel("Kemiskinan Kabupaten Kota.xlsx", sheet_name=0, header=2)
df_kab.columns = df_kab.columns.str.strip()

with open("id-ji.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

latest = df_kemiskinan.sort_values("Tahun").iloc[-1]
jumlah_miskin = latest.get("Penduduk Miskin", 0)

tab1, tab2 , tab3= st.tabs(["Input Data","Penduduk","Sosial-Ekonomi"])

with tab1:
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, step=1)

    col1, col2, col3 = st.columns(3)

    with col1:
        jumlah_penduduk = st.number_input("Jumlah Penduduk", min_value=0.0)
        penduduk_miskin = st.number_input("Penduduk Miskin", min_value=0.0)
        persentase_miskin = st.number_input("Persentase Penduduk Miskin (%)", min_value=0.0, max_value=100.0)
        garis_kemiskinan = st.number_input("Garis Kemiskinan", min_value=0.0)
        kedalaman = st.number_input("Indeks Kedalaman Kemiskinan", min_value=0.0)
        keparahan = st.number_input("Indeks Keparahan Kemiskinan", min_value=0.0)
        gini = st.number_input("Gini Ratio", min_value=0.0, max_value=1.0)
        t_smp = st.number_input("Pendidikan Tamat <SD", min_value=0.0)

    with col2:
        sd_smp = st.number_input("Pendidikan Tamat SD/SMP", min_value=0.0)
        sma = st.number_input("Pendidikan Tamat SMA", min_value=0.0)
        tidak_bekerja = st.number_input("Tidak Bekerja", min_value=0.0)
        bekerja_informal = st.number_input("Bekerja Informal", min_value=0.0)
        bekerja_formal = st.number_input("Bekerja Formal", min_value=0.0)
        bekerja_pertanian = st.number_input("Bekerja Pertanian", min_value=0.0)
        bekerja_nonpertanian = st.number_input("Bekerja Bukan Pertanian", min_value=0.0)
        melek_huruf = st.number_input("Angka Melek Huruf", min_value=0.0, max_value=100.0)

    with col3:
        aps_7_12 = st.number_input("APS 7–12 Tahun", min_value=0.0, max_value=100.0)
        aps_13_15 = st.number_input("APS 13–15 Tahun", min_value=0.0, max_value=100.0)
        air_layak = st.number_input("Air Layak (%)", min_value=0.0, max_value=100.0)
        jamban = st.number_input("Jamban Sendiri/Bersama (%)", min_value=0.0, max_value=100.0)
        keluhan_ya = st.number_input("Keluhan Kesehatan (Ya)", min_value=0.0)
        keluhan_tidak = st.number_input("Keluhan Kesehatan (Tidak)", min_value=0.0)
        jamkes_punya = st.number_input("Jamkes (Punya)", min_value=0.0)
        jamkes_tidak = st.number_input("Jamkes (Tidak Punya)", min_value=0.0)

        st.markdown('<div class:"simpan">', unsafe_allow_html=True)
        simpan = st.button("Simpan")
        st.markdown("</div>", unsafe_allow_html=True)

        if simpan:
            file_path = "Kemiskinan.xlsx"

            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                df.columns = df.columns.str.strip()
            else:
                df = pd.DataFrame(columns=[
                    "Tahun", "Jumlah Penduduk", "Penduduk Miskin", "Persentase Penduduk Miskin",
                    "Garis Kemiskinan", "Indeks Kedalaman Kemiskinan", "Indeks Keparahan Kemiskinan",
                    "Gini Ratio", "Pendidikan Tamat <SD", "Pendidikan Tamat SD/SMP", "Pendidikan Tamat SMA",
                    "Tidak Bekerja", "Bekerja Informal", "Bekerja Formal", "Bekerja Pertanian",
                    "Bekerja Bukan Pertanian", "Angka Melek Huruf",
                    "Angka Partsipasi Sekolah 7 - 12 tahun", "Angka Partsipasi Sekolah 13 - 15 tahun",
                    "Air Layak", "Jamban Sendiri/Bersama",
                    "Keluhan Kesehatan (Ya)", "Keluhan Kesehatan (Tidak)",
                    "Jamkes (Punya)", "Jamkes (Tidak Punya)"
                ])

            input_values = {
                "Jumlah Penduduk": jumlah_penduduk,
                "Penduduk Miskin": penduduk_miskin,
                "Persentase Penduduk Miskin": persentase_miskin,
                "Garis Kemiskinan": garis_kemiskinan,
                "Indeks Kedalaman Kemiskinan": kedalaman,
                "Indeks Keparahan Kemiskinan": keparahan,
                "Gini Ratio": gini,
                "Pendidikan Tamat <SD": t_smp,
                "Pendidikan Tamat SD/SMP": sd_smp,
                "Pendidikan Tamat SMA": sma,
                "Tidak Bekerja": tidak_bekerja,
                "Bekerja Informal": bekerja_informal,
                "Bekerja Formal": bekerja_formal,
                "Bekerja Pertanian": bekerja_pertanian,
                "Bekerja Bukan Pertanian": bekerja_nonpertanian,
                "Angka Melek Huruf": melek_huruf,
                "Angka Partsipasi Sekolah 7 - 12 tahun": aps_7_12,
                "Angka Partsipasi Sekolah 13 - 15 tahun": aps_13_15,
                "Air Layak": air_layak,
                "Jamban Sendiri/Bersama": jamban,
                "Keluhan Kesehatan (Ya)": keluhan_ya,
                "Keluhan Kesehatan (Tidak)": keluhan_tidak,
                "Jamkes (Punya)": jamkes_punya,
                "Jamkes (Tidak Punya)": jamkes_tidak
            }

            if tahun in df["Tahun"].values:
                st.warning(f"Data untuk tahun {tahun} sudah ada!")
            else:
                new_row = {col: 0 for col in df.columns}
                new_row["Tahun"] = tahun
                for col, val in input_values.items():
                    if val != 0:
                        new_row[col] = val
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.sort_values("Tahun", inplace=True)
                df.to_excel(file_path, index=False)
                st.success(f"Data untuk tahun {tahun} berhasil disimpan!")

with tab2:

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Penduduk Miskin</h4>
                <h2>{jumlah_miskin:,.0f} jiwa</h2>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Persentase Miskin</h4>
                <h2>{latest['Persentase Penduduk Miskin']:.2f}%</h2>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Indeks Kedalaman</h4>
                <h2>{latest['Indeks Kedalaman Kemiskinan']:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Indeks Keparahan</h4>
                <h2>{latest['Indeks Keparahan Kemiskinan']:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
            <div class="metric-card">
                <h4>Garis Kemiskinan</h4>
                <h2>Rp. {int(latest['Garis Kemiskinan']):,}</h2>
            </div>
        """, unsafe_allow_html=True)

    fig_combo = px.bar(df_kemiskinan, x="Tahun", y="Jumlah Penduduk", title="")
    fig_combo.add_scatter(x=df_kemiskinan["Tahun"], y=df_kemiskinan["Penduduk Miskin"],
                          mode="lines+markers", line=dict(color="red"))

    # FORECASTING
    ts = df_kemiskinan.set_index("Tahun")["Penduduk Miskin"]
    model = ARIMA(ts, order=(1,1,0)).fit()
    forecast = model.forecast(steps=5)
    future_years = [ts.index[-1] + i for i in range(1, 6)]

    fig_forecast = px.line(x=ts.index, y=ts.values, title="")
    fig_forecast.add_scatter(x=future_years, y=forecast.values,
                             mode="lines+markers", line=dict(dash="dash", color="red"))

    row2_col1, row2_col2 = st.columns([2, 1.2])

    with row2_col1:
        st.markdown('<div class="chart-card"><h3>Jumlah Penduduk vs Penduduk Miskin</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_combo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2_col2:
        st.markdown('<div class="chart-card"><h3>Forecasting Penduduk Miskin</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_forecast, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    tahun_selected = st.selectbox("Tahun", ["2020", "2021", "2022", "2023", "2024"])
    df_plot = df_kab[["Kabupaten/Kota Se Jawa Timur", tahun_selected]].copy()
    df_plot.rename(columns={"Kabupaten/Kota Se Jawa Timur": "Kabupaten",
                            tahun_selected: "Jumlah Penduduk Miskin"}, inplace=True)

    df_plot["Kabupaten"] = df_plot["Kabupaten"].str.replace("Kab.", "Kabupaten").str.strip()
    df_plot["Jumlah Penduduk Miskin"] = df_plot["Jumlah Penduduk Miskin"].astype(str).str.replace(",", "").astype(float) * 1000
    df_plot = df_plot[~df_plot["Kabupaten"].isin(["Jawa Timur"])]

    fig_map = px.choropleth_mapbox(
        df_plot, geojson=geojson, locations="Kabupaten", featureidkey="properties.name",
        color="Jumlah Penduduk Miskin", color_continuous_scale="Blues",
        center={"lat": -7.5, "lon": 113.7}, zoom=6.3
    )
    fig_map.update_layout(mapbox_style="white-bg", margin={"r": 0, "t": 30, "l": 0, "b": 0}, height=600)

    st.markdown('<div class="chart-card"><h3>Peta Jumlah Penduduk Miskin</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    # KORELASI
    df_subset = df.iloc[7:, 3:].drop(columns=[
        "Garis Kemiskinan", "Indeks Kedalaman Kemiskinan", "Indeks Keparahan Kemiskinan",
        "Jamban Sendiri/Bersama", "Air Layak",
        "Keluhan Kesehatan (Ya)", "Keluhan Kesehatan (Tidak)",
        "Jamkes (Punya)", "Jamkes (Tidak Punya)"
    ])

    corr_target = df_subset.corr()["Persentase Penduduk Miskin"].drop("Persentase Penduduk Miskin").sort_values(ascending=False)
    fig_corr = px.bar(x=corr_target.index, y=corr_target.values,
                      color=corr_target.values, color_continuous_scale="RdBu", title="")

    st.markdown('<div class="chart-card"><h3>Korelasi Variabel Sosial Ekonomi</h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    pendidikan_keywords = ["pendidikan tamat <sd", "pendidikan tamat sd/smp", "pendidikan tamat sma"]
    pend_cols = [c for c in df_lain.columns if any(k in c.lower() for k in pendidikan_keywords)]

    pekerjaan_keywords = ["tidak bekerja", "bekerja informal", "bekerja formal"]
    peker_cols = [c for c in df_lain.columns if any(k in c.lower() for k in pekerjaan_keywords)]

    fac_cols = [c for c in ["Air Layak", "Jamban Sendiri/Bersama"] if c in df_lain.columns]

    row3_col1, row3_col2, row3_col3 = st.columns(3)

    if pend_cols:
        fig1 = px.bar(df_lain, x="Tahun", y=pend_cols, barmode="group", title="")
        with row3_col1:
            st.markdown('<div class="chart-card"><h3>Pendidikan Penduduk</h3>', unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if peker_cols:
        fig2 = px.bar(df_lain, x="Tahun", y=peker_cols, barmode="group", title="")
        with row3_col2:
            st.markdown('<div class="chart-card"><h3>Pekerjaan Penduduk</h3>', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if fac_cols:
        fig3 = px.bar(df_lain, x="Tahun", y=fac_cols, barmode="group", title="")
        with row3_col3:
            st.markdown('<div class="chart-card"><h3>Akses Air & Jamban</h3>', unsafe_allow_html=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    health_cols_map = {"Keluhan Kesehatan (Ya)" : "Ya", "Keluhan Kesehatan (Tidak)" : "Tidak"}
    health_cols = [c for c in health_cols_map.keys() if c in df_lain.columns]
    
    jamkes_cols_map = {"Jamkes (Punya)" : "Punya" , "Jamkes (Tidak Punya)" : "Tidak Punya"}
    jamkes_cols = [c for c in jamkes_cols_map if c in df_lain.columns]

    row4_col1, row4_col2 = st.columns(2)

    # SELECTBOX TAHUN UNTUK KEDUA PIE CHART
    tahun_pie = st.selectbox(
        "Tahun",
        df_lain["Tahun"].unique(),
        key="pie_global"
    )

    row4_col1, row4_col2 = st.columns(2)

    # ------------------ PIE CHART KESEHATAN ------------------
    if health_cols:
        df_health = df_lain[df_lain["Tahun"] == tahun_pie]
        values = [float(df_health[c].values[0]) for c in health_cols]

        fig_health = px.pie(
            names=health_cols_map,
            values=values
        )

        with row4_col1:
            st.markdown('<div class="chart-card"><h3>Keluhan Kesehatan</h3>', unsafe_allow_html=True)
            st.plotly_chart(fig_health, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


    # ------------------ PIE CHART JAMKES ------------------
    if jamkes_cols:
        df_jamkes = df_lain[df_lain["Tahun"] == tahun_pie]
        values = [float(df_jamkes[c].values[0]) for c in jamkes_cols]

        fig_jamkes = px.pie(
            names=jamkes_cols_map,
            values=values
        )

        with row4_col2:
            st.markdown('<div class="chart-card"><h3>Kepemilikan Jamkes</h3>', unsafe_allow_html=True)
            st.plotly_chart(fig_jamkes, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
