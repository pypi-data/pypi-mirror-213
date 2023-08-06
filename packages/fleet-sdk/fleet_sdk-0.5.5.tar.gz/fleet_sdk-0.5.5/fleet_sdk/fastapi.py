import time
import json
import requests
import pkg_resources
from functools import wraps
from fastapi import Request, Response, FastAPI
import importlib
from fleet_sdk.base import BaseTracker
from fleet_sdk.adapters.fastapi_adapter import FastAPIAdapter
import os
import sys

# Add the parent directory of 'sdk' to the system path
sdk_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(sdk_dir)
if parent_dir not in sys.path:
  sys.path.insert(0, parent_dir)

class Tracker(BaseTracker):
  DEFAULT_HOST = 'middleware.usefleet.ai'
  DEFAULT_DEBUG = True

  def __init__(self, token, app, host=BaseTracker.DEFAULT_HOST, debug=BaseTracker.DEFAULT_DEBUG):
    """
        Initialize the Tracker with the provided token, host, and debug flag.
    """
    super().__init__(token, app, host, debug)
    self.adapter = FastAPIAdapter()

  def log_event(self, func):
    """
    Decorator function for logging events. This function wraps around the endpoint functions,
    logging the request, response, and latency of each call to the endpoint.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
      start_time = time.time()
      event_name = func.__name__  # extract the event_name
      print(f"appname: {self.app}")
      try:
        if isinstance(self.app, FastAPI):
          response = await func(*args, **kwargs)
          fastRequest = None
          for value in kwargs.values():
            if isinstance(value, Request):
              fastRequest = value
              break
  
          end_time = time.time()
          latency = end_time - start_time
  
          data = await self.adapter.extract_data(event_name, fastRequest,
                                                 response, latency)
        else:
          #Throw error
          print("Error: app is not a FastAPI app")
          raise Exception("Error: app is not a FastAPI app")
      except Exception as e:
        print(f"Error extracting data in log_event: {e}")
        return
      try:
        await self.log_event_post(data)
      except Exception as e:
        print(f"Error posting log event: {e}")
      return response

    return wrapper
