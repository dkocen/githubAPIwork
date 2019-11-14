import pandas as pd
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect


def determine_lang(string):
    try:
        return detect(string)
    except:
        return 'error'


def main():
    """Cleans data and runs sentiment analysis"""
    df = pd.read_csv('data_uncleaned_200repos.csv', header=None,
                      names=['language', 'repo', 'issue_id', 'comment_id', 'comment_body'])

    # Removes all rows that don't have a comment in English (hopefully)
    df = df[df['comment_body'].apply(lambda x: determine_lang(x)) == 'en']

    # Runs basic text cleaning function using cleantext library
    df['comment_body'] = df['comment_body'].apply(lambda x: clean(x, no_line_breaks=True, no_urls=True,
                          no_emails=True, no_phone_numbers=True, replace_with_url=' ', replace_with_email=' ',
                          replace_with_phone_number=' '))

    analyser = SentimentIntensityAnalyzer()
    df['sentiment'] = [analyser.polarity_scores(str(comment))['compound'] for comment in df['comment_body']]

    df.to_csv('data_cleaned_200repos_withSentiment.csv')


if __name__ == '__main__':
    main()

