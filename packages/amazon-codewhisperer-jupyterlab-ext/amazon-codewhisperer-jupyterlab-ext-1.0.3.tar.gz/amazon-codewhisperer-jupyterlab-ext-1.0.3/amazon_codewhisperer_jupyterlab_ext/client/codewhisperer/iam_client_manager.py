from abc import ABC
import logging
from amazon_codewhisperer_jupyterlab_ext.client.codewhisperer.client_manager import CodeWhispererClientManager
from amazon_codewhisperer_jupyterlab_ext.constants import (
    REQUEST_OPTOUT_HEADER_NAME,
    RTS_PROD_ENDPOINT,
    RTS_PROD_REGION,
    SIGV4
)

logging.basicConfig(format="%(levelname)s: %(message)s")


class CodeWhispererIamClientManager(CodeWhispererClientManager, ABC):

    def __init__(self):
        super().__init__()
        self._client = self.session.client(
            service_name=SIGV4,
            endpoint_url=RTS_PROD_ENDPOINT,
            region_name=RTS_PROD_REGION,
            verify=False,
        )

    def invoke_recommendations(self, request, opt_out):
        return self._client.generate_recommendations(**request)
