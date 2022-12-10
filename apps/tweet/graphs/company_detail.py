import dash
from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash

import pandas as pd
import plotly.express as px

from stock.models import Company
from tweet.models import Tweet

#_company_related_tweets
df = Tweet.as_dataframe(Company.objects.filter(symbol="AAPL").first().tweets.all())
app = DjangoDash('Comapny_detail')

app.layout = html.Div(
    [
    dcc.Graph(id='company-detail-graph'),
    dcc.Slider(
        df['like_number'].min(),
        df['like_number'].max(),
        step=None,
        value=df['like_number'].min(),
        #marks={str(year): str(year) for year in df['year'].unique()},
        id='like-slider'
    )
    ],
    style={'height': "20vh"}
)


@app.callback(
    Output('company-detail-graph', 'figure'),
    Input('like-slider', 'value'))
def update_figure(min_likes):
    filtered_df = df[df.like_number >= min_likes]
    display_df = filtered_df.groupby([df['post_date'].dt.date]).count()
    fig = px.bar(
        display_df, y="id",
        title='Total number of Tweets on each day')

    fig.update_layout(transition_duration=500)

    return fig