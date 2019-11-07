from github import Github
from textblob import TextBlob
import csv
import time


def check_ratelimit(remaining, resettime):
    """Checks if about to exceed ratelimit and pauses accordingly"""
    if remaining < 2:
        time.sleep(resettime - time.time())


def get_repo_entries(repo):
    """Goes through repo object and records entries for all issue and pull request comments"""

    for issue in repo.get_issues(state='all'):
        check_ratelimit(int(issue.raw_headers['x-ratelimit-remaining']), float(issue.raw_headers['x-ratelimit-reset']))
        print('ratelimit remaining: ' + str(issue.raw_headers['x-ratelimit-remaining']))
        for comment in issue.get_comments():
            check_ratelimit(int(comment.raw_headers['x-ratelimit-remaining']), float(comment.raw_headers['x-ratelimit-reset']))
            print('ratelimit remaining: ' + str(comment.raw_headers['x-ratelimit-remaining']))

            comment_blob = TextBlob(comment.body)
            entry = [repo.language, repo.name, issue.number, comment.id, comment_blob.sentiment.polarity,
                     comment_blob.sentiment.subjectivity]
            print(entry)
            with open('entries.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                writer.writerow(entry)


def main():
    g = Github('dkocen', 'n2T5%es%9s')
    languages = ['python', 'javascript', 'C', 'java', 'haskell']

    for language in languages:
        print(language)
        query = 'language:' + language
        repos = g.search_repositories(query=query)
        for repo in repos:
            get_repo_entries(repo)


if __name__ == '__main__':
    main()
