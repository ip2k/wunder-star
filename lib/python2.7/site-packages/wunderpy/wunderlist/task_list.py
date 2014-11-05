'''Implements the TaskList class.'''


class TaskList(dict):
    '''Object representing a single task list in Wunderlist.'''

    def __init__(self, info, tasks=None, *args):
        '''
        :param tasks: A list of Task objects this list contains.
        :type tasks: list
        :param info: Information dict about the list returned by the API.
        :type info: dict
        '''

        if tasks:
            self.tasks = tasks
        else:
            self.tasks = []
        self.info = info
        dict.__init__(self, args)

    def __getitem__(self, key):
        return dict.__getitem__(self.info, key)

    def __setitem__(self, key, value):
        dict.__setitem__(self.info, key, value)

    def __repr__(self):
        return "<wunderpy.wunderlist.TaskList: {} {}>".format(self.title,
                                                              self.id)

    @property
    def title(self):
        '''The TaskList's title.'''
        return self.info.get("title")

    @property
    def id(self):
        '''The TaskList's ID.'''

        return self.info.get("id")

    def add_task(self, task):
        '''Add a Task to the list.'''
        self.tasks.append(task)

    def remove_task(self, task):
        '''Remove a Task from the TaskList.'''

        self.tasks.remove(task)

    def task_with_title(self, title):
        '''Return the most recently created Task with the given title.'''

        tasks = self.tasks_with_title(title)
        if len(tasks) >= 1:
            #return most recent task
            tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
            return tasks[0]
        else:
            return None

    def tasks_with_title(self, title):
        '''Find all Tasks with the given title.
        :param title: Title to match Tasks with.
        :type title: str
        '''
        return [task for task in self.tasks if task.title == title]

    def tasks_due_before(self, date):
        '''Find all Tasks that are due before date.'''

        return [task for task in self.tasks
                if task.due_date and task.due_date < date]

    def tasks_due_on(self, date):
        '''Find all Tasks that are due on date.'''

        return [task for task in self.tasks
                if task.due_date and task.due_date == date]

    def incomplete_tasks(self):
        '''Return all incomplete tasks.'''

        return [task for task in self.tasks if task.completed is not True]
