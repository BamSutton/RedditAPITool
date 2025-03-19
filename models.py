from datetime import datetime
from collections import defaultdict

class Comments:
    id: str
    redditor: str
    content: str
    score: int
    parent_id: str
    time_created: datetime

    def __init__(self, 
                 id: str, 
                 poster: str,
                 content: str, 
                 score: int, 
                 parent_id: str,
                 time_created: int):
        
        self.id = id
        self.poster = poster
        self.content = content
        self.score = score
        self.parent_id = parent_id
        self.time_created = datetime.fromtimestamp(time_created)

class Submissions:
    id: str
    title: str
    content: str
    poster: str
    score: int
    time_created: datetime
    commentList: list
    commentMap: defaultdict

    def __init__(self, id: str,
                  title: str, 
                  content: str,
                  poster: str,
                  score: int, 
                  time_created: int):
        
        self.id = id
        self.title = title
        self.content = content
        self.poster = poster
        self.score = score
        self.time_created = datetime.fromtimestamp(time_created)
        self.commentList = []
        self.commentMap = defaultdict(list)

class Subreddits:
    id: str
    name: str
    description: str
    time_created: datetime
    subscribers: int
    submissionList: list

    def __init__(self, 
                 id: str, 
                 name: str, 
                 description: str, 
                 time_created: int, 
                 subsrcibers: int):
        
        self.id = id
        self.name = name
        self.description = description
        self.time_created = datetime.fromtimestamp(time_created)
        self.subscribers = subsrcibers
        self.submissionList = []