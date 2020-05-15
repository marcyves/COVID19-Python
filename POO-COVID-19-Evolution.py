import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import SourceCovid as sc

"""
    Display COVID-19 Evolution by Country
    =====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""


if __name__ == "__main__":

    source_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    data = sc.SourceCovid(source_url)

    data.SortCountries()
 
    while True:
        print("\n\nCountry Graphic Evolution")
        print("=========================\n")

        if data.SelectCountryFromList():
            break

        data.SelectGraph()

        data.DisplayGraph()
