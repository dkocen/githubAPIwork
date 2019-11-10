from github import Github
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import time
import codecs


def check_ratelimit(remaining, resettime):
    """Checks if about to exceed ratelimit and pauses accordingly"""
    if remaining < 5:
        time.sleep(resettime - time.time())


def get_repo_entries(repo):
    """Goes through repo object and records entries for all issue and pull request comments"""
    # analyser = SentimentIntensityAnalyzer()
    for issue in repo.get_issues():
        check_ratelimit(int(issue.raw_headers['x-ratelimit-remaining']), float(issue.raw_headers['x-ratelimit-reset']))
        print('ratelimit remaining: ' + str(issue.raw_headers['x-ratelimit-remaining']))
        for comment in issue.get_comments():
            check_ratelimit(int(comment.raw_headers['x-ratelimit-remaining']), float(comment.raw_headers['x-ratelimit-reset']))
            print('ratelimit remaining: ' + str(comment.raw_headers['x-ratelimit-remaining']))
            # score = analyser.polarity_scores(comment.body)
            entry = [repo.language, repo.name, issue.number, comment.id, comment.body] # , score['compound']
            print(entry)
            with codecs.open('entries.csv', 'a', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                writer.writerow(entry)


def main():
    g = Github('dkocen', 'n2T5%es%9s')
    languages = ['python', 'javascript', 'C', 'java', 'haskell']

    for language in languages:
        print(language)
        query = 'language:' + language
        repos = g.search_repositories(query=query)
        print(f'Found {repos.totalCount} repos')

        for repo in repos[:100]:
            get_repo_entries(repo)


if __name__ == '__main__':
    main()
