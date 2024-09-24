import pandas as pd

candidates = {'bernie': 'Bernie Sanders', 'pete': 'Pete Buttigieg', 'harris': 'Kamala Harris',
              'warren': 'Elizabeth Warren', 'biden': 'Joe Biden'}

topics = {'economy': 'Economy', 'healthcare': 'Health Care', 'gun control': 'Gun Control', 'immigration': 'Immigration',
          'taxes': 'Taxes'}
rows = []

for name in candidates.keys():
    for topic in topics.keys():
        data = pd.read_csv('tweets_' + name + '_' + topic + '.csv', header=None, index_col=0)

        data = data.iloc[:, [0, 3]]
        data.columns = ['Sentiment', 'Date']
        print(data.head())
        dictionary = dict(data['Sentiment'].value_counts())
        total_len = len(data)
        pos = round((dictionary[4]/total_len) * 100, 2)
        neg = round((dictionary[0]/total_len) * 100, 2)

    
        row = {'Name': candidates[name], 'Topic': topics[topic], 'POS': dictionary[4], 'NEG': dictionary[0],
               'Total': total_len, 'POS%': pos, 'NEG%': neg}
     
        rows.append(row)

df = pd.DataFrame(rows)
print(df)
