import pandas as pd

candidates = {'bernie': 'Bernie Sanders', 'pete': 'Pete Buttigieg', 'harris': 'Kamala Harris',
              'warren': 'Elizabeth Warren', 'biden': 'Joe Biden'}

locations = {'detroit': 'Detroit', 'sf': 'San Francisco', 'miami': 'Miami', 'nyc': 'New York', 'houston': 'Houston',
             'seattle': 'Seattle'}

rows = []

for name in candidates.keys():
    for location in locations.keys():
        data = pd.read_csv('tweets_' + name + '_' + location + '.csv', header=None, index_col=0)

        data = data.iloc[:, [0, 3]]
        data.columns = ['Sentiment', 'Date']
       t'].value_counts())

        total_len = len(data)
        pos = round((dictionary[4]/total_len) * 100, 2)
        neg = round((dictionary[0]/total_len) * 100, 2)

  
        row = {'Name': candidates[name], 'Location': locations[location], 'POS': dictionary[4], 'NEG': dictionary[0],
               'Total': total_len, 'POS%': pos, 'NEG%': neg}
        print(row)
        rows.append(row)

df = pd.DataFrame(rows)
print(df)

print(df.groupby(by=['Location']).max())
id = df.groupby(by=['Location'])['Total'].idxmax()
df_max = df.loc[id,]
print(df_max)

