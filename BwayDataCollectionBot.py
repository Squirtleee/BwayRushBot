import praw


'''
Notes:
1. created_utc: gives unix timestamps, meaning the number of seconds since Jan 1 1970
'''


reddit=praw.Reddit(client_id='',
                  client_secret='', # wouldn't be a secret if I told you :) (same for id and password)
                  username='BwayRushBot',
                  password='',
                  user_agent='BwayBot1.0')


##########################
# some variables
post_limit=900
subreddit=reddit.subreddit('broadway')
##########################

########################## Update current shows (start)
# all lower case, since later codes convert all submissions to lower case
# use set to avoid duplicates
shows_on_the_look_out={}
shows_on_the_look_out["parade"]=set()
shows_on_the_look_out["some like it hot"]=set()
shows_on_the_look_out["slih"]=set()
shows_on_the_look_out["chicago"]=set()
shows_on_the_look_out["kimberly akimbo"]=set()
########################## Update current shows (end)



# look at titles
for post in subreddit.hot(limit=post_limit):
        filter=False
        title=post.title.lower()
        for show in shows_on_the_look_out:
          if show in title and (" rush " in title or " rushed " in title):
                if show=="some like it hot" or show=="slih":
                  shows_on_the_look_out["some like it hot"].add((post.created_utc,post.url))
                  shows_on_the_look_out["slih"].add((post.created_utc,post.url))
                else:
                  shows_on_the_look_out[show].add((post.created_utc,post.url))
                filter=True
        

# look at post content
for post in subreddit.hot(limit=post_limit):
    filter=False
    content=post.selftext.lower()
    for show in shows_on_the_look_out:
          if show in content and (" rush " in content or " rushed " in content):
                if show=="some like it hot" or show=="slih":
                  shows_on_the_look_out["some like it hot"].add((post.created_utc,post.url))
                  shows_on_the_look_out["slih"].add((post.created_utc,post.url))
                else:
                  shows_on_the_look_out[show].add((post.created_utc,post.url))
                filter=True
    


# look at comments
# we only add one comment link from each post for each show
for post in subreddit.hot(limit=post_limit):
    filter=False
    added_show=set()
    for comment in post.comments:
        if hasattr(comment,'body'):
          comment2=comment.body.lower()
          comment_starter="https://www.reddit.com/"
          if comment.permalink[0]=="/":
              comment_starter="https://www.reddit.com"
          for show in shows_on_the_look_out:
            if show in comment2 and (" rush " in comment2 or " rushed " in comment2) and show not in added_show:
                  if show=="some like it hot" or show=="slih":
                    shows_on_the_look_out["some like it hot"].add((comment.created_utc,comment_starter+comment.permalink))
                    shows_on_the_look_out["slih"].add((comment.created_utc,comment_starter+comment.permalink))
                    added_show.add("some like it hot")
                    added_show.add("slih")
                  else:
                    shows_on_the_look_out[show].add((comment.created_utc,comment_starter+comment.permalink))
                    added_show.add(show)
                  filter=True


# write and format the result to a file
f = open("RushData.txt", "w")
f.write("Current Broadway Show Rush Ticket Data\n")
f.write("This data collecting bot looks at the last "+str(post_limit)+" posts on the Broadway Sub\n")
f.write("\n")
for show in shows_on_the_look_out:
    if show=="slih":
        continue
    f.write(show.upper()+": \n")
    temp__for_sort=[]
    for link in shows_on_the_look_out[show]:
        temp__for_sort.append(link)
    temp__for_sort.sort(reverse=True) # so we have the most recent submission first
    for link in temp__for_sort:
        f.write(link[1]+"\n")
    f.write("\n")
    f.write("\n")
f.close()     
