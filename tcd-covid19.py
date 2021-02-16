import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
    Display COVID-19 data by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""


if __name__ == "__main__":

    source_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    data = pd.read_csv(source_url)

#    cols = ["cases_weekly", "deaths_weekly"]
    cols = ["deaths_weekly"]

    tcd = data.pivot_table(index="countriesAndTerritories", values=cols)

    print(tcd)

#    ax = tcd.plot.bar(ylim=(0,1000000),yticks=np.arange(0,10000,10000))
    ax = tcd.plot.bar()
    plt.show()