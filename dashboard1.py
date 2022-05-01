import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from numerize.numerize import numerize

# import dash_iconify
##################### Data preparation ##############################
movies = pd.read_csv("movies.csv")

movies.dropna(how='any', inplace=True)

##################### Average stats versus years (per genres) ##############################

agg_data = movies.groupby(['year', 'genre'])[['gross', 'score', 'votes']].mean()
agg_data.reset_index(inplace=True)
subset_agg_data = agg_data[
    (agg_data['genre'] == 'Action') | (agg_data['genre'] == 'Adventure') | (agg_data['genre'] == 'Family') | (
            agg_data['genre'] == 'Drama') | (agg_data['genre'] == 'Horror')]

######################################################################

##################### Most appearing actors ##############################

star_data = movies.groupby('star')['name'].count().sort_values(ascending=False)
star_data = pd.DataFrame(star_data)
star_data.rename({'name': 'count'}, inplace=True, axis=1)
star_data = star_data.head(10)
star_data = star_data.iloc[::-1]

##################### Movies search bar ##############################

list_of_movies = movies['name'].tolist()

######################################################################

#######################bans#########################################
max_gross = movies.loc[movies['gross'].idxmax()]['gross']
max_gross = numerize(max_gross)
max_gross_name = movies.loc[movies['gross'].idxmax()]['name']

max_rate = movies.loc[movies['score'].idxmax()]['score']
max_rate_name = movies.loc[movies['score'].idxmax()]['name']

max_vote = movies.loc[movies['votes'].idxmax()]['votes']
max_vote = numerize(max_vote)
max_vote_name = movies.loc[movies['votes'].idxmax()]['name']

max_runtime = movies.loc[movies['runtime'].idxmax()]['runtime']
max_runtime_name = movies.loc[movies['runtime'].idxmax()]['name']

################################################################
app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div(
    children=[
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    html.Div([html.H1("IMDB Movies")],
                             style={'textAlign': 'center', "color": "grey", 'font-family': 'Roboto',
                                    "border": {"width": "2px", "color": "white"}})]),
                dbc.Row([
                    dbc.Col([html.Div([
                        html.A([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div([html.Div([
                                        html.H2("{} \U0001F4B2".format(max_gross)),
                                    ], style={'textAlign': 'center', "color": "white", 'font-family': 'Roboto'}),

                                        html.Div([
                                            html.H4('Highest grossing movie'),
                                        ], style={'textAlign': 'center', "color": "white"}),
                                        html.Div([
                                            html.H5("{}".format(max_gross_name))
                                        ], style={'textAlign': 'center', "color": "white"})

                                    ])

                                ], style={'background-color': '#430d27'})
                                , style={"outline": "solid grey"}),
                        ], href='https://www.imdb.com/title/tt0499549/', style={"text-decoration": "none"})
                    ])

                    ], width=3),
                    dbc.Col([html.Div([
                        html.A([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div([
                                        html.H2("{} \U0001F31F".format(max_rate)),
                                    ], style={'textAlign': 'center', "color": "white"}),

                                    html.Div([
                                        html.H4("Highest rated movie "),
                                    ], style={'textAlign': 'center', "color": "white"}),
                                    html.Div([
                                        html.H5("{}".format(max_rate_name))
                                    ], style={'textAlign': 'center', "color": "white"})
                                ], style={'background-color': '#430d27'}),

                                style={"outline": "solid grey"}),
                        ], href='https://www.imdb.com/title/tt0111161/', style={"text-decoration": "none"})
                    ])

                    ], width=3),
                    dbc.Col([html.Div([
                        html.A([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div([
                                        html.H2("{} \U0001f37f".format(max_vote)),
                                    ], style={'textAlign': 'center', "color": "white"}),
                                    html.Div([
                                        html.H4("Most popular movie ")
                                    ], style={'textAlign': 'center', "color": "white"}),
                                    html.Div([
                                        html.H5("{}".format(max_vote_name))
                                    ], style={'textAlign': 'center', "color": "white"})

                                ], style={'background-color': '#430d27'}),
                                style={"outline": "solid grey"}),
                        ], href='https://www.imdb.com/title/tt0111161/', style={"text-decoration": "none"})
                    ])

                    ], width=3),
                    dbc.Col([html.Div([
                        html.A([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div([
                                        html.H2("{0:.3g} hrs ⌛".format(max_runtime / 60)),
                                    ], style={'textAlign': 'center', "color": "white"}),
                                    html.Div([html.H4("Longest movie")

                                              ], style={'textAlign': 'center', "color": "white"}),
                                    html.Div([
                                        html.H5("{}".format(max_runtime_name))
                                    ], style={'textAlign': 'center', "color": "white"})
                                ], style={'background-color': '#430d27'})
                                , style={"outline": "solid grey"}),
                        ], href='https://www.imdb.com/title/tt0107007/', style={"text-decoration": "none"})
                    ])

                    ], width=3),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([

                    dbc.Row([
                                        html.Div([html.Div([
                                        html.H5("genre or rating?"),
                                    ], style={'textAlign': 'left', "color": "white", 'font-family': 'Roboto'}),

                    ]),
                        ]),
                        dcc.Dropdown(
                            placeholder="Select metric ...",
                            id="dropdown_11",
                            options=['rating', 'genre'],
                            value="genre",
                            clearable=False,

                            style={
                                'color': 'black',
                                'background-color': 'grey'}
                        ),
                        dbc.Row([
                            html.Div([html.Div([
                                html.H5("select a metric..."),
                            ], style={'textAlign': 'left', "color": "white", 'font-family': 'Roboto'}),

                            ]),
                        ]),


                        dcc.Dropdown(
                            placeholder="Select y axis ...",
                            id="dropdown_1",
                            options=['gross', 'votes', 'score'],
                            value="gross",
                            clearable=False,
                            style={
                                'color': 'black',
                                'background-color': 'grey',
                                'border-color': 'white'}

                        ),
                        dcc.Graph(id="graph_1",),

                    ], width=4),
                    dbc.Col([

                    ]),
                    dbc.Col([
                        dbc.Row([
                            html.Div([html.Div([
                                html.H5("select a metric.."),
                            ], style={'textAlign': 'left', "color": "white", 'font-family': 'Open Sans'}),

                            ]),
                        ]),
                        dcc.Dropdown(
                            placeholder="Select x axis ...",
                            id="dropdown_2",
                            options=['gross', 'score', 'votes'],
                            value="score",
                            clearable=False,

                            style={
                                'color': 'black',
                                'background-color': 'grey'
                            }
                        ),
                        dcc.Graph(id="graph_2"),

                    ], width=7),
                    # dbc.Col([
                    #
                    # ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            [
                                html.A(id='mov_link', children=[

                                    dbc.CardImg(id='poster', bottom=True),
                                ])
                            ],

                            style={"width": "18rem"},
                        )

                    ], width=4),
                    dbc.Col([
                        dbc.Row([
                            html.Div([html.Div([
                                html.H5("select a movie.."),
                            ], style={'textAlign': 'center', "color": "white", 'font-family': 'Open Sans'}),

                            ]),
                        ]),

                        dcc.Dropdown(
                            # placeholder="Select a movie ...",
                            id="dropdown_3",
                            options=list_of_movies,
                            value="Nightcrawler",
                            clearable=False,
                            style={
                                'color': 'black',
                                'background-color': 'grey'}
                        ),
                        dash_table.DataTable(
                            id='datatable',
                            style_data={
                                'color': 'white',
                                'backgroundColor': '#430d27'
                            },
                            style_header={
                                'backgroundColor': '#430d27',
                                'color': 'white',
                            }, style_cell={'fontSize': 20, 'font-family': 'Montserrat','textAlign': 'center'},
                        )

                    ], width=8),
                ], align='center'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="graph_3", figure=px.bar(star_data, x='count', y=star_data.index, range_x=[15, 42],
                                                              title='Who are the most appearing actors?').update_layout(
                            template='plotly_dark',
                            plot_bgcolor='rgba(0, 0, 0, 0)',
                            paper_bgcolor='rgba(0, 0, 0, 0)', ).update_traces(marker_color='#4db6ac'))
                    ], width=4),
                    dbc.Col([
                        dcc.Graph(id="graph_4",
                                  figure=px.scatter(movies, x='runtime', y='budget', color='rating', hover_name='name',
                                                    size='votes', size_max=20,
                                                    title='Does longer movies cost more?').update_layout(
                                      template='plotly_dark',
                                      plot_bgcolor='rgba(0, 0, 0, 0)',
                                      paper_bgcolor='rgba(0, 0, 0, 0)', ))

                    ], width=8),
                ]),
            ]), color='dark'
        )
    ])





@app.callback(
    Output("graph_1", "figure"),
    Input("dropdown_11", "value"),
    Input('dropdown_1', 'value'))
def update_genre_bar_chart(category, stats):
    df_metric = movies.groupby(category)[[stats]].mean().sort_values(by=stats, ascending=False).reset_index()

    if stats == 'score':
        fig = px.bar(df_metric.head(), x=category, y=stats, range_y=[6, 7.5])
        fig.update_layout(title_text='Average {} per {}'.format(stats, category), title_x=0.5, template='plotly_dark',
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          paper_bgcolor='rgba(0, 0, 0, 0)', )
        fig.update_traces(marker_color='#4db6ac')
    else:
        fig = px.bar(df_metric.head(), x=category, y=stats)
        fig.update_layout(title_text='Average {} per {}'.format(stats, category), title_x=0.5, template='plotly_dark',
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          paper_bgcolor='rgba(0, 0, 0, 0)', )
        fig.update_traces(marker_color='#4db6ac')
    return fig


@app.callback(
    Output("graph_2", "figure"),
    Input("dropdown_2", "value"))
def update_movie_line_chart(y):
    df_metric = subset_agg_data
    fig = px.line(df_metric, x='year', y=y, color='genre')
    fig.update_layout(title_text='Average {} per genre'.format(y), title_x=0.5, template='plotly_dark',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      paper_bgcolor='rgba(0, 0, 0, 0)', )

    return fig


@app.callback(Output('datatable', 'data'),
              Input("dropdown_3", 'value')
              )
def update_datatable(y):
    df = movies[movies['name'] == y][['gross', 'score', 'star', 'year', 'rating']]
    df['gross'] = df['gross'].apply(lambda x: '${:,.2f}'.format(x))
    df = pd.DataFrame(data=df.values.T, columns=[y], index=df.columns)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Title'}, inplace=True)
    # print(df)
    return df.to_dict('rows')


@app.callback(Output('poster', 'src'),
              Input("dropdown_3", 'value'))
def get_poster(y):
    url = "https://online-movie-database.p.rapidapi.com/auto-complete"

    querystring = {"q": y}

    headers = {
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
        "X-RapidAPI-Key": "a59b4def57msh304c600c02af5e1p1a7430jsn91a23d349f34"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()['d'][0]['i']['imageUrl']


@app.callback(Output('mov_link', 'href'),
              Input("dropdown_3", 'value'))
def get_link(y):
    url = "https://online-movie-database.p.rapidapi.com/auto-complete"

    querystring = {"q": y}

    headers = {
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
        "X-RapidAPI-Key": "a59b4def57msh304c600c02af5e1p1a7430jsn91a23d349f34"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    movie_id = response.json()['d'][0]['id']

    return 'https://www.imdb.com/title/{}/'.format(movie_id)


app.run_server()
