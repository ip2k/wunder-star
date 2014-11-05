'''Command line script for wunderpy.'''


import argparse
from datetime import date, timedelta

from wunderpy import Wunderlist
from .storage import get_token, setup
import wunderpy.cli.colors as colors
import wunderpy.cli.six as six


class WunderlistCLI(object):
    '''Handles basic tasks performed by the CLI app.'''

    def __init__(self):
        self.wunderlist = None
        self.get_wunderlist()

    def get_wunderlist(self):
        try:
            token = get_token()
        except IOError:  # first run
            setup()
            token = get_token()

        wunderlist = Wunderlist()
        wunderlist.set_token(token)
        wunderlist.update_lists()
        self.wunderlist = wunderlist

    def print_tasks(self, tasks, limit):
        '''
        :param tasks: A dict with key: TaskList, value: list of Tasks
        '''

        with colors.pretty_output(colors.BOLD, colors.UNDERSCORE) as out:
            for list_title, _tasks in six.iteritems(tasks):
                if len(_tasks) > 0:
                    out.write("\n" + list_title)

                    tasks_printed = 0
                    for task in _tasks:
                        if tasks_printed < limit:
                            pretty_print_task(task)
                            tasks_printed += 1

    def add(self, task_title, list_title):
        '''Add a task or create a list.
        If just --task is used, optionally with --list, add a task.
        If just --list is used, create an empty list.
        '''

        if task_title and list_title:  # adding a task to a list
            self.wunderlist.add_task(task_title, list_title=list_title)
        elif list_title != "inbox":  # creating a list
            self.wunderlist.add_list(list_title)

    def complete(self, task_title, list_title):
        '''Complete a task'''

        self.wunderlist.complete_task(task_title, list_title=list_title)

    def delete_task(self, task_title, list_title):
        '''Delete a task'''

        self.wunderlist.delete_task(task_title, list_title)

    def delete_list(self, list_title):
        '''Delete a list'''

        self.wunderlist.delete_list(list_title)

    def overview(self, limit, show_complete):
        '''Display a few tasks from each list.
        :param limit: Maximum number of tasks to display per list.
        :type limit: int
        :param show_complete: Disply completed tasks?
        :type show_complete: bool
        '''

        to_print = {}
        for task_list in self.wunderlist.lists:
            if show_complete:
                to_print[task_list.title] = task_list.tasks
            else:
                tasks = task_list.incomplete_tasks()
                to_print[task_list.title] = tasks

        self.print_tasks(to_print, limit)

    def today(self, limit, show_complete):
        '''Display tasks that are due or overdue today.
        :param limit: Maximum number of tasks to display per list.
        :type limit: int
        :param show_complete: Display completed tasks?
        :type show_complete: bool
        '''

        to_print = {}
        for task_list in self.wunderlist.lists:
            tasks = task_list.tasks_due_before(date.today() +
                                               timedelta(days=1))
            if show_complete:
                to_print[task_list.title] = tasks
            else:
                _tasks = [t for t in tasks if t.completed is not True]
                to_print[task_list.title] = _tasks

        self.print_tasks(to_print, limit)

    def week(self, limit, show_complete):
        '''Display tasks that are due or overdue this week.
        :param limit: Maximum number of tasks to display per list.
        :type limit: int
        :param show_complete: Display completed tasks?
        :type show_complete: bool
        '''

        to_print = {}
        for task_list in self.wunderlist.lists:
            tasks = task_list.tasks_due_before(date.today() +
                                               timedelta(days=6))
            if show_complete:
                to_print[task_list.title] = tasks
            else:
                _tasks = [t for t in tasks if t.completed is not True]
                to_print[task_list.title] = _tasks

        self.print_tasks(to_print, limit)

    def display(self, list_title, show_complete):
        '''Display all tasks in a list.
        :param list_title: Title of the list to display.
        :type list_title: str
        :param show_complete: Display completed tasks?
        :type show_complete: bool
        '''

        _list = self.wunderlist.list_with_title(list_title)
        to_print = {}

        if show_complete:
            to_print[_list.title] = _list.tasks
        else:
            _tasks = [t for t in _list.tasks if t.completed is not True]
            to_print[_list.title] = _tasks

        self.print_tasks(to_print, len(to_print[_list.title]))


def pretty_print_task(task):
    '''Take a Task object and format it like so:
    [ (check) ] title (star)
    '''

    if six.PY2:
        check_mark = u"\u2713".encode("utf-8")
        star = u"\u2605".encode("utf-8")
    elif six.PY3:
        check_mark = u"\u2713"
        star = u"\u2605"

    is_completed = check_mark  # in other words, True
    if not task.completed:
        is_completed = " "  # not completed, False

    use_star = star  # True
    if not task.starred:
        use_star = ""  # False

    if six.PY2:
        line = "[{}] {} {}".format(is_completed,
                                   task.title.encode("utf-8"),
                                   use_star)
    elif six.PY3:
        line = "[{}] {} {}".format(is_completed,
                                   task.title,
                                   use_star)
    print(line)


def main():
    '''Entry point'''

    parser = argparse.ArgumentParser(description="A Wunderlist CLI client.")

    parser.add_argument("-a", "--add", dest="add", action="store_true",
                        default=False, help="Add a task or list.")
    parser.add_argument("-c", "--complete", dest="complete",
                        action="store_true", default=False,
                        help="Complete a task.")
    parser.add_argument("-d", "--delete", dest="delete", action="store_true",
                        default=False, help="Delete a task or list.")
    parser.add_argument("-o", "--overview", dest="overview",
                        action="store_true", default=False,
                        help="Display an overview of your Wunderlist.")
    parser.add_argument("--week", dest="week", action="store_true",
                        default=False, help="Display all incomplete tasks"
                        "that are overdue or due in the next week.")
    parser.add_argument("--today", dest="today", action="store_true",
                        default=False, help="Display all incomplete tasks "
                        "that are overdue or due today.")
    parser.add_argument("--display", dest="display", action="store_true",
                        default=False, help="Display all items in a list "
                        "specified with --list.")
    parser.add_argument("--show-complete", dest="show_complete",
                        action="store_true", default=False,
                        help="Display complete tasks, "
                        "by default only incomplete are shown.")
    parser.add_argument("-n", "--num", dest="num_tasks", type=int, default=5,
                        help="Choose the number of tasks to display from "
                        "each list. [default 5]")
    parser.add_argument("-l", "--list", dest="list", default="inbox",
                        help="Used to specify a list, either for a task in a "
                        "certain list, or for a command that only operates "
                        "on lists. Default is inbox.")
    parser.add_argument("-t", "--task", dest="task",
                        help="Used to specify a task name.")
    args = parser.parse_args()

    cli = WunderlistCLI()

    if args.add:
        cli.add(args.task, args.list)
    elif args.complete:
        cli.complete(args.task, args.list)
    elif args.delete:
        if args.task:
            cli.delete_task(args.task, args.list)
        else:
            cli.delete_list(args.list)
    elif args.today:
        cli.today(args.num_tasks, args.show_complete)
    elif args.week:
        cli.week(args.num_tasks, args.show_complete)
    elif args.overview:
        cli.overview(args.num_tasks, args.show_complete)
    elif args.display:
        cli.display(args.list, args.show_complete)
    else:
        cli.overview(args.num_tasks, args.show_complete)
