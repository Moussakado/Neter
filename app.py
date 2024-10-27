import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import json
import pandas as pd
from globe import create_globe  # Globe

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'], suppress_callback_exceptions=True) # App DASH

with open('index.html', 'r') as f:  # Fichier HTML
    index_string = f.read()
app.index_string = index_string

with open('data/countries_data.json', 'r', encoding='utf-8') as f: # Données Pays JSON
    countries_data = json.load(f)

df = pd.read_csv('data/world_disaster.csv') # Données Catastrophes CSV

fig = create_globe('white')  # Création du globe avec un fond blanc par défaut

# Palette de couleurs pour le mode light
light_theme = {
    'bg_color': '#F5F5F5',  # Fond clair
    'text_color': '#333333',  # Texte foncé
    'nav_bg_color': '#1976D2',  # Bleu pour la barre de navigation
    'tab_bg_color': '#1976D2',  # Bleu pour les onglets
    'secondary_bg_color': '#FFFFFF',  # Couleur secondaire pour le panneau
    'footer_bg_color': '#1976D2',  # Bleu pour le bandeau en bas
    'button_color': '#1976D2',  # Bleu pour les boutons
    'link_color': 'black'  # Couleur des liens
}

# Palette de couleurs pour le mode dark
dark_theme = {
    'bg_color': '#1F2937',  # Fond sombre
    'text_color': '#F9FAFB',  # Texte clair
    'nav_bg_color': '#374151',  # Fond sombre pour la barre de navigation
    'tab_bg_color': '#374151',  # Fond sombre pour les onglets
    'secondary_bg_color': '#4B5563',  # Couleur secondaire pour le panneau
    'footer_bg_color': '#374151',  # Fond sombre pour le bandeau en bas
    'button_color': '#1D4ED8',  # Bleu pour les boutons
    'link_color': '#1D4ED8'  # Couleur des liens en mode dark (bleu)
}

##### Mise en page

# Layout principal
app.layout = dbc.Container([
    dbc.Row([
        # Barre de navigation
        dbc.Col(html.Img(id='logo', src='/assets/logo_light.png', style={'width': '150px', 'height': 'auto'}), width='auto'),
        dbc.Col([  # Onglets
            dbc.Tabs(id='tabs', active_tab='modelisation'),
        ], width=True),
        dbc.Col([
            dbc.Switch(
                id='mode-switch',
                value=False,  # Light mode par défaut
                className='my-2',
                style={'float': 'right'},
                label=html.Div([
                    html.I(className="fas fa-sun", style={'color': '#FFD700', 'marginRight': '5px'}),
                    html.I(className="fas fa-moon", style={'color': '#FFF', 'marginLeft': '5px'})
                ]))], width='auto')
    ], align="center", className="mb-4", id='nav-bar'),

    # Contenu de l'onglet
    dbc.Row([
        dbc.Col(html.Div(id='tab-content'))
    ], id='main-content'),

    # Footer
    dbc.Row(dbc.Col(html.Div(id='footer-content')))
], fluid=True, id='app-container')

# Footer
def create_footer(theme):
    return dbc.Row(dbc.Col(html.Div([
        html.P("© Neter • Tous droits réservés", style={'display': 'inline', 'color': theme['text_color'], 'margin-right': '20px'})
    ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': theme['footer_bg_color'], 'borderRadius': '5px'})))

# Layout Modelisation
modelisation_layout = dbc.Row([
    # Panneau de contrôle
    dbc.Col([
        html.Div([
            # Fenêtre pour afficher le nom du pays sélectionné
            html.Div(id='selected-country', style={'margin': '10px 0', 'padding': '10px', 'border': '1px solid #ccc', 'borderRadius': '5px', 'minHeight': '30px'}),

            # Menu déroulant pour choisir la saison
            dcc.Dropdown(
                id='season-dropdown',
                options=[
                    {'label': 'Hiver', 'value': 'Winter'},
                    {'label': 'Printemps', 'value': 'Spring'},
                    {'label': 'Été', 'value': 'Summer'},
                    {'label': 'Automne', 'value': 'Autumn'}
                ],
                placeholder="Saison",
                style={'margin': '20px 10px', 'width': '200px', 'color': '#333333'}
            ),

            # Menu déroulant pour choisir le type de catastrophe
            dcc.Dropdown(
                id='disaster-type-dropdown',
                options=[
                    {'label': 'Séisme', 'value': 'Earthquake'},
                    {'label': 'Inondation', 'value': 'Flood'},
                    {'label': 'Tempête', 'value': 'Storm'},
                    {'label': 'Tsunami', 'value': 'Tsunami'},
                    {'label': 'Incendie de Forêt', 'value': 'Forest_fire'},
                    {'label': 'Éruption Volcanique', 'value': 'Volcanic_eruption'},
                    {'label': 'Glissement de Terrain', 'value': 'Landslide'},
                ],
                placeholder="Type de catastrophe",
                style={'margin': '20px 10px', 'width': '200px', 'color': '#333333'}
            ),

            # Menu déroulant pour choisir le type de catastrophe
            dcc.Dropdown(
                id='duration-dropdown',
                options=[
                    {'label': 'Court', 'value': 'Short'},
                    {'label': 'Moyen', 'value': 'Medium'},
                    {'label': 'Long', 'value': 'Long'},
                ],
                placeholder="Durée",
                style={'margin': '20px 10px', 'width': '200px', 'color': '#333333'}
            ),

            # Menu déroulant pour choisir l'intensité (échelle de 1 à 10)
            dcc.Dropdown(
                id='intensity-dropdown',
                options=[{'label': str(i), 'value': i} for i in range(1, 11)],
                placeholder="Intensité",
                style={'margin': '20px 10px', 'width': '200px', 'color': '#333333'}
            ),

            # Bouton de Modélisation
            html.Button('Lancer Modélisation', id='run-model-button', className='btn btn-primary', style={'margin': '20px 10px'})
        ], id='control-panel', style={'padding': '20px', 'borderRadius': '5px'}),
    ], width=2),

    # Globe interactif
    dbc.Col([
        dcc.Graph(id='globe-graph', figure=fig, config={'displayModeBar': False}, style={'height': '80vh', 'width': '100%'})
    ], width=7),

    # Panneau de résultats
    dbc.Col([
        html.Div(id='model-results-table', style={'margin': '20px 10px', 'padding': '10px', 'borderRadius': '5px', 'minHeight': '200px'})
    ], width=3),
])

# Layout Aide
aide_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Aide et support", id='help-title', style={'marginBottom': '20px'}),
            html.P("Bienvenue dans l'onglet d'aide. Ici, vous trouverez des informations utiles pour naviguer et utiliser l'application.", style={'marginBottom': '20px'}),

            # Guide de navigation
            html.H4("Guide de Navigation", style={'marginBottom': '25px'}),
            html.P("• Utilisez l'onglet Modélisation pour explorer les catastrophes par pays.", style={'marginBottom': '10px'}),
            html.P("• Passez du mode clair au mode sombre avec le bouton de bascule en haut à droite.", style={'marginBottom': '20px'}),

            # Guide de la modélisation
            html.H4("Guide d'Utilisation de la Modélisation", style={'marginBottom': '25px'}),
            html.P("1. Sélectionnez les critères de catastrophe à simuler : saison, type, durée, intensité.", style={'marginBottom': '10px'}),
            html.P("2. Cliquez sur le bouton 'Lancer Modélisation' pour obtenir des résultats.", style={'marginBottom': '10px'}),
            html.P("3. Consultez le tableau des probabilités pour comprendre les risques associés aux critères choisis.", style={'marginBottom': '20px'}),

            # Interprétation des résultats
            html.H4("Interprétation des Résultats", style={'marginBottom': '25px'}),
            html.P("• Le tableau de probabilités montre le risque de survenue selon le pays, la saison, etc.", style={'marginBottom': '10px'}),
            html.P("• Les estimations des morts et des dégâts sont basées sur des moyennes historiques.", style={'marginBottom': '20px'}),

            # FAQ
            html.H4("FAQ", style={'marginBottom': '25px'}),
            html.P("Q : Que faire si aucun résultat n'apparaît ?", style={'marginBottom': '10px'}),
            html.P("R : Vérifiez les filtres, car certains choix peuvent ne pas avoir de données disponibles.", style={'marginBottom': '20px'}),
            html.P("Q : Comment sont calculées les probabilités ?", style={'marginBottom': '10px'}),
            html.P("R : Les probabilités de survenue des catastrophes sont calculées en fonction de plusieurs filtres, comme le type de catastrophe, la saison, la durée, et l’intensité, à partir des données historiques disponibles. Ces probabilités ne représentent pas des prévisions mais bien des estimations basées sur des événements passés.", style={'marginBottom': '20px'}),    
            html.P("Q : Quelle est la précision des données sur les décès et les dégâts ?", style={'marginBottom': '10px'}),
            html.P("R : Les chiffres sur les décès et les dégâts sont des estimations moyennes issues de données historiques. Ils peuvent ne pas refléter les variations locales ou les circonstances particulières de chaque catastrophe.", style={'marginBottom': '20px'}),
            html.P("Q : D'où viennent les données ?", style={'marginBottom': '10px'}),
            html.P(["R : Les données utilisées pour cette application proviennent de la base de données internationale des catastrophes EM-DAT, accessible à l'adresse suivante : ",
            html.A("https://www.emdat.be/", href="https://www.emdat.be/", target="_blank", style={'color': '#333333', 'textDecoration': 'none'})
            ], style={'marginBottom': '20px'})
        ], width=12)
    ])
])

##### Callbacks

# Callback pour gérer les changements de thème et les onglets
@app.callback(
    [Output('app-container', 'style'),
     Output('nav-bar', 'style'),
     Output('tabs', 'children'),
     Output('main-content', 'style'),
     Output('logo', 'src'),
     Output('tab-content', 'children'),
     Output('footer-content', 'children'),
     Output('mode-switch', 'label')],
    [Input('mode-switch', 'value'),
     Input('tabs', 'active_tab')]
)
def update_theme(is_dark_mode, active_tab):
    theme = dark_theme if is_dark_mode else light_theme
    logo_src = '/assets/logo_dark.png' if is_dark_mode else '/assets/logo_light.png'

    # Couleurs des onglets actifs et non actifs
    tabs = [
        dbc.Tab(label='Modélisation des Catastrophes', tab_id='modelisation',
                tab_style={'backgroundColor': theme['tab_bg_color'], 'color': 'white'},
                label_style={'color': 'white' if active_tab != 'modelisation' else 'black'}),
        dbc.Tab(label='Aide', tab_id='aide',
                tab_style={'backgroundColor': theme['tab_bg_color'], 'color': 'white'},
                label_style={'color': 'white' if active_tab != 'aide' else 'black'})
    ]

    # Layout du contenu en fonction de l'onglet actif
    if active_tab == 'modelisation':
        content = modelisation_layout
    elif active_tab == 'aide':
        content = aide_layout
    else:
        content = html.Div("Sélectionnez un onglet")

    footer = create_footer(theme) # Bandeau de bas de page

    label = html.Div([
        html.I(className="fas fa-sun", style={'color': '#FFD700', 'marginRight': '5px'}) if not is_dark_mode else html.I(className="fas fa-moon", style={'color': '#FFF', 'marginLeft': '5px'})
    ])

    return [
        {'backgroundColor': theme['bg_color'], 'color': theme['text_color']},
        {'backgroundColor': theme['nav_bg_color'], 'color': theme['text_color'], 'padding': '10px 0'},
        tabs,
        {'backgroundColor': theme['bg_color'], 'color': theme['text_color']},
        logo_src,
        content,
        footer,
        label
    ]

# Callback pour mettre à jour le globe uniquement lorsque l’onglet "modélisation" est actif
@app.callback(
    Output('globe-graph', 'figure'),
    [Input('mode-switch', 'value')],
    [State('tabs', 'active_tab')]
)
def update_globe(is_dark_mode, active_tab):
    if active_tab == 'modelisation':
        globe_bg_color = '#1F2937' if is_dark_mode else '#F5F5F5'
        fig = create_globe(globe_bg_color)
        return fig
    return dash.no_update

# Callback pour afficher le nom du pays sélectionné
@app.callback(
    Output('selected-country', 'children'),
    Input('globe-graph', 'clickData')
)
def display_selected_country(clickData):
    if clickData:
        curve_number = clickData['points'][0]['curveNumber']
        point_number = clickData['points'][0]['pointNumber']
        if curve_number < len(countries_data) and point_number < len(countries_data):
            country_name = countries_data[curve_number]["name"]
            return country_name
    return

# Callback pour afficher les résultats de la modélisation
@app.callback(
    Output('model-results-table', 'children'),
    Input('run-model-button', 'n_clicks'),
    State('disaster-type-dropdown', 'value'),
    State('intensity-dropdown', 'value'),
    State('duration-dropdown', 'value'),
    State('season-dropdown', 'value')
)
def update_results(n_clicks, disaster_type, intensity, duration, season):
    if n_clicks:
        # Filtrer le DataFrame en fonction des options sélectionnées
        filtered_df = df
        if disaster_type:
            filtered_df = filtered_df[filtered_df['Disaster Type'] == disaster_type]
        if intensity:
            filtered_df = filtered_df[filtered_df['Intensity'] == intensity]
        if duration:
            filtered_df = filtered_df[filtered_df['Duration'] == duration]
        if season:
            filtered_df = filtered_df[filtered_df['Season'] == season]

        results = [] # Initialisation des résultats

        # Test si le DataFrame filtré est vide
        if filtered_df.empty:
            return html.Div("Aucun résultat trouvé.", style={'color': 'red'})

        # Probabilités en fonction des filtres
        total_lines = df.shape[0]
        prob_country = (filtered_df.shape[0] / total_lines) * 100 if filtered_df['Country'].nunique() > 0 else 0
        prob_season = (filtered_df[filtered_df['Season'] == season].shape[0] / 
                       df[df['Season'] == season].shape[0]) * 100 if season else 0
        prob_duration = (filtered_df[filtered_df['Duration'] == duration].shape[0] / 
                         df[df['Duration'] == duration].shape[0]) * 100 if duration else 0
        prob_intensity = (filtered_df[filtered_df['Intensity'] == intensity].shape[0] / 
                          df[df['Intensity'] == intensity].shape[0]) * 100 if intensity else 0

        # Moyenne des décès et des dommages
        avg_deaths = filtered_df['Total Deaths'].mean() if not filtered_df['Total Deaths'].isnull().all() else 0
        avg_damages = filtered_df['Total Damage (\'000 US$)'].mean() if not filtered_df['Total Damage (\'000 US$)'].isnull().all() else 0

        # Tableau des probabilités
        prob_table = dbc.Table(
            [
                html.Thead(html.Tr([html.Th("Probabilité de survenue de la catastrophe", colSpan=2)])),
                html.Tbody([
                    html.Tr([html.Td("Pays"), html.Td(f"{prob_country:.2f}%")]),
                    html.Tr([html.Td("Saison"), html.Td(f"{prob_season:.2f}%")]),
                    html.Tr([html.Td("Durée"), html.Td(f"{prob_duration:.2f}%")]),
                    html.Tr([html.Td("Intensité"), html.Td(f"{prob_intensity:.2f}%")]),
                ])
            ],
            bordered=True,
            hover=True,
            responsive=True,
            style={'margin-top': '10px'}
        )

        # Informations et estimations supplémentaires
        additional_info = html.Div([
            html.P(
                "* Il s'agit des différentes probabilités de survenue de la catastrophe sachant différents paramètres",
                style={'fontSize': 'small', 'fontStyle': 'italic', 'marginTop': '10px'}
            ),
            html.P(
                "** Si un paramètre n'est pas sélectionné, toutes les valeurs possibles de ce paramètre sont prises en compte.",
                style={'fontSize': 'small', 'fontStyle': 'italic'}
            )
        ])
        
        # Ajout des estimations finales
        final_estimations = [
            html.P(f"Estimation des morts totaux: {avg_deaths:.2f}"),
            html.P(f"Estimation des dégâts totaux: ${avg_damages:.2f}")
        ]

        # Ajouter le tout à la liste des résultats
        results.append(html.H3("Analyse des risques"))
        results.append(prob_table)
        results.append(additional_info)
        results.extend(final_estimations)

        return results

    return ""

if __name__ == '__main__':
    app.run_server(debug=False)