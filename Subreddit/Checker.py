import praw
import praw.exceptions

# this pulls all of the subreddits that match the search terms provided
# and the puts them into a List to iterate over as well as makes file of all the names
def check_subreddit(reddit: praw.Reddit, search_terms: list[str]):
    print(f"pulling subreddit data from search terms: {search_terms}")
    foundSet = set()
    count = 0
    writefile = open('founditems.txt', 'w')
    for term in search_terms:
        findingSubreddits = reddit.subreddits.search(query=term,limit = 1) # this searches for subreddits based on a search term
        for item in findingSubreddits:
            # This filters out private subreddits and subreddits that have already been collected
            if item.subreddit_type != 'private' and item.display_name not in foundSet: 
                foundSet.add(item.display_name)
                writefile.write(f'{item.display_name}\n')
            else:
                count+=1
    print(f"Total unique subreddist's pulled: {len(foundSet)}")            
    writefile.flush
    writefile.close
    return foundSet, count