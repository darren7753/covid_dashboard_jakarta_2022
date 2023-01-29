# Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import streamlit as st

# Settings
st. set_page_config(
    page_title="COVID-19 Dashboard",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
local_css("style.css")

# Main title
reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style,unsafe_allow_html=True)
reduce_header_height_style2 = """
    <style>
        div.block-container {padding-bottom:2rem;}
    </style>
"""
st.markdown(reduce_header_height_style2,unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>COVID-19 Dashboard for DKI Jakarta 2022</h1>",unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Made by <a href='https://www.linkedin.com/in/mathewdarren/'>Mathew Darren Kusuma</a></p>",
    unsafe_allow_html=True
)

# Data
df = pd.read_pickle("combined_data2.pkl")
covid_kecamatan = pd.read_excel("covid_kecamatan.xlsx")

with open("Kecamatan-DKI-Jakarta.json") as user_file:
    file_contents = user_file.read()
file_contents = json.loads(file_contents)

# Subtitle
st.write("")
st.markdown("<h5>Distribution of Cumulative Cases</h5>",unsafe_allow_html=True)

# Set columns
col1,col2 = st.columns([2,1])

# Jakarta map
with col1:
    map_options = st.selectbox(label="label",options=["Infected","Recovered","Deaths"],label_visibility="collapsed")
    if map_options == "Infected":
        value_color = "positif"
        map_color = "reds"
    elif map_options == "Recovered":
        value_color = "sembuh"
        map_color = "greens"
    else:
        value_color = "meninggal"
        map_color = "greys"

    fig = px.choropleth_mapbox(
        covid_kecamatan,
        geojson=file_contents,
        locations="id",
        color=value_color,
        mapbox_style="carto-positron",
        featureidkey="properties.id",
        center={"lat":-6.1753942 - 0.055,"lon":106.827183},
        color_continuous_scale=map_color,
        zoom=10,
        labels={"id":"ID",value_color:map_options},
        hover_name="nama_kecamatan",
        opacity=0.5
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},paper_bgcolor="rgba(0,0,0,0)")
    fig.update_geos(fitbounds="locations",visible=False)
    st.plotly_chart(fig,use_container_width=True)

# Table
with col2:
    col2_df = covid_kecamatan.copy()
    col2_df = col2_df.set_index("nama_kecamatan")[["positif","sembuh","meninggal"]]
    col2_df.columns = ["Infected","Recovered","Deaths"]

    st.info("Click on the header of each column to sort the data",icon="ℹ️")
    st.dataframe(
        col2_df.style.background_gradient(cmap="Reds",subset="Infected")\
            .background_gradient(cmap="Greens",subset="Recovered")\
                .background_gradient(cmap="Greys",subset="Deaths"),
        use_container_width=True,
        height=438
    )

# Subtitle
st.markdown("<h5>Number of Active Cases Graph</h5>",unsafe_allow_html=True)

# Set columns
col3,col4 = st.columns([2,1])

# Line chart
with col3:
    st.write("<style>div.row-widget.stRadio>div{flex-direction:row;}</style>",unsafe_allow_html=True)
    time_options = st.radio(label="label",options=["Day","Week","Month"],label_visibility="collapsed")
    if time_options == "Day":
        time_resample = "D"
    elif time_options == "Week":
        time_resample = "W"
    else:
        time_resample = "M"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].index,
        y=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].positif,
        mode="lines",
        line_color="#fa6b84",
        name="Infected",
        line=dict(width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].index,
        y=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].sembuh,
        mode="lines",
        line_color="#90EF90",
        name="Recovered",
        line=dict(width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].index,
        y=df.set_index("date").resample(time_resample).sum()[["positif","sembuh","meninggal"]].meninggal,
        mode="lines",
        line_color="black",
        name="Deaths",
        line=dict(width=3)
    ))
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#cdcdcd",
            gridwidth=0.1
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
        legend=dict(bgcolor="#1f364d")
    )
    fig.update_geos(fitbounds="locations",visible=False)
    st.plotly_chart(fig,use_container_width=True)
    st.info("The range slider allows you to adjust the time range of the data displayed in the line chart",icon="ℹ️")

# Donut chart
with col4:
    fig = go.Figure(go.Pie(
        labels=["Infected","Recovered","Deaths"],
        values=[df["positif"].sum(),df["sembuh"].sum(),df["meninggal"].sum()],
        hole=0.3,
        text=["Infected","Recovered","Deaths"],
        marker=dict(colors=["#fa6b84","#90EF90","lightgrey"])
    ))
    fig.update_traces(
        hoverinfo="label+percent+value"
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"r":0,"l":0,"b":0},
    )
    fig.update_geos(fitbounds="locations",visible=False)
    st.plotly_chart(fig,use_container_width=True)

# Disclaimer
st.write("")
st.markdown("<p>Disclaimer: This is a personal dashboard project that visualizes the COVID-19 cases in DKI Jakarta in 2022. All the data used in this project have been collected from <a href='https://riwayat-file-covid-19-dki-jakarta-jakartagis.hub.arcgis.com/'>here</a>. This dashboard is far from perfect and may be improved in the future. If you're interested, the codes used to create this dashboard are available on my <a href='https://github.com/darren7753/covid_dashboard_jakarta_2022'>GitHub repository</a> for you to check out and potentially build upon.</p>",unsafe_allow_html=True)