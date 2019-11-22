import pandas as pd
import re
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
    """Cleans data and runs sentiment analysis"""
    df = pd.read_csv('data_uncleaned200repos_50issues.csv', header=None,
                      names=['language', 'repo', 'issue_id', 'comment_id', 'comment_body'])

    # Runs basic text cleaning function using cleantext library
    df['comment_body'] = df['comment_body'].apply(lambda x: clean(x, no_line_breaks=True, no_urls=True,
                          no_emails=True, no_phone_numbers=True, replace_with_url=' ', replace_with_email=' ',
                          replace_with_phone_number=' '))

    # Run sentiment analysis
    analyser = SentimentIntensityAnalyzer()
    df['sentiment'] = [analyser.polarity_scores(str(comment))['compound'] for comment in df['comment_body']]


    #df = pd.read_csv('data_cleaned200repos_50issues.csv')
    # Load in additional repo info
    repo_info_df = pd.read_csv('repo_info.csv', header=None, names=['repo', 'url', 'created', 'subscribers', 'stars'])
    repo_info_df['repo'] = repo_info_df['repo'].apply(lambda x: re.sub(r'.*/', '', x)) # Clean up repo names to match df

    # Create dataframe that has sentiment means per repo
    repos_df = df.groupby(['repo'], as_index=False).apply(
        lambda x: pd.Series({
            'repo': x['repo'].iloc[0],
            'language': x['language'].iloc[0],
            'comment count': x['repo'].count(),
            'mean sentiment': x['sentiment'].mean()
        })
    )
    repos_df = repos_df.sort_values(by='repo')


    # Merge additional repo info df with repo means df
    entries = list()
    for repo in repos_df['repo']:
        entry = repo_info_df.loc[repo_info_df['repo'] == repo]
        entries.append([entry.iloc[0][2], entry.iloc[0][3], entry.iloc[0][4]])

    entries_df = pd.DataFrame(entries, columns=['creation_date', 'subscribers', 'stars'])
    repos_df = pd.concat([repos_df, entries_df], axis=1)

    repos_df.to_csv('data_cleaned200repos_alldata.csv')


if __name__ == '__main__':
    main()

