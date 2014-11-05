'''
.. module:: wunderlist
'''

import itertools

from wunderpy import api
from .task_list import TaskList
from .task import Task


class Wunderlist(api.APIClient):
    '''A basic Wunderlist client.'''

    def __init__(self, lists=None):
        api.APIClient.__init__(self)

        if lists:
            self.lists = lists
        else:
            self.lists = []

    def __repr__(self):
        "<wunderpy.Wunderlist: {}>".format(self.token)

    # login(self, email, password) is inherited from api.APIClient

    def update_lists(self):
        '''Populate the lists with all tasks.

        This must be run right after logging in,
        before doing any operations.
        '''

        # delete any currently stored lists
        self.lists = []

        tasks, lists = self.send_requests([api.calls.get_all_tasks(),
                                          api.calls.get_lists()])

        # make inbox list
        inbox_info = {"title": "inbox", "id": "inbox", "created_on": None,
                      "updated_on": None}
        inbox = TaskList(inbox_info)
        inbox_tasks = [Task(t, parent_list=inbox) for t in tasks
                       if t["list_id"] == "inbox"]
        inbox.tasks = inbox_tasks
        self.lists.append(inbox)

        for list_info in lists:
            new_list = TaskList(info=list_info)
            new_tasks = [Task(t, parent_list=new_list) for t in tasks
                         if t["list_id"] == list_info["id"]]
            new_list.tasks = new_tasks
            self.lists.append(new_list)

    def list_with_title(self, list_title):
        '''Return a TaskList with the given title.'''

        lists = self.lists_with_title(list_title)
        if len(lists) >= 1:
            return lists[0]
        else:
            return None

    def lists_with_title(self, list_title):
        '''Return all TaskLists with the given title.'''

        return [list for list in self.lists if list.title == list_title]

    def tasks_for_list(self, list_title):
        '''Get all tasks belonging to a list.'''

        return self.list_with_title(list_title).tasks

    def id_for_list(self, list_title):
        '''Return the ID for a list'''

        return self.list_with_title(list_title).id

    def get_task(self, task_title, list_title):
        '''Return a dict with all a task with the specified title
        in the specified list.
        '''

        _list = self.list_with_title(list_title)
        return _list.task_with_title(task_title)

    def id_for_task(self, task_title, list_title):
        '''Return the ID for a task in a list.'''

        _list = self.list_with_title(list_title)
        return _list.task_with_title(task_title)["id"]

    def tasks_due_before(self, date):
        '''Return a list of tasks due before date'''

        tasks = [l.tasks_due_before(date) for l in self.lists]
        tasks = itertools.chain.from_iterable(tasks)  # no flatten in python
        return list(tasks)

    def tasks_due_on(self, date):
        '''Return all Tasks due on the given date.'''

        tasks = [l.tasks_due_on(date) for l in self.lists]
        tasks = itertools.chain.from_iterable(tasks)
        return list(tasks)

    def add_task(self, title, list_title="inbox", note=None, due_date=None,
                 starred=False, **kwargs):
        '''Create a new task.

        :param title: The task's name.
        :type title: str
        :param list_title: The title of the list that the task will go in.
        :type list: str
        :param note: An additional note in the task.
        :type note: str or None
        :param due_date: The due date/time for the task in ISO format.
        :type due_date: str or None
        :param starred: If the task should be starred.
        :type starred: bool
        '''

        # for API compatibility til 0.3
        if "list" in kwargs:
            list_title = kwargs["list"]

        list_id = self.id_for_list(list_title)
        add_task = api.calls.add_task(title, list_id, due_date=due_date,
                                      starred=starred)
        result = self.send_request(add_task)

        # update internal state
        parent_list = self.list_with_title(list_title)
        new_task = Task(result, parent_list=parent_list)
        parent_list.add_task(new_task)

        if note:
            self.send_request(api.calls.set_note_for_task(note, result["id"]))

    def complete_task(self, task_title, list_title="inbox"):
        '''Complete a task with the given title in the given list.'''

        task_id = self.id_for_task(task_title, list_title)
        new_task = self.send_request(api.calls.complete_task(task_id))
        self.get_task(task_title, list_title).info = new_task

    def delete_task(self, task_title, list_title="inbox"):
        '''Delete a task'''

        task_id = self.id_for_task(task_title, list_title)
        self.send_request(api.calls.delete_task(task_id))

        task_to_remove = self.get_task(task_title, list_title)
        self.list_with_title(list_title).remove_task(task_to_remove)

    def add_list(self, list_title):
        '''Create a new list'''

        new = self.send_request(api.calls.add_list(list_title))
        new_list = TaskList(info=new)
        self.lists.append(new_list)

    def delete_list(self, list_title):
        '''Delete a list.'''

        self.send_request(api.calls.delete_list(self.id_for_list(list_title)))
        self.lists.remove(self.list_with_title(list_title))
