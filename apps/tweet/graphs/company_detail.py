import dash
from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash

import pandas as pd
import plotly.express as px

from stock.models import Company
from tweet.models import Tweet

#_company_related_tweets
companies = Company.as_dataframe(Company.objects.all())
app = DjangoDash('Comapny_detail')

app.layout = html.Div(
    [
    dcc.Graph(id='company-detail-graph'),
    dcc.Dropdown(
    companies['symbol'],
    'AAPL',
    id='comapny-symbol',
    ),
    dcc.Slider(
        0,
        50000,
        step=None,
        value=0,
        #marks={str(year): str(year) for year in df['year'].unique()},
        id='like-slider'
    )
    ],
    style={'height': "20vh"}
)


@app.callback(
    Output('company-detail-graph', 'figure'),
    Input('like-slider', 'value'),
    Input('comapny-symbol', 'value'))
def update_figure(min_likes, company_symbol):
    df = Tweet.as_dataframe(Company.objects.filter(symbol=company_symbol).first().tweets.all())
    filtered_df = df[df.like_number >= min_likes]
    display_df = filtered_df.groupby([df['post_date'].dt.date]).count()
    fig = px.bar(
        display_df, y="id",
        title='Total number of Tweets on each day')

    fig.update_layout(transition_duration=500)

    return fig