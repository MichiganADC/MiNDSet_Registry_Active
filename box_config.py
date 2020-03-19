# box_config.py

# Import modules

from boxsdk import JWTAuth, Client
import os.path


# Configuration

# Set the path to config JSON file
pathToConfigJson = os.path.expanduser("~") + "/scripts/config/81663_ldlfw6r6_config.json"


# Functions

def get_authenticated_client(configPath):
    """Get an authenticated Box client for a JWT service account

    Arguments:
        configPath {str} -- Path to the JSON config file for your Box JWT app

    Returns:
        Client -- A Box client for the JWT service account

    Raises:
        ValueError -- if the configPath is empty or cannot be found.
    """
    if (os.path.isfile(configPath) == False):
        raise ValueError(f"configPath must be a path to the JSON config file for your Box JWT app")
    auth = JWTAuth.from_settings_file(configPath)
    print("Authenticating...")
    auth.authenticate_instance()
    return Client(auth)