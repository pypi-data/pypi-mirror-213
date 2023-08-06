from abc import ABC, abstractmethod
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from amazon_codewhisperer_jupyterlab_ext.utils import generate_succeeded_service_response, \
    generate_client_error_codewhisperer_service_response


# Interface for managing lifecycles of different sdk clients.
class CodeWhispererClientManager(ABC):
    _instance = None

    def __init__(self):
        self.session = boto3.Session()
        self._client = None
        session_folder = f"{Path(__file__).parent.parent}/service_models"
        self.session._loader.search_paths.append(session_folder)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_client(self):
        return self._client

    @abstractmethod
    def invoke_recommendations(self, request, opt_out):
        pass

    def generate_recommendations(self, recommendation_request, opt_out):
        try:
            recommendation_response = self.invoke_recommendations(recommendation_request, opt_out)
            return generate_succeeded_service_response(recommendation_response)
        except ClientError as e:
            return generate_client_error_codewhisperer_service_response(e)
