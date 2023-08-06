import json


class BaseAdapter:

  async def extract_response_data(self, response):
    # Extract the data from the response
    data = {}

    # Check if the response is a tuple (status_code, content)
    if isinstance(response, tuple):
      content, status_code = response
      data['response_code'] = status_code
      if isinstance(content, dict):
        data['response_data'] = content
        data['response_size'] = len(json.dumps(content))
      elif isinstance(content, str):
        data['response_data'] = {'message': content}
        data['response_size'] = len(content)
    elif isinstance(response, dict):
      # If the response is a dictionary, simply assign it to 'response_data'
      data['response_data'] = response
      data['response_code'] = 200
      data['response_size'] = len(json.dumps(response))
    elif isinstance(response, str):
      # If the response is a string, convert it to a dictionary for 'response_data'
      data['response_data'] = {'message': response}
      data['response_code'] = 200
      data['response_size'] = len(response)
    else:
      # If the response is an unexpected type, raise an exception
      raise ValueError(f"Unexpected response type: {type(response)}")

    return data
