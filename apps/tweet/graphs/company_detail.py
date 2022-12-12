import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django.conf import settings
from django.db.models import Avg, Count, Q, Sum
from django_plotly_dash import DjangoDash
from stock.models import Company
from stock.utils import get_cluster_context
from tweet.models import Tweet, TwitterUser

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
                dbc.Col([], md=6, lg=4, id='main_info'),
                dbc.Col([], md=6, lg=4, id='numbers'),
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
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(id='cluster_table')
                    ],
                ), width=12),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(id='users_table'),
                    ],
                ), md=12, lg=6),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardBody(id='tweets_table'),
                    ],
                ), md=12, lg=6),
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
    display_df = grouped_df.count()
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
    # df['sentiment_compound_normalized'] = df.apply(lambda x: x.sentiment_compound*x.like_number if x.sentiment_compound else 0, axis=1)
    grouped_df = group_by_date(df, graph_detail_chooser)
    display_df = grouped_df.count()
    display_df['sentiment_compound'] = grouped_df['sentiment_compound'].mean()
    # display_df['sentiment_compound_normalized'] = grouped_df['sentiment_compound_normalized'].mean()

    fig = px.line(
        display_df, y='sentiment_compound',# y=['sentiment_compound', 'sentiment_compound_normalized'],
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

@app.callback(
    Output('users_table', 'children'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_users_table(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    users = company.get_twitter_users(from_date_chooser, till_date_chooser)
    number_of_users = len(users) if len(users) < 5 else 5

    df = TwitterUser.as_dataframe(users)
    df['compound'] = [i.get_compound(from_date_chooser, till_date_chooser) for i in users]
    df['total_likes'] = [i.total_likes(from_date_chooser, till_date_chooser) for i in users]
    df['tweets_count'] = [i.tweets.count() for i in users]

    active_tabs = []
    df_tweets = df.sort_values(by='tweets_count', ascending=False)
    df_tweets = df_tweets.reset_index(drop=True)
    for i in range(number_of_users):
        user = df.loc[i,:]
        active_tabs.append(
            html.Tr([
                html.Td(
                    html.P(user.username)
                ),
                html.Td(html.H6(user.tweets_count, className='m-0')),
                html.Td(html.H6(user.total_likes, className='m-0')),
                html.Td(html.H6(user.compound, className='m-0')),
            ])
        )
    
    active = html.Div(dbc.Table(
        [
            html.Tr([
                html.Th('User'),
                html.Th('Tweets'),
                html.Th('Likes'),
                html.Th('Sentiment'),
            ]),
            html.Tbody(
                active_tabs
            ), 
        ], bordered=True, hover=True, responsive=True,
    ))

    like_tabs = []
    df_likes = df.sort_values(by='total_likes', ascending=False)
    df_likes = df_likes.reset_index(drop=True)
    for i in range(number_of_users):
        user = df_likes.loc[i,:]
        like_tabs.append(
            html.Tr([
                html.Td(
                    html.P(user.username)
                ),
                html.Td(html.H6(user.tweets_count, className='m-0')),
                html.Td(html.H6(user.total_likes, className='m-0')),
                html.Td(html.H6(user.compound, className='m-0')),
            ])
        )
    
    like = html.Div(dbc.Table(
        [
            html.Tr([
                html.Th('User'),
                html.Th('Tweets'),
                html.Th('Likes'),
                html.Th('Sentiment'),
            ]),
            html.Tbody(
                like_tabs
            ), 
        ], bordered=True, hover=True, responsive=True,
    ))
    
    positive_tabs = []
    df_positive = df.sort_values(by='compound', ascending=False)
    df_positive = df_positive.reset_index(drop=True)
    for i in range(number_of_users):
        user = df_positive.loc[i,:]
        positive_tabs.append(
            html.Tr([
                html.Td(
                    html.P(user.username)
                ),
                html.Td(html.H6(user.tweets_count, className='m-0')),
                html.Td(html.H6(user.total_likes, className='m-0')),
                html.Td(html.H6(user.compound, className='m-0')),
            ])
        )
    
    positive = html.Div(dbc.Table(
        [
            html.Tr([
                html.Th('User'),
                html.Th('Tweets'),
                html.Th('Likes'),
                html.Th('Sentiment'),
            ]),
            html.Tbody(
                positive_tabs
            ), 
        ], bordered=True, hover=True, responsive=True,
    ))

    negative_tabs = []
    df_negative = df.sort_values(by='compound', ascending=True)
    df_negative = df_negative.reset_index(drop=True)
    for i in range(number_of_users):
        user = df_negative.loc[i,:]
        negative_tabs.append(
            html.Tr([
                html.Td(
                    html.P(user.username)
                ),
                html.Td(html.H6(user.tweets_count, className='m-0')),
                html.Td(html.H6(user.total_likes, className='m-0')),
                html.Td(html.H6(user.compound, className='m-0')),
            ])
        )
    
    negative = html.Div(dbc.Table(
        [
            html.Tr([
                html.Th('User'),
                html.Th('Tweets'),
                html.Th('Likes'),
                html.Th('Sentiment'),
            ]),
            html.Tbody(
                negative_tabs
            ), 
        ], bordered=True, hover=True, responsive=True,
    ))

    return [
        html.H3('Most Interesting Users'),
        dbc.Tabs(
        [
            dbc.Tab(active, label='Tweets'),
            dbc.Tab(like, label='Likes'),
            dbc.Tab(positive, label='Positive'),
            dbc.Tab(negative, label='Negative'),
        ]
    )]

# @app.callback(
#     Output('tweets_table', 'children'), [
#         Input('like_slider', 'value'),
#         Input('company_id', 'value'),
#         Input('from_date_chooser', 'value'),
#         Input('till_date_chooser', 'value'),
#     ])
# def update_tweets_table(min_likes, company_id, from_date_chooser, till_date_chooser):
#     company = Company.objects.get(id=company_id)
#     tweets = company.get_tweets(from_date_chooser, till_date_chooser)
#     number_of_tweets = len(tweets) if len(tweets) < 5 else 5

#     df = Tweets.as_dataframe(tweets)
#     df['compound'] = [i.get_compound(from_date_chooser, till_date_chooser) for i in users]
#     df['total_likes'] = [i.total_likes(from_date_chooser, till_date_chooser) for i in users]
#     df['tweets_count'] = [i.tweets.count() for i in users]

#     active_tabs = []
#     df_tweets = df.sort_values(by='tweets_count', ascending=False)
#     df_tweets = df_tweets.reset_index(drop=True)
#     for i in range(number_of_users):
#         user = df.loc[i,:]
#         active_tabs.append(
#             html.Tr([
#                 html.Td(
#                     html.P(user.username)
#                 ),
#                 html.Td(html.H6(user.tweets_count, className='m-0')),
#                 html.Td(html.H6(user.total_likes, className='m-0')),
#                 html.Td(html.H6(user.compound, className='m-0')),
#             ])
#         )
    
#     active = html.Div(dbc.Table(
#         [
#             html.Tr([
#                 html.Th('User'),
#                 html.Th('Tweets'),
#                 html.Th('Likes'),
#                 html.Th('Sentiment'),
#             ]),
#             html.Tbody(
#                 active_tabs
#             ), 
#         ], bordered=True, hover=True, responsive=True,
#     ))

#     like_tabs = []
#     df_likes = df.sort_values(by='total_likes', ascending=False)
#     df_likes = df_likes.reset_index(drop=True)
#     for i in range(number_of_users):
#         user = df_likes.loc[i,:]
#         like_tabs.append(
#             html.Tr([
#                 html.Td(
#                     html.P(user.username)
#                 ),
#                 html.Td(html.H6(user.tweets_count, className='m-0')),
#                 html.Td(html.H6(user.total_likes, className='m-0')),
#                 html.Td(html.H6(user.compound, className='m-0')),
#             ])
#         )
    
#     like = html.Div(dbc.Table(
#         [
#             html.Tr([
#                 html.Th('User'),
#                 html.Th('Tweets'),
#                 html.Th('Likes'),
#                 html.Th('Sentiment'),
#             ]),
#             html.Tbody(
#                 like_tabs
#             ), 
#         ], bordered=True, hover=True, responsive=True,
#     ))
    
#     positive_tabs = []
#     df_positive = df.sort_values(by='compound', ascending=False)
#     df_positive = df_positive.reset_index(drop=True)
#     for i in range(number_of_users):
#         user = df_positive.loc[i,:]
#         positive_tabs.append(
#             html.Tr([
#                 html.Td(
#                     html.P(user.username)
#                 ),
#                 html.Td(html.H6(user.tweets_count, className='m-0')),
#                 html.Td(html.H6(user.total_likes, className='m-0')),
#                 html.Td(html.H6(user.compound, className='m-0')),
#             ])
#         )
    
#     positive = html.Div(dbc.Table(
#         [
#             html.Tr([
#                 html.Th('User'),
#                 html.Th('Tweets'),
#                 html.Th('Likes'),
#                 html.Th('Sentiment'),
#             ]),
#             html.Tbody(
#                 positive_tabs
#             ), 
#         ], bordered=True, hover=True, responsive=True,
#     ))

#     negative_tabs = []
#     df_negative = df.sort_values(by='compound', ascending=True)
#     df_negative = df_negative.reset_index(drop=True)
#     for i in range(number_of_users):
#         user = df_negative.loc[i,:]
#         negative_tabs.append(
#             html.Tr([
#                 html.Td(
#                     html.P(user.username)
#                 ),
#                 html.Td(html.H6(user.tweets_count, className='m-0')),
#                 html.Td(html.H6(user.total_likes, className='m-0')),
#                 html.Td(html.H6(user.compound, className='m-0')),
#             ])
#         )
    
#     negative = html.Div(dbc.Table(
#         [
#             html.Tr([
#                 html.Th('User'),
#                 html.Th('Tweets'),
#                 html.Th('Likes'),
#                 html.Th('Sentiment'),
#             ]),
#             html.Tbody(
#                 negative_tabs
#             ), 
#         ], bordered=True, hover=True, responsive=True,
#     ))

#     return dbc.Tabs(
#         [
#             dbc.Tab(active, label='Tweets'),
#             dbc.Tab(like, label='Likes'),
#             dbc.Tab(positive, label='Positive'),
#             dbc.Tab(negative, label='Negative'),
#         ]
#     )

@app.callback(
    Output('cluster_table', 'children'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_cluster_table(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    tweets = company.get_tweets(from_date_chooser, till_date_chooser)

    if len(tweets) < 50:
        return html.Div()

    clusters = list(get_cluster_context(tweets))

    cluster_elements = []
    for index, cluster in enumerate(clusters):
        p_text = ''.join(f'{word}' if index==0 else f' - {word}' for index, word in enumerate(cluster[0]))

        cluster_elements.append([
            html.H4('Top used words in this potential event'),
            html.Hr(),
            html.P(p_text),
            html.H4('Most representative tweets for this potential event'),
        ])

        for best_tweet in cluster[1]:
            cluster_elements[index].append(html.Hr())
            cluster_elements[index].append(html.P(best_tweet))#, className='m-0 text-c-green'))

    tabs = dbc.Tabs([])
    for index, cluster in enumerate(clusters):
        tabs.children.append(
            dbc.Tab(cluster_elements[index], label=f'Event {index}'),
        )

    return tabs

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