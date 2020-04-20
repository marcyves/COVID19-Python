import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
    Display COVID-19 Evolution by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""
def process(country):
    # Get French data
    df_country = df[df.countriesAndTerritories == 'France']

    # Retain only date, cases and deaths columns
    df_country = df_country[['dateRep', 'cases', 'deaths']]

    # Calculate cumulative cases & deaths
    df_country = df_country.sort_values('dateRep')
    df_country['cumCases'] = df_country.cases.cumsum()
    df_country['cumDeaths'] = df_country.deaths.cumsum()

    return df_country

def display(df):
    x = np.arange(len(df.dateRep))  # the label are dates
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots(figsize=(10,12))
    rects1 = ax.bar(x - width/3, df.cumCases, width, label='Cases')
    rects2 = ax.bar(x + width/3, df.cumDeaths, width, label='Deaths')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count')
    ax.set_title('Confirmed Cases and Deaths')
    ax.set_xticks(x)
    ax.set_xticklabels(df.dateRep)
    ax.legend()

    autolabel(ax,rects1)
    autolabel(ax,rects2)

    fig.tight_layout()

    plt.xticks(rotation=45)

    plt.show()

def autolabel(ax,rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

if __name__ == "__main__":
    df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv").dropna()
    display(process("France"))
