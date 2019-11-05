from github import Github

g = Github()
repo = g.get_repo('dkocen/CS3012_dev_tasks')
print(repo.name)
commits = repo.get_commits()
for commit in commits:
    print(str(commit.commit.committer.date) + ": " + commit.commit.message)
