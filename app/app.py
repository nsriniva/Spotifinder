import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.express as px
from dash.dependencies import Input, Output
from .data_model.find_songs import FindSongs

REC_COLS = ['artist','song']
FEATURES = ['name', 'artists']

get_song_info = lambda x:  ' '.join(x[FEATURES].to_list())

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
        placeholder = 'Song Name and/or Artist(s)',
        debounce=True
    ),
    html.Label("Songs:", style={'fontSize':30, 'textAlign':'left'}),
    dcc.Dropdown(id='Songs',
                 multi=False),
    html.Label("Recommendations:", style={'fontSize':30, 'textAlign':'left'}),
    dt.DataTable(
        id='rec-table',
        columns=[{"name": i.upper(), "id": i} for i in FEATURES],
        style_cell={'textAlign': 'center'},
        style_table={'minWidth': '360px','width': '360px','maxWidth': '360px'}
    )
])

@app.callback(
    Output('Songs', 'options'),
    Output('Songs', 'value'),
    [Input('Hint', 'value')]
)
def set_options(hint):
    if hint is None:
        hint = 'Fast Chapman'
    df = findSongs.find_song_entries(hint)
    best_idx = findSongs.get_best_choice(hint, df)
    dicosongs = [{'label': get_song_info(row), 'value': idx} for idx,row in df.iterrows()]
    return dicosongs, best_idx

@app.callback(
    Output('rec-table', 'data'),
    [Input('Songs', 'value')],
)
def predict(song):
    selected_song = findSongs.get_df_entry(song)

    result = findSongs.get_recommendations(selected_song)
    return result[FEATURES].to_dict('records')

    
if __name__ == '__main__':
    app.run_server(debug=True)
