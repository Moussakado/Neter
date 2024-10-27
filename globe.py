import plotly.graph_objects as go
import json

# Chargement des données JSON pour les pays
with open('data/countries_data.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

def create_globe(bg_color):
    fig = go.Figure()

    for country in countries_data:
        fig.add_trace(go.Scattergeo(
            lon=[country["lon"]],
            lat=[country["lat"]],
            mode='markers',
            marker=dict(size=3, color='red', opacity=0.7),
            text=country["name"],
            hoverinfo='text',
            name=country["name"],
            showlegend=False
        ))

    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        coastlinecolor="black",
        showland=True,
        landcolor="#61D32C",
        showocean=True,
        oceancolor="#1976D2",
        showlakes=True,
        lakecolor="#1976D2",
        showcountries=True,
        countrycolor="gray",
        bgcolor=bg_color,
        visible=False
    )

    fig.update_layout(
        showlegend=False,
        geo=dict(
            showframe=False,
            projection_type='orthographic',
            visible=False
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
    )

    return fig