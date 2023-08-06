import time
import json
from fastapi import Request, Response
from .base_adapter import BaseAdapter
from typing import Union, Dict


class FastAPIAdapter(BaseAdapter):

  async def extract_data(self, event_name, request: Request,
                         response: Response, latency):
    
    # Extract the data from the request and response
    request_data = await self.extract_request_data(request)
    response_data = await self.extract_response_data(response)

    # Combine request data and response data into one dictionary
    data = request_data
    data.update(response_data)
    data['latency'] = latency
    data[
      'function_name'] = event_name  # Add the event_name to the data dictionary

    return data

  async def extract_request_data(self, request: Request):
    # Extract the data from the request
    data = {}

    # Add the headers
    data['headers'] = dict(request.headers)

    # Add required fields
    data['plugin_hostname'] = request.base_url.hostname

    data['event_time'] = time.time()

    # Add endpoint info
    data['endpoint'] = request.url.path
    data['ip_address'] = request.client.host
    data['query_params'] = dict(request.query_params)
    data['method'] = request.method

    # Add request data
    try:
      data['request_body'] = await request.json()
    except json.JSONDecodeError:
      data['request_body'] = None

    return data

  async def extract_response_data(self, response: Union[Response, Dict, str]):
    # Print debug information about the response
    print(f"Response type: {type(response)}")
    print(f"Response content: {response}")

    if isinstance(response, Response):
      # If the response is a 'Response' object, extract its JSON data
      data = {}
      try:
        data['response_data'] = response.json()
      except Exception:
        data['response_data'] = None
      data['response_code'] = response.status_code
      data['response_size'] = len(json.dumps(data['response_data']))

      return data
    else:
      # If the response is not a 'Response' object, defer to the base adapter
      return await super().extract_response_data(response)
