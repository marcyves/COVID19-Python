import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
    Display COVID-19 Evolution by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""


def display_bar(df, country):
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

def display_scatter(df, country):

    plt.title('Confirmed Cases and Deaths in {}'.format(country))

    x = np.arange(len(df.dateRep))  # the label are dates

    plt.scatter(x, df.cumCases, c = 'blue')
    plt.scatter(x, df.cases, c = 'green')
    plt.scatter(x, df.cumDeaths, c = 'red')
    plt.scatter(x, df.deaths, c = 'orange')

    plt.legend()
    plt.show()

def display_plot(df, country, full):

    #    print(df)

    plt.title('Confirmed Cases and Deaths in {}\nSource: {}'.format(country, source_url))

    x = df.dateRep
    plt.xticks(rotation=80)

    y_ticks = np.arange(0, df.cumCases.max(), 5000)

    plt.yticks(y_ticks)
    
    if full:
        plt.plot(x, df.cumCases, c = 'blue', label='Cumulated Cases')
        plt.plot(x, df.cumDeaths, c = 'red', label='Cumulated Deaths')
    plt.plot(x, df.cases, c = 'green', label='Cases')
    plt.plot(x, df.rollingCases,":", c = 'green', label='Rolling Mean of Cases')
    plt.plot(x, df.deaths, c = 'orange', label='Deaths')
    plt.plot(x, df.rollingDeaths,":", c = 'orange', label='Rolling Mean of Cases')

    # draw line of Max Cases
#    x_cases = [df.date.min(), df.date.max()]
#    y_cases = [df.cases.max(), df.cases.max()]
#    plt.plot(x_cases, y_cases)

    plt.subplots_adjust(left=0.1, bottom=0.18, right=0.95, top=0.9)

    plt.legend()
    plt.grid(color='gainsboro', linestyle='dashed')

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

class SourceCovid():

    def __init__(self, url):

        self.df = pd.read_csv(url).dropna()
        self.country_selected = ""
        self.plot_type = 1

    def SortCountries(self):
        self.countries = self.df.countriesAndTerritories.unique()

    def SelectCountryFromList(self):
        i = 0
        for country in self.countries:
            i += 1
            print("{} - {}".format(i, country))

        n = -1
        while(n<0 or n>len(self.countries)):
            try:
                n = int(input("Votre choix ==> "))
            except:
                n = 0

        if n != 0:
            self.country_selected =  str(self.countries[n-1])
            print("\nNous allons afficher le graphe pour '{}'".format(self.country_selected))
            return False
        else:
            return True
        
    def Process(self, country):
        # Get Country data
        df_country = self.df[self.df.countriesAndTerritories == country]
        # Retain only date, cases and deaths columns
        # df_country = df_country[['dateRep', 'cases', 'deaths']]

        # Make dateRep a Date field to sort it
        df_country['date'] = pd.to_datetime(df_country.dateRep, format="%d/%m/%Y")
        df_country = df_country.sort_values('date')
        # remove time
        df_country['date'] = df_country['date'].dt.date

        # Calculate cumulative cases & deaths
        df_country['cumCases'] = df_country.cases.cumsum()
        df_country['cumDeaths'] = df_country.deaths.cumsum()

        # Remove early values
        if len(df_country) < 100:
            print("\nWARNING: Pas assez de cas pour {} ".format(country))
        else:
            df_country = df_country[df_country.cumCases > 1000]
    
        # Rolling mean
        df_country['rollingCases'] = df_country.cases.rolling(window=7,center=False).mean()
        df_country['rollingDeaths'] = df_country.deaths.rolling(window=7,center=False).mean()

        return df_country

    def SelectGraph(self):
        print("\n\nOn affiche les données cumulées ? ([n]/y)")


        print("Type de graphique")
        print(" [1] - Courbes des données journalières")
        print("  2 - Courbes des données journalières et cumulées")
        print("  3 - Histogramme")
        print("  4 - Nuages de points")

        n = 0
        while(n<1 or n>4):
            try:
                n = int(input("Votre choix ==> "))
            except:
                n = 1

        self.plot_type = n

    def DisplayGraph(self):
        
        result = self.Process(self.country_selected)
        if self.plot_type == 1:
            display_plot(result, self.country_selected ,False)
        elif self.plot_type == 2:
            display_plot(result, self.country_selected ,True)
        elif self.plot_type == 3:
            display_bar(result, self.country_selected)
        elif self.plot_type == 4:
            display_scatter(result, self.country_selected)


if __name__ == "__main__":

    source_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    data = SourceCovid(source_url)

    data.SortCountries()
 
    while True:
        print("\n\nCountry Graphic Evolution")
        print("=========================\n")

        if data.SelectCountryFromList():
            break

        data.SelectGraph()

        data.DisplayGraph()
