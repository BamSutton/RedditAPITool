import praw

def find_subreddits(reddit: praw.Reddit, search_terms: list[str]):
    print(f"pulling subreddit data from search terms: {search_terms}")
    unique_subreddits_set = set()
    private_count = 0
    
    for term in search_terms:
        findingSubreddits = reddit.subreddits.search(query=term, limit=None)
        for item in findingSubreddits:
            if item.subreddit_type != 'private' and item.display_name not in unique_subreddits_set: 
                unique_subreddits_set.add(item)
            else:
                private_count+=1        
    unique_subreddits_list = list(unique_subreddits_set)
    print(f"Total subreddits found: {len(unique_subreddits_list) + private_count}")
    print(f"Number of private subreddits found: {private_count}")
    print(f"Number of unique subreddits used for data pull: {len(unique_subreddits_list)}")
    return unique_subreddits_list