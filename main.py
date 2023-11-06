import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


# menyiapkan daily
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# menyiapkan daily casual


def create_daily_casual_df(df):
    daily_casual_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_df

# menyiapkan registered


def create_daily_registered_df(df):
    daily_registered_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_df

# menyiapkan season


def create_season_df(df):
    season_df = df.groupby(by='season')[
        ['registered', 'casual']].sum().reset_index()
    return season_df

# menyiapkan monthly


def create_month_df(df):
    month_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_month = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    month_df = month_df.reindex(ordered_month, fill_value=0)
    return month_df

# menyiapkan year


def create_year_df(df):
    year_df = df.groupby(by='year').agg({
        'count': 'sum'
    }).reset_index()
    return year_df

# menyiapkan hour


def create_hour_df(df):
    hour_df = df.gorupby(by='hour').agg({
        'count': 'sum'
    }).reset_index()
    return hour_df


# membaca csv
all_df = pd.read_csv('Bike-dataset\hour.csv')


datetime_column = ["dteday"]
all_df.sort_values(by="dteday",inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_column:
    all_df[column] = pd.to_datetime(all_df[column])
    
min_date = all_df["datetime_column"].min()
max_date = all_df["datetime_column"].max()


with st.sidebar:
    st.image("https://github.com/anasshn/dataset/blob/1d40f5251f9ab012fce63c5f96270e8554be6b4a/88_bicycle_old.jpg")
    
    
