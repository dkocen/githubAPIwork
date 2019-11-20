import pandas as pd
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def main():
    """Cleans data and runs sentiment analysis"""
    # df = pd.read_csv('data_uncleaned200repos_50issues.csv', header=None,
    #                   names=['language', 'repo', 'issue_id', 'comment_id', 'comment_body'])
    #
    # # Runs basic text cleaning function using cleantext library
    # df['comment_body'] = df['comment_body'].apply(lambda x: clean(x, no_line_breaks=True, no_urls=True,
    #                       no_emails=True, no_phone_numbers=True, replace_with_url=' ', replace_with_email=' ',
    #                       replace_with_phone_number=' '))
    #
    # analyser = SentimentIntensityAnalyzer()
    # df['sentiment'] = [analyser.polarity_scores(str(comment))['compound'] for comment in df['comment_body']]
    #
    # df.to_csv('data_cleaned200repos_50issues.csv')

    df = pd.read_csv('data_cleaned200repos_50issues.csv')
    repo_info_df = pd.read_csv('repo_info.csv', header=None, names=['name', 'url', 'created', 'subscribers', 'watchers'])

    repos_df = df.groupby(['repo', 'language'], as_index=False)['sentiment'].mean()
    repos_df = repos_df.sort_values(by='sentiment')
    repos_df['repo'] = [repo[0:30] for repo in repos_df['repo']]
    additional_data = list()
    for repo in repos_df['repo']:
        entry = repo_info_df.loc[repo_info_df['name']]
        additional_data.append([entry['created'], entry['subscribers'], entry['watchers']])


if __name__ == '__main__':
    main()

