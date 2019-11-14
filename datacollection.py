from github import Github
import csv
import time
import codecs


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
            check_ratelimit(int(comment.raw_headers['x-ratelimit-remaining']), float(comment.raw_headers['x-ratelimit-reset']))
            print('ratelimit remaining: ' + str(comment.raw_headers['x-ratelimit-remaining']))
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

        for repo in repos[:500]:
            get_repo_entries(repo)


if __name__ == '__main__':
    main()
