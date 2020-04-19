import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import requests

"""
    Display COVID-19 WorldWide Evolution
    ====================================

    (c) Marc Augier - XDM Consulting
    m.augier@me.com

"""

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:,}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

today = date.today()

# Pretend to be a browser
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
url = 'https://www.worldometers.info/coronavirus/#countries'

r = requests.get(url, headers=header)

df = pd.read_html(r.text)[0]
new_cols = df.columns.values
new_cols[0] = 'Countries'
df.columns = new_cols

top50 = df['TotalCases'] > 5000
low50 = df['TotalCases'] < 1000
nototal = df['Countries'] != 'Total:'
noworld = df['Countries'] != 'World'

x = np.arange(len(df[top50 & nototal & noworld].Countries))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots(figsize=(15,7))
rects1 = ax.bar(x - width/3, df[top50 & nototal & noworld].TotalCases, width, label='Cases')
rects2 = ax.bar(x + width/3, df[top50 & nototal & noworld].TotalDeaths, width, label='Deaths')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Count')
ax.set_title('Confirmed Cases and Deaths by Country')
ax.set_xticks(x)
ax.set_xticklabels(df[top50 & nototal & noworld].Countries)
ax.legend()


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.xticks(rotation=90)

plt.show()