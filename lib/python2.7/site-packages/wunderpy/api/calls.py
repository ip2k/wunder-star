'''
.. module:: calls
'''

import datetime
from requests import Request


API_URL = "https://api.wunderlist.com"
COMMENTS_URL = "https://comments.wunderlist.com"


def batch(ops):
    '''Make a Request for a batch call.

    :param ops: a list of pre-formatted requests
    :returns: Request
    '''

    request_body = {"ops": ops, "sequential": True}
    return Request("POST", "{}/batch".format(API_URL), data=request_body)


def login(email, password):
    '''Login request, so we can get a token.

    :returns: Request
    '''

    return Request("POST", "{}/login".format(API_URL),
                   data={"email": email, "password": password})


def me():
    '''Request for /me, which returns user information.

    :returns: Request
    '''

    return Request("GET", "{}/me".format(API_URL))


def get_all_tasks():
    '''Get every task associated with the account.

    :returns: Request
    '''

    return Request("GET", "{}/me/tasks".format(API_URL))


def add_task(title, list_id, due_date=None, starred=False):
    '''Add a task to a list.

    :param title: The task name/title.
    :type title: str
    :param list_id: id of the list to put the task in.
    :type list_id: str
    :param due_date: Date the task will be due in ISO format
    :type due_date: str
    :param starred: Whether the task should be starred.
    :type starred: bool
    :returns: Request
    '''

    if starred:
        starred = 1
    else:
        starred = 0

    body = {"list_id": list_id, "title": title, "starred": starred}
    if due_date:
        body["due_date"] = due_date  # should be in ISO format

    return Request("POST", "{}/me/tasks".format(API_URL), data=body)


def complete_task(task_id, completed_at=None):
    '''Mark a task as completed.

    :param task_id: The ID of the task you are completing.
    :type task_id: str
    :param completed_at: The datetime it was completed at, in ISO format.
    :type completed_at: str
    '''

    if not completed_at:
        completed_at = datetime.datetime.now().isoformat()

    url = "{}/{}".format(API_URL, task_id)
    body = {"completed_at": completed_at, "position": 0}
    return Request("PUT", url, data=body)


def set_note_for_task(note, task_id):
    '''Set a task's note field.

    :param note: The note's contents.
    :type note: str
    :param task_id: The id of the task.
    :type task_id: str
    :returns: Request
    '''

    url = "{}/{}".format(API_URL, task_id)
    body = {"note": note}
    return Request("PUT", url, data=body)


def set_task_due_date(task_id, due_date, recurrence_count=1):
    '''Set a task's due date.

    :param task_id: The id of the task.
    :type task_id: str
    :param due_date: The new due date in ISO format.
    :type due_date: str
    :param recurrence_count: Not completely sure yet.
    :type recurrence_count: int
    :returns: Request
    '''

    url = "{}/{}".format(API_URL, task_id)
    body = {"due_date": due_date, "recurrence_count": recurrence_count}
    return Request("PUT", url, data=body)


def delete_task(task_id, deleted_at=None):
    '''Delete a task.

    :param task_id: The task's id.
    :type task_id: str
    :returns: Request
    '''

    if not deleted_at:
        deleted_at = datetime.datetime.now().isoformat()

    url = "{}/{}".format(API_URL, task_id)
    body = {"deleted_at": deleted_at}
    return Request("DELETE", url, data=body)


def get_lists():
    '''Get all of the task lists

    :returns: Request
    '''

    return Request("GET", "{}/me/lists".format(API_URL))


def add_list(list_name):
    '''Create a new task list.

    :param list_name: The name of the new list.
    :type list_name: str
    :returns: Request
    '''

    body = {"title": list_name}
    return Request("POST", "{}/me/lists".format(API_URL), data=body)


def delete_list(list_id):
    '''Delete a list and all of its contents.

    :param list_id: The id of the list to delete.
    :type list_id: str
    :returns: Request
    '''

    url = "{}/{}".format(API_URL, list_id)
    return Request("DELETE", url)


def get_comments(task_id):
    '''Get all comments from the specified task.

    :param task_id: The ID of the task.
    :type task_id: str
    '''

    url = "{}/tasks/{}/messages".format(COMMENTS_URL, task_id)
    return Request("GET", url)


def add_comment(title, task_id):
    '''Add a comment to a task. I'm not sure if this works with batch

    :param title: The comment name/title.
    :param task_id: The ID of the task you're commenting on.
    :type title: str
    :type task_id: str
    :returns: Request
    '''

    url = "{}/tasks/{}/messages".format(COMMENTS_URL, task_id)
    body = {"channel_id": task_id, "channel_type": "tasks",
            "text": title}
    return Request("POST", url, data=body)


def get_reminders():
    '''Get a list of all reminders.

    :returns: Request
    '''

    return Request("GET", "{}/me/reminders".format(API_URL))


def set_reminder_for_task(task_id, date):
    '''Add a reminder for a task.

    :param task_id: The id of the task.
    :type task_id: str
    :param date: The reminder date/time in ISO format.
    :type date: str
    :returns: Request
    '''

    body = {"task_id": task_id, "date": date}  # date is in ISO date format
    return Request("POST", "{}/me/reminders".format(API_URL), data=body)


def get_shares():
    '''Get a list of all things shared with you, I think...

    :returns: Request
    '''

    return Request("GET", "{}/me/shares".format(API_URL))


def get_services():
    '''Not sure.

    :returns: Request
    '''

    return Request("GET", "{}/me/services".format(API_URL))


def get_events():
    '''Not sure.

    :returns: Request
    '''

    return Request("GET", "{}/me/events".format(API_URL))


def get_settings():
    '''Get account settings.

    :returns: Request
    '''

    return Request("GET", "{}/me/settings".format(API_URL))


def get_friends():
    '''Get friends list.

    :returns: Request
    '''

    return Request("GET", "{}/me/friends".format(API_URL))


def get_quota():
    '''Get your account's quota.

    :returns: Request
    '''

    return Request("GET", "{}/me/quota".format(API_URL))
