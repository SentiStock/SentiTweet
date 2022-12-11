import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django.conf import settings
from django_plotly_dash import DjangoDash
from stock.models import Company
from tweet.models import Tweet

df = Tweet.as_dataframe(Tweet.objects.filter(id=1598620724163248129))

def get_tweets(company, from_date_time=None, till_date_time=None):
    return Tweet.as_dataframe(company.get_tweets(
            from_date_time=from_date_time, 
            till_date_time=till_date_time
    ))

app = DjangoDash('comapny_detail', external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    f'{settings.ASSETS_ROOT}/fonts/fontawesome/css/fontawesome-all.min.css',
    f'{settings.ASSETS_ROOT}/plugins/animation/css/animate.min.css',
    f'{settings.ASSETS_ROOT}/css/style.css',
    f'{settings.ASSETS_ROOT}/css/dark.css',
    f'{settings.ASSETS_ROOT}/css/sentitweet.css',
])


app.layout = html.Div([
    dcc.Input(id='company_id', value='0', type='text', style=dict(display="none")),
    html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H2('Company Name'),
                                html.H4('Company Symbol'),
                                html.P('Market Cap'),
                                html.P('From till'),
                            ]
                        ),
                    ],
                ), md=6, lg=4, id='main_info'),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H2('Numbers'),
                                html.H4('Tweet#: '),
                                html.H4('Hashtag#: '),
                                html.H4('Twitter User#: '),
                                html.H4('Followers#: '),
                            ]
                        ),
                    ],
                ), md=6, lg=4, id='numbers'),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3('Filters', className='mb-4'),
                                html.H6('Date range'),
                                dbc.Row([
                                    dbc.Col(id='from_date_chooser_div', width=6),
                                    dbc.Col(id='till_date_chooser_div', width=6),
                                ]),
                                html.Div([
                                    html.H6('Number of likes'),
                                    html.Div(id='likes_slider'),
                                ], className='mt-4'),
                                html.Div([
                                    html.H6('Graph detail'),
                                    html.Div(dcc.Dropdown(
                                        id='graph_detail_chooser',
                                        options=[
                                            {'label': 'Daily', 'value': 'day'},
                                            {'label': 'Hourly', 'value': 'hour'},
                                            {'label': 'Munites', 'value': 'minute'},
                                            {'label': 'Seconds', 'value': 'second'},
                                        ],
                                        value='day',
                                    ), id='graph_detail_chooser_div'),
                                ], className='mt-4'),
                            ]
                        ),
                    ],
                ), md=6, lg=4),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(dcc.Graph(id='tweet_number_graph'))
                    ],
                ), width=12),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(dcc.Graph(id='sentiment_graph'))
                    ],
                ), width=12),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(dcc.Graph(id='tweet_sentiment_pie'))
                    ],
                ), md=6, lg=6),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(dcc.Graph(id='user_sentiment_pie'))
                    ],
                ), md=6, lg=6),
            ]
        ),
    ], className="page-wrapper")
], className="main-body")


@app.callback(
    Output('main_info', 'children'),[
        Input('company_id', 'value'),
        Input('like_slider', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_main_info(company_id, min_likes, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_chooser, till_date_chooser)
    df = df[df.like_number >= min_likes]
    return dbc.Card(dbc.CardBody([
        html.H2(company.name),
        html.H4(company.symbol),
        html.H6(f'{company.country}'),
        html.H6(f'Stock price: {company.stock_price}$'),
        html.H6(f'{df.post_date.dt.date.min()} - {df.post_date.dt.date.max()}'),
        html.H6(f'Sentiment: {company.get_compound(from_date_chooser, till_date_chooser)} --> {company.get_sentiment_label(from_date_chooser, till_date_chooser)}'),
    ]))

@app.callback(
    Output('numbers', 'children'), [
        Input('company_id', 'value'),
        Input('like_slider', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_numbers(company_id, min_likes, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    hashtags = company.get_hashtags(from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    twitter_users = company.get_twitter_users(from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    df = get_tweets(company, from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    df = df[df.like_number >= min_likes]
    return [dbc.Card(dbc.CardBody([
            html.H3('Numbers'),
            html.H6(f'Tweets: {len(df)}'),
            html.H6(f'Hashtags: {len(hashtags)}'),
            html.H6(f'Twitter Users: {len(twitter_users)}'),
            html.H6(f'Followers: {len(company.favorites)}'),
        ])),
            dbc.Card(dbc.CardBody([
                html.H6(f'Total Likes: {df.like_number.sum()}'),
                html.H6(f'Total Retweets: {df.retweet_number.sum()}'),
                html.H6(f'Total Comments: {df.comment_number.sum()}'),
        ])),
    ]

@app.callback(
    Output('likes_slider', 'children'), [
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_slider(company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    return dcc.Slider(
        df['like_number'].min(),
        df['like_number'].max(),
        step=None,
        value=df['like_number'].min(),
        id='like_slider'
    )

@app.callback(
    Output('from_date_chooser_div', 'children'),
    Input('company_id', 'value'))
def update_from_date_chooser(company_id):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company)
    return dcc.Dropdown(
        id='from_date_chooser',
        options=[{'label': i, 'value': i} for i in df.post_date.dt.date.sort_values().unique()],
        # value=df.post_date.dt.date.min(), # TODO default till 1 week ago??
        placeholder='Date From',
    )

@app.callback(
    Output('till_date_chooser_div', 'children'),
    Input('company_id', 'value'))
def update_till_date_chooser(company_id):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=None, till_date_time=None)
    return dcc.Dropdown(
        id='till_date_chooser',
        options=[{'label': i, 'value': i} for i in df.post_date.dt.date.sort_values().unique()],
        # value=df.post_date.dt.date.max(),
        placeholder='Date Till',
    )

@app.callback(
    Output('tweet_number_graph', 'figure'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_figure(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    filtered_df = df[df.like_number >= min_likes]
    grouped_df = filtered_df.groupby([df['post_date'].dt.date], sort=True)
    display_df = filtered_df.groupby([df['post_date'].dt.date], sort=True).count()
    display_df['likes'] = grouped_df['like_number'].sum()
    display_df['retweets'] = grouped_df['retweet_number'].sum()
    display_df['comments'] = grouped_df['comment_number'].sum()
    display_df['tweets'] = display_df['id']
    fig = px.line(
        display_df, y=['tweets', 'likes', 'retweets', 'comments'],
        title='Total number of Tweets on each day',
    )
    fig.update_layout(transition_duration=500, xaxis_title="Date", yaxis_title="Amount")
    return fig


@app.callback(
    Output('sentiment_graph', 'figure'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
        Input('graph_detail_chooser', 'value'),
    ])
def update_figure(min_likes, company_id, from_date_chooser, till_date_chooser, graph_detail_chooser):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    df = df[df.like_number >= min_likes]
    grouped_df = group_by_date(df, graph_detail_chooser)
    display_df = grouped_df['sentiment_compound'].mean()
    # display_df['sentiment_compound_normalized'] = grouped_df['sentiment_compound'] * grouped_df['like_number']
    # print(display_df)

    fig = px.line(
        display_df, y='sentiment_compound',
        title='Avarage sentiment per day',
    )
    fig.update_layout(transition_duration=500, xaxis_title="Date", yaxis_title="Sentiment Compound")
    return fig

@app.callback(
    Output('tweet_sentiment_pie', 'figure'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_tweet_sentiment_pie(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    tweets = company.get_tweets(from_date_chooser, till_date_chooser)
    df = pd.DataFrame([i.sentiment_label for i in tweets], columns=['label'])
    df['count'] = 1

    fig = px.pie(df, values='count', names='label', title='Tweet sentiment labels', hole=.2)
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('user_sentiment_pie', 'figure'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_user_sentiment_pie(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    users = company.get_twitter_users(from_date_chooser, till_date_chooser)
    df = pd.DataFrame([i.sentiment_label for i in users], columns=['label'])
    df['count'] = 1

    fig = px.pie(df, values='count', names='label', title='User sentiment labels', hole=.2)
    fig.update_layout(transition_duration=500)
    return fig

def group_by_date(df, graph_detail_chooser='day'):
    # TODO
    # df['post_date'] = df.post_date.values.astype(np.int64) // 10 ** 9
    if graph_detail_chooser == 'week':
        return df.groupby([df['post_date'].dt.week], sort=True)
    if graph_detail_chooser == 'day':
        return df.groupby([df['post_date'].dt.date], sort=True)
    if graph_detail_chooser == 'hour':
        return df.post_date.floor('H')
        return df.groupby(pd.Grouper(level='time', freq='H'), sort=True).median()
        # return df.groupby([df['post_date'].dt.day + ' ' + df['post_date'].dt.hour], sort=True)
    if graph_detail_chooser == 'minute':
        return df.groupby([df['post_date'].dt.second], sort=True)
    if graph_detail_chooser == 'second':
        return df.groupby([df['post_date'].dt.minute], sort=True)
    return df