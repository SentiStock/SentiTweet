import os

from django.conf import settings
from sqlalchemy import create_engine

nasdaq_api = 'https://data.nasdaq.com/api/v3/datasets/WIKI/ORB.json?api_key=ytqghVKP6zuYXw8tLwxU'


def get_sql_engine():
    return create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=False)


def create_from_df(model, df, table=False, if_exists='append'):
    # Make sure all attributes are the same name as the columns # TODO improve
    # TODO it will give an error automatically if the columns are not the same
    # attribute_names = [f.name for f in model._meta.get_fields()]
    # print(attribute_names)
    # print(df.columns)

    # if not list(df.columns) == attribute_names:
    #     raise Exception(f'Column names are not corect, they should be: {attribute_names}')
    
    table = table if table else model._meta.db_table
    engine = get_sql_engine()
    df.to_sql(name=table, con=engine, if_exists=if_exists, index=False, chunksize=1000, method='multi')
