'''A Wunderlist API client for python.

.. moduleauthor:: bsmt
'''

import pkg_resources
__version__ = pkg_resources.require("wunderpy")[0].version

from wunderpy.wunderlist import Wunderlist
