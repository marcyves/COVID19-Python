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
    # Get Country data
    df_country = df[df.countriesAndTerritories == country]

    # Retain only date, cases and deaths columns
    df_country = df_country[['dateRep', 'cases', 'deaths']]

    # Make dateRep a Date field to sort it
    df_country['dateRep'] =pd.to_datetime(df_country.dateRep)
    df_country = df_country.sort_values('dateRep')
    # remove time
    df_country['dateRep'] = df_country['dateRep'].dt.date

    # Calculate cumulative cases & deaths
    df_country['cumCases'] = df_country.cases.cumsum()
    df_country['cumDeaths'] = df_country.deaths.cumsum()

    return df_country

def display(df, country):
    x = np.arange(len(df.dateRep))  # the label are dates
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots(figsize=(10,12))
    rects1 = ax.bar(x - width/3, df.cumCases, width, label='Cases')
    rects2 = ax.bar(x + width/3, df.cumDeaths, width, label='Deaths')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count')
    ax.set_title('Confirmed Cases and Deaths in {}'.format(country))
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


    print("Country Graphic Evolution")
    print("=========================\n")

    while True:
        print("1 - France")
        print("2 - Canada")
        print("3 - Italy")
        print("\n0 - Quitter\n")
        n = -1

        while(n<0 or n>3):
            n = int(input("Votre choix ==> "))

        if n == 0:
            break
        elif n == 1:
            country = "France"
        elif n == 2:
            country = "Canada"
        elif n == 3:
            country = "Italy"

        display(process(country), country)
