from datetime import datetime
from wunderpy import Wunderlist
from github import Github
import base64
import time

WL_USER = 'your-wunderlist-login'
WL_PASS = base64.b64decode('base64-of-your-wunderlist-password')
WL_LIST_NAME = 'Github Starred'  # name of list to add stars to. Must exist ahead of time.
GH_TOKEN = 'see https://github.com/settings/tokens/new'

# get wunderlist stuff
print ">>>>> WUNDER-STAR STARTED {} <<<<<".format(time.asctime( time.localtime(time.time()) ))
print "Getting list from Wunderlist..."
w = Wunderlist()
w.login(WL_USER, WL_PASS)
w.update_lists()
tasks = w.tasks_for_list(WL_LIST_NAME)

# get github stuff
print "Getting stars from GitHub (this may take a bit)"
gh = Github(login_or_token=GH_TOKEN)
me = gh.get_user()
repos = [repo for repo in me.get_starred()]

# get what projects are already in Wunderlist by splitting on :
print "Comparing stars to Wunderlist items..."
task_title_list = [task.title.split(':')[0].encode('ISO-8859-1', 'ignore') for task in w.tasks_for_list(WL_LIST_NAME)]
added = 0
skipped = 0
notes = 0
error = 0
for repo in repos:
    repo_name = repo.full_name.encode('ISO-8859-1', 'ignore')
    if repo_name in task_title_list:
        skipped +=1
        print "{} already in Wunderlist. Skipping...".format(repo_name)
    else:
        try:
            info = "{}: {} // {}".format(repo_name, repo.description.encode('ISO-8859-1', 'ignore'), repo.homepage.encode('ISO-8859-1', 'ignore'))
            w.add_task(title=info, list_title=WL_LIST_NAME, note=None, due_date=None, starred=False)
            added +=1
        except Exception as e:
            print "Couldn\'t add {} ... exception: {} ... will retry with description as a note....".format(repo_name, e)
	    try:
                info = "{}: [too long; see notes] // {}".format(repo_name, repo.homepage.encode('ISO-8859-1', 'ignore'))
		desc = repo.description.encode('ISO-8859-1', 'ignore')
                w.add_task(title=info, list_title=WL_LIST_NAME, note=desc, due_date=None, starred=False)
                added += 1
                notes += 1
            except Exception as e:
                print "Couldn\'t add {} ... exception: {} ... retry didn't work...skipping...".format(repo_name, e)
                error +=1
                pass

print "Done. Added {} ({} with description in notes)// skipped {} // {} errors".format(added, notes, skipped, error)
