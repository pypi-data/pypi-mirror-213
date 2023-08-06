## Set Up Fleet

# Install the SDK 

pip install fleet-sdk

# Import the SDK at the top of your plugin's files

from fleet_sdk.fastapi import Tracker 

from fleet_sdk.flask import Tracker 

from fleet_sdk.quart import Tracker 

# Initialize the SDK with your Plugins Analytics's ID.

tracker = Tracker("fleet-49b1bee7-b471-492a-a814-1bfbc2c2afa8", app=app)

# Add this decorator to the endpoints you want to track.

@tracker.log_event