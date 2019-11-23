# githubAPIwork
Repo for GitHub API assignments for TCD CSU3012 Software Engineering

## GitHub Access Assignment
For the first assignment I use PyGitHub to connect to the GitHub API and print out all the commit times and messages for one of my public repos (dkocen/CS3012_dev_tasks). The code for this can be found in `githubaccess.py`. 

For grading please look at commit number: `118c6a12cde15a00a41f8c77c65fc45f9c7e85db` in the master branch.

### Dependencies
- [PyGitHub](https://pypi.org/project/PyGithub/)

## Github Social Graph Assignment
For this assignment I created an interactive graph that looks at a number of different features of individual GitHub repos in order to answer questions about comment sentiment across repos.

For grading please look at the most recent commit in the master branch.
 
### Key Questions
The purpose of this visualization was initially to answer the question "which programming language has the friendliest userbase?" To answer this question sentiment analysis was run on active issue comments across 5 languages, 200 repos per language. Graphing language on the x-axis and mean sentiment on the y-axis will give some insight into which language has the most positive comments. Though positivity does not necessarily mean friendliness it seemed like a good proxy.

There are a number of other questions this visualization can help answer as well such as:
- How does the number of comments/stars/subscribers in a repo impact comment sentiment?
- How does the number of comments/stars/subscribers in a repo impact the number of comment/stars/subscribers?
- Do number of comments/stars/subscribers vary across language?

By allowing the user to select what piece of data is plotted, any combination of questions involving comment count, language, mean sentiment, stars, and subscribers could be asked.

### Dependencies
#### Required to run visualization
- [Bokeh](https://pypi.org/project/bokeh/)
- [Pandas](https://pypi.org/project/pandas/)

#### Required to run data collection and analysis
- [Clean-Text](https://pypi.org/project/clean-text/)
- [Pandas](https://pypi.org/project/pandas/)
- [PyGitHub](https://pypi.org/project/PyGithub/)
- [VADER-Sentiment-Analysis](https://github.com/cjhutto/vaderSentiment)

### Basic Usage
To run the visualization:
1. Install [Bokeh](https://pypi.org/project/bokeh/) and [Pandas](https://pypi.org/project/pandas/) 
1. Open terminal and navigate to the repo folder
2. Run `visualization.py` as a Bokeh server using the command `bokeh serve --show visualization.py`
3. Adjust x-axis, y-axis, color, and size variables as desired
4. Hover over any data point to get specific information about it

### Features
The visualization has the following features:
- Ability to compare several different variables including comment count, repo language, mean sentiment, stars count, and subscriber count
- Ability to adjust color and size of data points to provide additional information
- Ability to zoom in on specific segments of the graph
- Automatically updating hover information and legend based on the chosen graph parameters

### Data Collection Process
Data collection was performed in `datacollection.py` using the `PyGitHub` library. It works as follows:
1. Given a list of languages search for repositories on GitHub written in that language
2. For each repo found (200 per language due to time constraints):
	1. Gather basic data about that repo and record in `repo_info.csv`
	2. Record active issue comments in `data_uncleaned.csv`. Due to time constraints each repo was limited to 50 active issues and 20 comments per active issue resulting in a maximum of 1000 comments per repo. The largest comment count was 704.

Because GitHub has request ratelimits, ratelimit monitoring was used. After each request made the function `check_ratelimit` was run and if necessary caused the program to sleep until the ratelimit was reset. These calculations were done using information provided by the GitHub API in order to ensure the program slept for the minimum amount of time necessary.

Because the data collection process took a considerable amount of time, `datacollection.py` was run using an Amazon Web Services EC2 instance over a period of several days. This ensured any interruption to the internet on my laptop would not cause the script to crash.

### Data Analysis Process
Data analysis was performed in `analysis.py` using `Pandas`, `Clean-Text`, and `VADER-Sentiment-Analysis`. It works as follows:
1. Read in `data_uncleaned.csv` and turn into a Pandas dataframe
2. Run a cleaning function on each of the comments (more information on this function can be found [here](https://pypi.org/project/clean-text/)).
3. Run sentiment analysis on each comment using VADER sentiment analysis. Record the compound value in the dataframe
4. Group comments by repo resulting in a new dataframe with one entry per repo and the average sentiment across all comments in that repo
5. Read in `repo_info.csv` and turn into a Pandas dataframe
6. Add the additional information found in `repo_info.csv` to the main repo sentiment dataframe
7. Save this dataframe to `data_cleaned_sentiment.csv`

`Clean-Text` provides a nice premade text cleaning function that allows for the quick cleaning of often very chaotic text data. While this is a good first step additional cleaning would be nice to ensure more uniform data. Perhaps the most useful additional process would be detecting comment language as the sentiment analyser only works with English.

VADER-Sentiment-Analysis was used because it is specifically designed to work with sentiments expressed in social media. While GitHub is not typically treated as a social media platform, comments on repos are probably more in line with comments on social media than in other domains. Additional information about this analysis can be found in:
> Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

### Visualization Process

Visualization was performed in `visualization.py` using `Pandas` and `Bokeh`.

Most of the data for the visualization is found in `data_cleaned_sentiment.csv` and stored as a Bokeh ColumnDataSource object. However, when language is one of the axes a separate Pandas dataframe is used that groups repo information by language. Thus, mean sentiment is the mean sentiment across all the repos in that language and things like comment count are the total number across all repos in that language. This allows for questions such as which language has the most friendly userbase to be asked. This dataframe is made when `visualization.py` is ran.

Bokeh is a Python library that provides easy to use functions to create highly flexible and interactive plots. This library is particularly useful because it integrates well with Pandas and allows you to easily launch a visualization in a web server.

### Known Issues
- Cleaning textual data needs to be improved to provide more accurate sentiment analysis. This includes removing non-English comments and code snippets
- Due to time limitations only so much data could be collected and processed which may lead to skewed results
- Data analysis could probably be streamlined. For instance instead of having two separate dataframes and merging them, find a way to have all the necessary data readily available in `data_uncleaned.csv`
- Positive sentiment is used as a proxy for friendliness. This may be good enough but it is possible that there are better ways to measure friendliness in comments that I am unaware of






