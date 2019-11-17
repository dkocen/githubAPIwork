from bokeh.plotting import figure, output_file, show
import pandas as pd

def main():
    raw_data = pd.read_csv('data_cleaned_200repos_withSentiment.csv')
    repo_names = raw_data.repo.unique()
    repo_means = raw_data.groupby('repo', as_index=False)['sentiment'].mean().sort_values(by='sentiment')

    p = figure(x_range=repo_means.repo, plot_width=10000)
    p.vbar(x=repo_means.repo, top=repo_means.sentiment, width=0.9)
    output_file('test.html')
    show(p)


if __name__ == '__main__':
    main()