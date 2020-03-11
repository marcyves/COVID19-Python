import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

today = date.today()

df = pd.read_html('https://www.worldometers.info/coronavirus/#countries')[0]
new_cols = df.columns.values
new_cols[0] = 'Countries'
df.columns = new_cols

top50 = df['TotalCases'] > 500
nototal = df['Countries'] != 'Total:'
nochina = df['Countries'] != 'China'

#  First Figure with China
x = np.arange(len(df[top50 & nototal].Countries))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots(figsize=(15,7))
rects1 = ax.bar(x - width/3, df[top50 & nototal].TotalCases, width, label='Cases')
rects2 = ax.bar(x + width/3, df[top50 & nototal].TotalDeaths, width, label='Deaths')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Count')
ax.set_title('Confirmed Cases and Deaths by Country')
ax.set_xticks(x)
ax.set_xticklabels(df[top50 & nototal].Countries)
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

# Second Figure Without China
x = np.arange(len(df[top50 & nototal & nochina].Countries))  # the label locations
width = 0.5  # the width of the bars

fig, ax = plt.subplots(figsize=(10,6))
rects1 = ax.bar(x - width/3, df[top50 & nototal & nochina].TotalCases, width, label='Cases')
rects2 = ax.bar(x + width/3, df[top50 & nototal & nochina].TotalDeaths, width, label='Deaths')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Count')
ax.set_title('Confirmed Cases and Deaths by Country\n{}'.format(today))
ax.set_xticks(x)
ax.set_xticklabels(df[top50 & nototal & nochina].Countries)
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


plt.xticks(rotation=45)

plt.show()