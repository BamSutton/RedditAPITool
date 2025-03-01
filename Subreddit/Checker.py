import praw
import praw.exceptions

# this pulls all of the subreddits that match the search terms provided
# and the puts them into a List to iterate over as well as makes file of all the names
def check_subreddit(reddit: praw.Reddit, search_terms: list[str]):
    
    foundSet = set()
    writefile = open('founditems.txt', 'w')
    for item in search_terms:
        findingSubreddits = reddit.subreddits.search(query=item)
        for i in findingSubreddits:
            if i.subreddit_type != 'private':
                foundSet.add(i.display_name)
                writefile.write(f'{i.display_name}\n')
                
    writefile.flush
    writefile.close
    return foundSet