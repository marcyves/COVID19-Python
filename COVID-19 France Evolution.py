import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
    Display COVID-19 Evolution in France
    ====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""

df = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv").dropna()

# Get French data
df_fr = df[df.countriesAndTerritories == 'France']

# Retain only date, cases and deaths columns
df_fr = df_fr[['dateRep', 'cases', 'deaths']]
# Make dateRep a Date field to sort it
df_fr['date'] =pd.to_datetime(df_country.dateRep, format="%d/%m/%Y")
df_fr['just_date'] = df_fr['dateRep'].dt.date
df_fr = df_fr.sort_values('date')

# Calculate cumulative cases & deaths
df_fr['cumCases'] = df_fr.cases.cumsum()
df_fr['cumDeaths'] = df_fr.deaths.cumsum()

import numpy as np

x = np.arange(len(df_fr.dateRep))  # the label are dates
width = 0.5  # the width of the bars

fig, ax = plt.subplots(figsize=(10,12))
rects1 = ax.bar(x - width/3, df_fr.cumCases, width, label='Cases')
rects2 = ax.bar(x + width/3, df_fr.cumDeaths, width, label='Deaths')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Count')
ax.set_title('Confirmed Cases and Deaths')
ax.set_xticks(x)
ax.set_xticklabels(df_fr.dateRep)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.xticks(rotation=45)

plt.show()