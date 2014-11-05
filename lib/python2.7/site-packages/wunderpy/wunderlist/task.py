'''Implements the Task class.'''


import dateutil.parser


class Task(dict):
    '''Object representing a single task in Wunderlist.'''

    def __init__(self, info, parent_list=None, subtasks=None, *args):
        '''
        :param info: The task information obtained from the API.
        :type info: dict
        :param parent_list: The TaskList this Task belongs to.
        :type parent_list: TaskList
        :param subtasks: A list of Task objects belonging to this TAsk.
        :type subtasks: list or None
        '''

        self.parent_list = parent_list
        self.info = info
        if subtasks:
            self.subtasks = subtasks
        else:
            self.subtasks = []
        dict.__init__(self, args)

    def __getitem__(self, key):
        return dict.__getitem__(self.info, key)

    def __setitem__(self, key, value):
        dict.__setitem__(self.info, key, value)

    def __repr__(self):
        return "<wunderpy.wunderlist.Task: {} {}>".format(self.title, self.id)

    @property
    def title(self):
        '''The Task's title.'''

        return self.info.get("title")

    @property
    def id(self):
        '''The Task's ID.'''

        return self.info.get("id")

    @property
    def created_at(self):
        '''Return a Datetime object for the moment the Task was created.'''

        created = self.info.get("created_at")
        if created:
            return dateutil.parser.parse(created)
        else:
            return None

    @property
    def due_date(self):
        '''Return a Date object with the date the Task is due, if any.'''

        due = self.info.get("due_date")
        if due:
            return dateutil.parser.parse(due).date()
        else:
            return None

    @property
    def due_date_iso(self):
        '''Return the due date as a sting in ISO format.'''

        return self.info.get("due_date")

    @property
    def completed(self):
        '''Return the Task's completion status'''
        if self.info.get("completed_at"):
            return True
        else:
            return False

    @property
    def starred(self):
        '''Is the Task starred?'''

        if self.info.get("starred") == 1:
            return True
        else:
            return False
