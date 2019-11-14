from bokeh.plotting import figure, output_file, show
import pandas as pd

raw_data = pd.read_csv('data_cleaned_200repos_withSentiment.csv')

means = raw_data.groupby('repo', as_index=False)['sentiment'].mean()


output_file('test.html')
p = figure(x_range=means['repo'], title='Average Sentiment across repos')
p.vbar(x=means['repo'], top=means['sentiment'], width=0.9)
show(p)