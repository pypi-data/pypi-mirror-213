import time
import json
import requests
import pkg_resources
from functools import wraps
from fastapi import Request, Response, FastAPI
from quart import request as QuartRequest, Quart, Response as QuartResponse
from flask import request as FlaskRequest, Flask, Response as FlaskResponse
import importlib
import os
import sys

# Add the parent directory of 'sdk' to the system path
sdk_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(sdk_dir)
if parent_dir not in sys.path:
  sys.path.insert(0, parent_dir)

class BaseTracker:
  DEFAULT_HOST = 'middleware.usefleet.ai'
  DEFAULT_DEBUG = True

  def __init__(self, token, app, host=DEFAULT_HOST, debug=DEFAULT_DEBUG):
    """
        Initialize the Tracker with the provided token, host, and debug flag.
    """
    self.token = token
    self.host = host
    self.debug = debug
    self.app = app  # Store the app instance

  def log_event(self, func):
    """
    This function should be overridden by subclasses to implement the logging logic.
    """
    raise NotImplementedError("log_event must be overridden by subclasses")

  async def log_event_post(self, data):
    """ 
    Log an event with the provided data. 
    """
    try:
      # Construct the payload as a list of objects, one for each event
      payload = [{}]
      # Get the installed version of the SDK
      sdk_version = pkg_resources.get_distribution("fleet-sdk").version
  
      # Add the SDK version
      payload[0]['sdk_version'] = sdk_version
  
      #Add the header data
      payload[0]['headers'] = data.get('headers')  # Add headers
  
      # Add the required fields
      payload[0]['function_name'] = data.get('function_name')
      payload[0]['plugin_analytics_id'] = self.token
      payload[0]['plugin_hostname'] = data.get('plugin_hostname')
      payload[0]['event_time'] = time.time()
  
      # Add endpoint info
      payload[0]['endpoint'] = data.get('endpoint')
      payload[0]['ip_address'] = data.get('ip_address')
      payload[0]['query_params'] = data.get('query_params')
      payload[0]['method'] = data.get('method')
  
      # Add request data
      payload[0]['request_body'] = data.get('request_body')
  
      # Add response data
      payload[0]['response_data'] = data.get('response_data')
  
      # Add response code/size/latency
      payload[0]['response_code'] = data.get('response_code')
      payload[0]['response_size'] = data.get('response_size')
  
      payload[0]['latency'] = data.get('latency')
  
      uri = f"http://{self.host}/log_events/"
      r = requests.post(url=uri, json=payload)
      if self.debug:
        print(f"bot-lens endpoint: {uri}")
        print(f"payload is {payload}")
        print(f"{r.status_code} Response:{r.text}")
    except Exception as e:
        print(f"Error in log_event_post: {e}")
