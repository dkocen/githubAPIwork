from github import Github
import csv
import time
import codecs

USERNAME = 'ENTER USERNAME'
PASSWORD = 'ENTER PASSWORD'

def check_ratelimit(remaining, resettime):
    """Checks if about to exceed ratelimit and pauses accordingly"""
    if remaining < 5:
        print(f'sleeping for {resettime-time.time()} ms')
        time.sleep(resettime - time.time())


def get_repo_entries(repo):
    """Goes through repo object and records entries for all issue and pull request comments"""
    issues = repo.get_issues(state='open')
    # Have an if statement instead of just splicing in for loop because may not have more than 20 issues
    if issues.totalCount > 50:
        issues = issues[:50]

    for issue in issues:
        check_ratelimit(int(issue.raw_headers['x-ratelimit-remaining']), float(issue.raw_headers['x-ratelimit-reset']))
        print('ratelimit remaining: ' + str(issue.raw_headers['x-ratelimit-remaining']))

        comments = issue.get_comments()
        # Have if statement instead of splicing in for loop because may not have more than 20 comments
        if comments.totalCount > 20:
            comments = comments[:20]

        for comment in comments:
            try:
                check_ratelimit(int(comment.raw_headers['x-ratelimit-remaining']), float(comment.raw_headers['x-ratelimit-reset']))
                print('ratelimit remaining: ' + str(comment.raw_headers['x-ratelimit-remaining']))
                entry = [repo.language, repo.name, issue.number, comment.id, comment.body] # , score['compound']
                print(entry)
                with codecs.open('data_uncleaned.csv', 'a', encoding='utf8') as csvfile:
                    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                    writer.writerow(entry)
            except:
                print('an error has occurred')


def main():
    g = Github(USERNAME, PASSWORD)
    languages = ['python', 'javascript', 'C', 'java', 'haskell']

    for language in languages:
        print(language)
        query = 'language:' + language
        repos = g.search_repositories(query=query)
        print(f'Found {repos.totalCount} repos')
        for repo in repos[:200]:
            check_ratelimit(int(repo.raw_headers['x-ratelimit-remaining']), float(repo.raw_headers['x-ratelimit-reset']))

            try:
                repo_info = [repo.full_name, repo.html_url, repo.created_at, repo.subscribers_count, repo.watchers]

                with codecs.open('repo_info.csv', 'a', encoding='utf8') as csvfile:
                    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                    writer.writerow(repo_info)

                get_repo_entries(repo)
            except:
                print('error occurred')


if __name__ == '__main__':
    main()
