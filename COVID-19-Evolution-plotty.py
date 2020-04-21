import pandas as pd
import numpy as np

import plotly.express as px

"""
    Display COVID-19 Evolution by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""

def display(df):

#    df = df.query("continentExp=='Europe'")
    fig = px.line(df, x="dateRep", y="deaths", color='countriesAndTerritories')
    fig.show()

    x = np.arange(len(df.dateRep))  # the label are dates


if __name__ == "__main__":
    df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv").dropna()

    # Make dateRep a Date field to sort it
    df['date'] =pd.to_datetime(df.dateRep)
    df['just_date'] = df['dateRep'].dt.date
    df = df.sort_values('date')

    # Calculate cumulative cases & deaths
    df['cumCases']  = df.cases.cumsum()
    df['cumDeaths'] = df.deaths.cumsum()

    df = df.query("countryterritoryCode=='ITA'")

    print(df)
    display(df)
