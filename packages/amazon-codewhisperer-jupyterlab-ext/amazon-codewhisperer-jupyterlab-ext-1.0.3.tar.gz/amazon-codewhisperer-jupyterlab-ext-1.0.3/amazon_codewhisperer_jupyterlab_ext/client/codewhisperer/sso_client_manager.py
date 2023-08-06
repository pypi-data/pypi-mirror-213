from abc import ABC
from botocore import UNSIGNED
from botocore.client import Config
from amazon_codewhisperer_jupyterlab_ext.client.codewhisperer.client_manager import CodeWhispererClientManager
from amazon_codewhisperer_jupyterlab_ext.constants import (
    REQUEST_OPTOUT_HEADER_NAME,
    RTS_PROD_ENDPOINT,
    RTS_PROD_REGION,
    BEARER
)


class CodeWhispererSsoClientManager(CodeWhispererClientManager, ABC):
    _initialized = False

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        super().__init__()
        self._bearer_token = ""
        self._opt_out = False
        self._client = self.session.client(
            service_name=BEARER,
            endpoint_url=RTS_PROD_ENDPOINT,
            region_name=RTS_PROD_REGION,
            config=Config(signature_version=UNSIGNED),
        )

        self._client.meta.events.register_first("before-sign.*.*", self._add_header)

    def _add_header(self, request, **kwargs):
        request.headers.add_header("Authorization", "Bearer " + self._bearer_token)
        request.headers.add_header(REQUEST_OPTOUT_HEADER_NAME, f"{self._opt_out}")

    def invoke_recommendations(self, request, opt_out):
        self._opt_out = opt_out
        return self.get_client().generate_completions(**request)

    def set_bearer_token(self, token):
        self._bearer_token = token
