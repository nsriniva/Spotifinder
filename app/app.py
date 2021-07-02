import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from .data_model.find_songs import FindSongs

REC_COLS = ['artist','song']
FEATURES = ['name', 'artists', 'popularity']

get_song_info = lambda x:  x[FEATURES].to_list()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

findSongs = FindSongs()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.Label("Spotifinder: Recommending Songs", style={'fontSize':40, 'textAlign':'left'}),
    html.Label("Song Name and/or Artist(s)", style={'fontSize':30, 'textAlign':'left'}),
    dcc.Input(
        id='Hint',
        type = 'text',
        placeholder = 'Song Name and/or Artist(s)'
    ),
    html.Label("Songs:", style={'fontSize':30, 'textAlign':'left'}),
    dcc.Dropdown(id='Songs',
                 multi=False),
    html.Label("Recommendations:", style={'fontSize':30, 'textAlign':'left'}),
    html.Div([
        html.Div(
            [html.Tr([html.Th(col) for col in REC_COLS])], id='rec-table', style={'width': '100%', 'height': '100%'}),
        dcc.Interval(id='interval_component',
                     interval=1000,
                     n_intervals=0
        )
    ],id='Recommendations')
])

@app.callback(
    Output('Songs', 'options'),
    Output('Songs', 'value'),
    [Input('Hint', 'value')]
)
def set_options(hint):
    df = findSongs.find_song_entries(hint)
    best_idx = findSongs.get_best_choice(hint, df)
    dicosongs = [{'label': get_song_info(row), 'value': idx} for idx,row in df.iterrows()]
    return dicosongs, best_idx

@app.callback(
    Output('rec-table', 'children'),
    [Input('Songs', 'value')],
)
def predict(song):
    selected_song = findSongs.get_df_entry(song)

    result = findSongs.get_recommendations(selected_song)
    rec_songs = {"artist": [], "song": []};
    for idx, row in result.iterrows():
        artist = row['artists']
        song = row['name']
        rec_songs['artist'].append(artist)
        rec_songs['song'].append(song)
    return html.Table(
            [html.Tr([
                html.Td(rec_songs[col][i]) for col in REC_COLS
            ]) for i in range(len(rec_songs))]
        ) 

if __name__ == '__main__':
    app.run_server(debug=True)
