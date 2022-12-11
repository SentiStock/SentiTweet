import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html
from django_plotly_dash import DjangoDash
from stock.models import Company
from tweet.models import Tweet

df = Tweet.as_dataframe(Tweet.objects.filter(id=1598620724163248129))

def get_tweets(company, from_date_time=None, till_date_time=None):
    return Tweet.as_dataframe(company.get_tweets(
            from_date_time=from_date_time, 
            till_date_time=till_date_time
    ))

app = DjangoDash('comapny_detail')

app.layout = html.Div([
    dcc.Input(id='company_id', value='0', type='text', style=dict(display="none")),
    # html.Div(className="pcoded-main-container", children=[
    #     html.Div(className="pcoded-wrapper", children=[
    #         html.Div(className="pcoded-content", children=[
    #             html.Div(className="pcoded-inner-content", children=[
    #                 html.Div(className="main-body", children=[
    #                     html.Div(className="page-wrapper", children=[
    #                         html.Div(className="row", children=[
                                html.Div(className="col-md-4 col-xl-4", children=[
                                    html.Div(className='card', children=[
                                        html.Div(id='from_date_chooser_div'),
                                        html.Div(id='till_date_chooser_div'),
                                        html.Div(id='likes_slider'),
                                    ]),
                                ]),
                                html.Div(className="col-md-12 col-xl-12", children=[
                                    html.Div(className='card', children=[
                                        dcc.Graph(id='company_detail_graph'),
                                    ])
                                ]),
    #                         ]),
    #                     ]),
    #                 ]),
    #             ]),
    #         ]),
    #     ]),
    # ]),
], id='main')

@app.callback(
    Output('likes_slider', 'children'),
    Input('company_id', 'value'))
def update_slider(company_id):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=None, till_date_time=None)
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
    df = get_tweets(company, from_date_time=None, till_date_time=None)
    return dcc.Dropdown(
        id='from_date_chooser',
        options=[{'label': i, 'value': i} for i in df.post_date.dt.date.sort_values().unique()],
        value=df.post_date.dt.date.min(),
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
        value=df.post_date.dt.date.max(),
    )

@app.callback(
    Output('company_detail_graph', 'figure'), [
        Input('like_slider', 'value'),
        Input('company_id', 'value'),
        Input('from_date_chooser', 'value'),
        Input('till_date_chooser', 'value'),
    ])
def update_figure(min_likes, company_id, from_date_chooser, till_date_chooser):
    company = Company.objects.get(id=company_id)
    df = get_tweets(company, from_date_time=from_date_chooser, till_date_time=till_date_chooser)
    filtered_df = df[df.like_number >= min_likes]
    display_df = filtered_df.groupby([df['post_date'].dt.date]).count()
    fig = px.bar(
        display_df, y="id",
        title='Total number of Tweets on each day'
    )
    fig.update_layout(transition_duration=500)
    return fig


# @app.callback(
#     Output('company_id', 'value'),
#     Input('company_id', 'value'))
# def update_from_date_chooser(company_id):
#     company = Company.objects.get(id=company_id)
#     df = get_tweets(company, from_date_time=None, till_date_time=None)
#     return company_id