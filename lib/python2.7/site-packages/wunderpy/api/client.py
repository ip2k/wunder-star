'''Facilities for a client that only sends requests to the Wunderlist API'''


import json
import time

from requests import Session

from wunderpy.api.calls import batch, API_URL
from wunderpy.api.calls import login as login_call


def batch_format(request):
    '''Make a dict compatible with wunderlist's batch endpoint.'''

    request.url = request.url.replace(API_URL, "")

    op = {"method": request.method, "url": request.url,
          "params": request.data}
    return op


class APIClient(object):
    '''A class implementing all of the features needed to talk to Wunderlist'''
    def __init__(self):
        self.session = Session()
        self.token = None
        self.id = None
        self.headers = {"Content-Type": "application/json"}

    def login(self, email, password):
        '''Login to wunderlist'''

        r = self.send_request(login_call(email, password))
        self.set_token(r["token"])
        self.id = r["id"]

    def set_token(self, token):
        '''Set token manually to avoid having to login repeatedly'''
        self.token = token
        self.headers["Authorization"] = "Bearer {}".format(self.token)

    def send_request(self, request, timeout=30):
        '''Send a single request to Wunderlist in real time.

        :param request: A prepared Request object for the request.
        :type request_method: Request
        :param timeout: Timeout duration in seconds.
        :type timeout: int
        :returns: dict:
        '''

        request.headers = self.headers
        # Include the session headers in the request
        request.headers.update(self.session.headers)
        if request.data == []:
            request.data = json.dumps({})
        else:
            request.data = json.dumps(request.data)

        r = self.session.send(request.prepare(), timeout=timeout)

        if r.status_code < 300:
            return r.json()
        elif r.status_code == 404:  # dirty hack around this timing bullshit
            time.sleep(1)
            r2 = self.session.send(request.prepare(), timeout=timeout)
            if r2.status_code == 404:  # still doesn't work
                raise Exception(r2.status_code, r2)
            else:
                return r2.json()
        else:
            raise Exception(r.status_code, r)

    def send_requests(self, api_requests, timeout=30):
        '''Sends requests as a batch.

        Returns a generator which will yield the server response for each
        request in the order they were supplied.
        You must run next() on the result at least once.

        :param api_requests: a list of valid, prepared Request objects.
        :type api_requests: list -- Made up of requests.Request objects
        :yields: dict
        '''

        ops = [batch_format(req) for req in api_requests]

        batch_request = batch(ops)
        responses = self.send_request(batch_request)
        for response in responses["results"]:
            if response["status"] < 300:  # /batch is always 200
                yield response["body"]
            else:
                raise Exception(response["status"])
