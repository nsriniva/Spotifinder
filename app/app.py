import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from .data_model.find_songs import FindSongData, getBestChoice

from requests import post
from os import getenv

if (FIND_SONGS_URL := getenv('FIND_SONGS_URL')) is None:
    FIND_SONGS_URL = 'http://ec2-18-117-181-89.us-east-2.compute.amazonaws.com/'
FIND_MATCHING_SONGS = FIND_SONGS_URL+'matching_songs'
GET_RECOMMENDED_SONGS = FIND_SONGS_URL+'recommended_songs'

extract_id_list = lambda x: [int(y) for y in x[1:-2].split(',')]

def find_matching_songs(hint):
    ret = post(FIND_MATCHING_SONGS, params={'hint':hint})
    return extract_id_list(ret.text)


def get_recommended_songs(selected_song):
    ret = post(GET_RECOMMENDED_SONGS,data=selected_song.to_json())
    return extract_id_list(ret.text)

REC_COLS = ['artist','song']
FEATURES = ['name', 'artists']
SPOTIFINDER = 'Spotifinder'

get_song_info = lambda x:  ' '.join(x[FEATURES].to_list())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

findSongData = FindSongData()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = SPOTIFINDER

app.layout = html.Div([
    html.H1(children="Spotifinder: Recommending Songs", style={'textAlign':'center'}),
    html.Div([
        html.H2(children="Specifying Song Choice", style={'textAlign':'center'}),        
        html.Div([
            html.Label("Song Name and/or Artist(s):", style={'fontSize':20, 'textAlign':'left'})
        ],
                 style={
                    'width':'10%',
                     'text-align':'left',
                     'display':'inline-block'
                 }
        ),
        html.Div([
            dcc.Input(
                id='Hint',
                type = 'text',
                placeholder = 'Song Name and/or Artist(s)',
                debounce=True
            )
        ],
                 style={
                    'width':'10%',
                     'text-align':'left',
                     'display':'inline-block'
                 }
                 
        ),
        html.Div([
            dcc.Dropdown(id='Songs',
                         multi=False)
        ],
                 style={
                     'width':'70%',
                     'vertical-align':'middle',
                     'display':'inline-block'
                 }
        ),
    ]),
   html.Div([
        html.H2("Recommendations", style={'textAlign':'center'}),
        dt.DataTable(
            id='rec-table',
            columns=[{"name": i.upper(), "id": i} for i in FEATURES],
            style_cell={'textAlign': 'center'},
            style_table={'minWidth': '360px','width': '360px','maxWidth': '360px', 'marginLeft':'auto', 'marginRight':'auto'}
        )
    ])
])

@app.callback(
    Output('Songs', 'options'),
    Output('Songs', 'value'),
    [Input('Hint', 'value')]
)
def set_options(hint):
    if hint is None:
        raise PreventUpdate
    entries = find_matching_songs(hint)
    df = findSongData.get_song_entries_data(entries, sorted=True)
    best_idx = getBestChoice(hint, df)
    dicosongs = [{'label': get_song_info(row), 'value': idx} for idx,row in df.iterrows()]
    return dicosongs, best_idx

@app.callback(
    Output('rec-table', 'data'),
    [Input('Songs', 'value')],
)
def predict(song):
    if song is None:
        raise PreventUpdate
    selected_song = findSongData.get_df_entry(song)
    entries = get_recommended_songs(selected_song)
    result = findSongData.get_song_entries_data(entries)

    return result[FEATURES].to_dict('records')

    
if __name__ == '__main__':
    app.run_server(debug=True)

