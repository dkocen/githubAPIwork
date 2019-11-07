from github import Github
from textblob import TextBlob


if __name__ == '__main__':
    g = Github('dkocen', 'n2T5%es%9s')
    repo = g.get_repo('thedaviddias/Front-End-Checklist') # Just some random test repo
    issues = repo.get_issues(state='all')
    for issue in issues:
        for comment in issue.get_comments():
            comment_blob = TextBlob(comment.body)
            entry = [repo.language, repo.name, issue.number, comment.id, comment_blob.sentiment.polarity,
                     comment_blob.sentiment.subjectivity]

            print(entry)