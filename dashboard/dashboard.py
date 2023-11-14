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


def create_weekday_df(df):
    weekday_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_df


# membaca csv C:\Users\anas\Desktop\dataset\dashboard\hour.csv
all_df = pd.read_csv(".\hour.csv")

all_df.rename(columns={
    'dteday': 'dateday',
    'hr': 'hour',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

all_df['month'] = all_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

all_df['season'] = all_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
all_df['weekday'] = all_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})

datetime_column = ["dateday"]
all_df.sort_values(by="dateday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_column:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dateday"].min()
max_date = all_df["dateday"].max()

# side
with st.sidebar:
    st.image("https://www.freepik.com/free-vector/bicycle-logo-design-template_42061726.htm#query=bike%20logo&position=25&from_view=search&track=ais&uuid=3ced7b8a-2ba8-4fc2-8c9c-fa4d2e898398")

    # setting tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dateday"] >= str(start_date)) &
                 (all_df["dateday"] <= str(end_date))]


# menyiapkan dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_df = create_daily_casual_df(main_df)
registered_df = create_daily_registered_df(main_df)
season_df = create_season_df(main_df)
month_df = create_month_df(main_df)
year_df = create_year_df(main_df)
weekday_df = create_weekday_df(main_df)

# membuat dashboard
st.header('Bike Rent Dashboard')

# jumalah harin rent
st.subheader('Daily Rentals')

col1, col2, col3 = st.columns(3)

with col1:
    daily_casual = daily_casual_df['casual'].sum()
    st.metric('Total Casual User', value=daily_casual)

with col2:
    registered_rent = registered_df['registered'].sum()
    st.metric('Total Registered User', value=registered_rent)

with col3:
    total_rent = daily_rent_df['count'].sum()
    st.metric('Total User', value=total_rent)


# grafik bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(
    month_df.index,
    month_df['count'],
    marker='o',
    linewidth=3,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=25, rotation=45)

st.pyplot(fig)


# seasonly
st.subheader('Seasonly Rentals')
fig, ax = plt.subplots(figsize=(15, 8))

sns.barplot(
    x = 'season',
    y = 'registered',
    data= season_df,
    label= 'Registered',
    color= 'tab:blue',
    ax=ax
    )
sns.barplot(
    x = 'season',
    y = 'casual',
    data= season_df,
    label= 'Casual',
    color= 'tab:orange',
    ax=ax
    )

for index, row in season_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# mingguan
st.subheader('Daily Rentals')
fig, ax = plt.subplots(figsize=(10, 6))

colors=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

sns.barplot(
  x='weekday',
  y='count',
  data=weekday_df,
  palette=colors,
  ax=ax
  )

for index, row in enumerate(weekday_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_title('Number of Rents based on Weekday')
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)