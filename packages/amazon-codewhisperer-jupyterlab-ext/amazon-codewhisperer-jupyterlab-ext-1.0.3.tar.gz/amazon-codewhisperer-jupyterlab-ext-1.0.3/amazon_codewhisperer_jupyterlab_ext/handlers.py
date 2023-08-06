import os
import json
import logging
from abc import ABC

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler
from amazon_codewhisperer_jupyterlab_ext.env import Environment
from amazon_codewhisperer_jupyterlab_ext.client.codewhisperer import CodeWhispererIamClientManager, CodeWhispererSsoClientManager
from amazon_codewhisperer_jupyterlab_ext.client.telemetry import ToolkitTelemetry
from amazon_codewhisperer_jupyterlab_ext.utils import ServiceResponse, ServiceResponseStatus, ServiceErrorInfo
from amazon_codewhisperer_jupyterlab_ext.validator import InputValidator
from amazon_codewhisperer_jupyterlab_ext.auth.sso_auth_manager import CodeWhispererSsoAuthManager

logging.basicConfig(format="%(levelname)s: %(message)s")

toolkit_telemetry_api = ToolkitTelemetry()
authManager = CodeWhispererSsoAuthManager()


class RecommendationHandler(APIHandler, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        environment = Environment.get_environment()
        self.input_validator = InputValidator()
        self.codewhisperer_client = CodeWhispererIamClientManager() \
            if environment == Environment.SM_STUDIO \
            else CodeWhispererSsoClientManager()

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        try:
            if not self.input_validator.is_valid_input("generate_recommendations", input_data):
                self.set_status(400)
                self.finish(json.dumps({'success': False,  'message': 'Invalid input data.'}))
                return
            token = self.request.headers['Token']
            opt_out = self.request.headers['OptOut']
            if token is not None and isinstance(self.codewhisperer_client, CodeWhispererSsoClientManager):
                self.codewhisperer_client.set_bearer_token(token)
            resp = self.codewhisperer_client.generate_recommendations(input_data, opt_out == 'True')
            self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class RegisterClientHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def get(self):
        try:
            resp = authManager.register_client()
            self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class DeviceAuthorizationHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def post(self):
        try:
            input_data = self.get_json_body()
            resp = authManager.device_authorization(input_data)
            self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class CreateTokenHandler(APIHandler, ABC):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        try:
            input_data = self.get_json_body()
            resp = yield authManager.create_token(
                input_data['clientRegistration'],
                input_data['deviceAuthorizationResponse']
            )
            if resp is None:
                self.finish(json.dumps(resp))
            else:
                self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class RefreshHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def post(self):
        try:
            input_data = self.get_json_body()
            resp = authManager.refresh(input_data['clientRegistration'], input_data['token'])
            self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class CancelLoginHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def get(self):
        try:
            authManager.cancel_login()
            self.finish()
        except Exception as e:
            return_server_error(self)


class PostMetricsHandler(APIHandler, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        environment = Environment.get_environment()
        self.parent_product = environment

    @tornado.web.authenticated
    def post(self):
        input_data = self.get_json_body()
        logging.info("input data: ", input_data)
        toolkit_telemetry_api.post_metrics(input_data, self.parent_product)


class GetEnvironmentHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def get(self):
        update_notification, latest_version = Environment.get_update_notification()
        self.finish(json.dumps(ServiceResponse(
            ServiceResponseStatus.SUCCESS,
            {
                'environment': Environment.get_environment(),
                'version_notification' : update_notification,
                'latest_version' : latest_version
            },
            None,
            None,
            None
        ).__dict__))


def setup_handlers(web_app, url_path):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    # Prepend the base_url so that it works in a JupyterHub setting
    generate_recommendations_pattern = url_path_join(base_url, url_path, "generate_recommendations")
    register_client_pattern = url_path_join(base_url, url_path, "register_client")
    device_authorization_pattern = url_path_join(base_url, url_path, "device_authorization")
    create_token = url_path_join(base_url, url_path, "create_token")
    refresh_pattern = url_path_join(base_url, url_path, "refresh")
    cancel_login_pattern = url_path_join(base_url, url_path, "cancel_login")
    post_metrics_pattern = url_path_join(base_url, url_path, "post_metrics")
    get_environment_pattern = url_path_join(base_url, url_path, "get_environment")
    handlers = [(generate_recommendations_pattern, RecommendationHandler),
                (register_client_pattern, RegisterClientHandler),
                (device_authorization_pattern, DeviceAuthorizationHandler),
                (create_token, CreateTokenHandler),
                (refresh_pattern, RefreshHandler),
                (cancel_login_pattern, CancelLoginHandler),
                (post_metrics_pattern, PostMetricsHandler),
                (get_environment_pattern, GetEnvironmentHandler)]
    web_app.add_handlers(host_pattern, handlers)

    # Prepend the base_url so that it works in a JupyterHub setting
    doc_url = url_path_join(base_url, url_path, "public")
    doc_dir = os.getenv(
        "JLAB_SERVER_EXAMPLE_STATIC_DIR",
        os.path.join(os.path.dirname(__file__), "public"),
    )
    handlers = [("{}/(.*)".format(doc_url), StaticFileHandler, {"path": doc_dir})]
    web_app.add_handlers(".*$", handlers)


def return_server_error(api_handler):
    api_handler.set_status(500)
    api_handler.finish(json.dumps(ServiceResponse(
        ServiceResponseStatus.ERROR,
        None,
        ServiceErrorInfo('InternalServerException', 'Internal server error. Try again later'),
        None,
        None
    ).__dict__))
