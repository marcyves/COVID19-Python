import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""
    Display COVID-19 Evolution by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""


def display_bar(df, country, full, only):

    x = np.arange(len(df.dateRep))  # the label are dates
    width = 0.5  # the width of the bars

    if full:
        if only:
            rects1 = plt.bar(x - width/3, df.cumCases, width, label='Cas cumulés')
            autolabel(plt,rects1)
        rects2 = plt.bar(x + width/3, df.cumDeaths, width, label='Décés cumulés')
        autolabel(plt,rects2)
    if only:
        rects3 = plt.bar(x - width/3, df.cases, width, label='Cas')
        autolabel(plt,rects3)
    rects4 = plt.bar(x + width/3, df.deaths, width, label='Décés')
    autolabel(plt,rects4)

    # Add some text for custom x-axis tick labels.
    plt.xticks(x, df.dateRep)

def autolabel(ax,rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def display_scatter(df, country):

    x = df.dateRep

    plt.scatter(x, df.cumCases, c = 'blue')
    plt.scatter(x, df.cases, c = 'green')
    plt.scatter(x, df.cumDeaths, c = 'red')
    plt.scatter(x, df.deaths, c = 'orange')


def display_plot(df, country, full):

    x = df.dateRep

    y_ticks = np.arange(0, df.cumCases.max(), 1000)

    plt.yticks(y_ticks)
    
    if full:
        plt.plot(x, df.cumCases, c = 'blue', label='Cumulated Cases')
        plt.plot(x, df.cumDeaths, c = 'red', label='Cumulated Deaths')
    plt.plot(x, df.cases, ":",c = 'green', label='Cases')
    plt.plot(x, df.rollingCases, c = 'green', label='Rolling Mean of Cases')
    plt.plot(x, df.deaths, ":",c = 'orange', label='Deaths')
    plt.plot(x, df.rollingDeaths, c = 'orange', label='Rolling Mean of Cases')

    # draw line of Max Cases
#    x_cases = [df.date.min(), df.date.max()]
#    y_cases = [df.cases.max(), df.cases.max()]
#    plt.plot(x_cases, y_cases)

class SourceCovid():

    def __init__(self, url):

        self.df = pd.read_csv(url).dropna()
        self.url = url
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
        print("  3 - Histogramme des données journalières")
        print("  4 - Histogramme des données journalières et cumulées")
        print("  5 - Nuages de points")
        print("  6 - Histogramme des décés journaliers")

        n = 0
        while(n<1 or n>6):
            try:
                n = int(input("Votre choix ==> "))
            except:
                n = 1

        self.plot_type = n

    def DisplayGraph(self):
        
        plt.title('Confirmed Cases and Deaths in {}\nSource: {}'.format(self.country_selected, self.url))

        result = self.Process(self.country_selected)
        if self.plot_type == 1:
            display_plot(result, self.country_selected ,False)
        elif self.plot_type == 2:
            display_plot(result, self.country_selected ,True)
        elif self.plot_type == 3:
            display_bar(result, self.country_selected, False, True)
        elif self.plot_type == 4:
            display_bar(result, self.country_selected, True, True)
        elif self.plot_type == 5:
            display_scatter(result, self.country_selected)
        elif self.plot_type == 6:
            display_bar(result, self.country_selected, False, False)

        plt.xticks(rotation=80)
        plt.subplots_adjust(left=0.03, bottom=0.18, right=0.95, top=0.9)
        plt.grid(color='gainsboro', linestyle='dashed')
        plt.legend()
        plt.show()