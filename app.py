import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("🌍 Earthquake Dashboard: Magnitudes & Locations Over Time")

# Load your dataset
df = pd.read_csv("cleaned_file.csv")

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Drop invalid/missing values
df = df.dropna(subset=['date', 'mag', 'country', 'latitude', 'longitude', 'depth'])

# Extract year
df['Year'] = df['date'].dt.year

# Sidebar - Filters
st.sidebar.header("🧰 Filters")

# Year range
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Filter by year
df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# Country filter
countries = sorted(df_filtered['country'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", options=countries, default=countries)

# Apply country filter
df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

# Group by year
magnitude_by_year = df_filtered.groupby('Year')['mag'].sum().reset_index()
depth_by_year = df_filtered.groupby('Year')['depth'].sum().reset_index()

# Earthquakes per country
quake_counts = df_filtered['country'].value_counts().reset_index()
quake_counts.columns = ['country', 'Earthquake Count']

# --- Custom Colors ---
line_color = '#EF553B'
line_color2 = '#636EFA'
bar_colors = px.colors.sequential.Viridis

# --- Charts ---
# Line: Magnitude by Year
fig_mag = px.line(
    magnitude_by_year, x='Year', y='mag',
    title='Total Earthquake Magnitudes by Year',
    markers=True,
    line_shape='spline'
)
fig_mag.update_traces(line_color=line_color, marker=dict(size=7))
fig_mag.update_layout(template="plotly_white")

# Line: Depth by Year
fig_depth = px.line(
    depth_by_year, x='Year', y='depth',
    title='Total Earthquake Depth by Year',
    markers=True,
    line_shape='spline'
)
fig_depth.update_traces(line_color=line_color2, marker=dict(size=7))
fig_depth.update_layout(template="plotly_white")

# Bar Chart: Earthquakes per Country
fig_bar = px.bar(
    quake_counts, x='Earthquake Count', y='country',
    orientation='h',
    title='🌍 Number of Earthquakes per Country',
    color='country',
    color_continuous_scale=bar_colors,
    height=800
)
fig_bar.update_layout(
    yaxis=dict(categoryorder='total ascending'),
    template="plotly_white"
)

# Map: Depth
fig_map = px.scatter_geo(
    df_filtered,
    lat='latitude',
    lon='longitude',
    color='depth',
    hover_name='country',
    size='depth',
    title='Earthquake Locations by Depth',
    color_continuous_scale='Turbo',
    projection='natural earth'
)

# Map: Magnitude
fig_map2 = px.scatter_geo(
    df_filtered,
    lat='latitude',
    lon='longitude',
    color='mag',
    hover_name='country',
    size='mag',
    title='Earthquake Locations by Magnitude',
    color_continuous_scale='Turbo',
    projection='natural earth'
)
fig_animated = px.scatter_geo(
    df_filtered,
    lat='latitude',
    lon='longitude',
    color='mag',
    hover_name='country',
    size='mag',
    animation_frame='Year',
    title='📽️ Animated Earthquake Magnitudes Over Time',
    color_continuous_scale='Turbo',
    projection='natural earth'
)

# --- Layout with Tabs ---
tab1, tab2, tab3, tab4, tab5 , tab6 = st.tabs([
    "🌐 Map by Depth", "🌐 Map by Magnitude",
    "📈 Line Charts", "📊 Bar Chart",
    "📋 Data Table", "🎞️ Animated Map"
])

with tab1:
    st.subheader("🗺️ Earthquake Depth Map")
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.subheader("🗺️ Earthquake Magnitude Map")
    st.plotly_chart(fig_map2, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📉 Total Earthquake Magnitudes by Year")
        st.plotly_chart(fig_mag, use_container_width=True)
    with col2:
        st.subheader("📉 Total Earthquake Depth by Year")
        st.plotly_chart(fig_depth, use_container_width=True)

with tab4:
    st.subheader("📊 Earthquakes per Country")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab5:
    st.subheader("📋 Explore Earthquake Data")
    with st.expander("Click to view filtered data table"):
        st.dataframe(df_filtered.reset_index(drop=True))
        
with tab6:
    st.subheader("🎞️ Animated Earthquake Map by Magnitude")
    st.plotly_chart(fig_animated, use_container_width=True)
