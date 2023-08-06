from flask import request
from .base_adapter import BaseAdapter

class FlaskAdapter(BaseAdapter):
  def extract_data(self, event_name, request, response, latency):
    # Extract the data from the request and response
    request_data = self.extract_request_data(request)
    response_data = self.extract_response_data(response)

    # Combine request data and response data into one dictionary
    data = request_data
    data.update(response_data)
    data['latency'] = latency
    data[
      'function_name'] = event_name  # Add the event_name to the data dictionary

    return data

  def extract_request_data(self, request):
    # Extract the data from the request
    data = {}

    # Add the headers
    data['headers'] = dict(request.headers)

    # Add required fields
    data['plugin_hostname'] = request.url_root.split('/')[2]

    data['event_time'] = time.time()

    # Add endpoint info
    data['endpoint'] = request.path
    data['ip_address'] = request.remote_addr
    data['query_params'] = request.args.to_dict()
    data['method'] = request.method

    # Add request data
    data['request_body'] = request.get_json()

    return data

  def extract_response_data(self, response):
    # Print debug information about the response
    print(f"Response type: {type(response)}")
    print(f"Response content: {response}")

    if isinstance(response, Response):
        # If the response is a 'Response' object, extract its JSON data
        data = {}
        try:
            response_body = response.get_data(as_text=True)
            data['response_data'] = json.loads(response_body)
        except json.JSONDecodeError:
            data['response_data'] = None
        data['response_code'] = response.status_code
        data['response_size'] = len(response_body)

        return data
    else:
        # If the response is not a 'Response' object, defer to the base adapter
        return super().extract_response_data(response)

