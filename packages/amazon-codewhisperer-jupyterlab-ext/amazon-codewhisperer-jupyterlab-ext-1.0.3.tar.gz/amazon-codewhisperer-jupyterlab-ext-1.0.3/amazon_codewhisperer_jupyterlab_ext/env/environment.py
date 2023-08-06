import json
import os
import requests
from packaging.version import Version
from amazon_codewhisperer_jupyterlab_ext.constants import CURRENT_VERSION, CODEWHISPERER_PYPI_JSON_URL, NEW_VERSION_USER_MESSAGE

class Environment:
    SM_STUDIO = "SageMaker Studio"
    JUPYTER_OSS = "Jupyter OSS"

    # TODO : Update version for new release to get notification
    CURRENT_VERSION = "0.1.0"

    @staticmethod
    def get_update_notification():
        try:
            # Get the URL from environment variable or fall back to default
            url = os.environ.get("JSON_URL", CODEWHISPERER_PYPI_JSON_URL)

            # Download the JSON data
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Get the latest version and launch date
            latest_version = data["info"]["version"]

            # Compare the current version with the latest version
            if Version(latest_version) > Version(CURRENT_VERSION):
                return NEW_VERSION_USER_MESSAGE.format(latest_version), latest_version
            else:
                return "", ""
        except Exception as e:
            print(f"Error: {e}")
            return "", ""
    

    @staticmethod
    def get_environment():
        env = Environment.JUPYTER_OSS
        try:
            with open('/opt/ml/metadata/resource-metadata.json', 'r') as f:
                data = json.load(f)
                if 'ResourceArn' in data:
                    env = Environment.SM_STUDIO
        except Exception as e:
            # Default to Builder ID / Jupyter OSS for all errors
            pass
        return env
