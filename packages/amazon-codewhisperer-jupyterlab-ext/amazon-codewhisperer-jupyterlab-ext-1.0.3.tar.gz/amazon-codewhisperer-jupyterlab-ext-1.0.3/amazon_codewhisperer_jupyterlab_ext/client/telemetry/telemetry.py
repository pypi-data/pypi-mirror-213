import boto3
import logging
from botocore.exceptions import ClientError
from pathlib import Path
from amazon_codewhisperer_jupyterlab_ext.constants import (
    PROD_COGNITO_POOL_ID,
    INVALID_TOKEN_EXCEPTION_MESSAGE,
    TELEMETRY_PROD_ENDPOINT,
    PostMetricsRequestConstants,
)

logging.basicConfig(format="%(levelname)s: %(message)s")
session = boto3.Session()


class ToolkitTelemetry:
    def __init__(self):
        self.session = boto3.Session()
        session_folder =  f"{Path(__file__).parent.parent}/service_models"
        self.session._loader.search_paths.append(session_folder)
        self.cognito_client = boto3.client("cognito-identity", region_name="us-east-1")
        self.identity_id = self.cognito_client.get_id(
            IdentityPoolId=PROD_COGNITO_POOL_ID
        )["IdentityId"]
        credentials = self.cognito_client.get_credentials_for_identity(
            IdentityId=self.identity_id
        )["Credentials"]
        self.telemetry_client = self.session.client(
            "telemetry",
            region_name="us-east-1",
            endpoint_url=TELEMETRY_PROD_ENDPOINT,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretKey"],
            aws_session_token=credentials["SessionToken"],
        )

        self.credential_expire_time = credentials["Expiration"]

    def post_metrics(self, request, parent_product):
        logging.info(request["ClientID"])
        logging.info(request["MetricData"][0]["EpochTimestamp"])
        try:
            self.telemetry_client.post_metrics(
                AWSProduct=request[PostMetricsRequestConstants.AWS_PRODUCT],
                AWSProductVersion=request[
                    PostMetricsRequestConstants.AWS_PRODUCT_VERSION
                ],
                ClientID=request[PostMetricsRequestConstants.CLIENT_ID],
                MetricData=request[PostMetricsRequestConstants.METRIC_DATA],
                ParentProduct=parent_product,
            )
        except ClientError as e:
            if INVALID_TOKEN_EXCEPTION_MESSAGE in e.response["Error"]["Message"]:
                logging.info("refreshing credentials")
                self._refresh_credentials()
                self.telemetry_client.post_metrics(
                    AWSProduct=request[PostMetricsRequestConstants.AWS_PRODUCT],
                    AWSProductVersion=request[
                        PostMetricsRequestConstants.AWS_PRODUCT_VERSION
                    ],
                    ClientID=request[PostMetricsRequestConstants.CLIENT_ID],
                    MetricData=request[PostMetricsRequestConstants.METRIC_DATA],
                    ParentProduct=parent_product,
                )
            else:
                raise e

        logging.info("sent telemetry")

    def _refresh_credentials(self):
        credentials = self.cognito_client.get_credentials_for_identity(
            IdentityId=self.identity_id
        )["Credentials"]
        self.telemetry_client = self.session.client(
            "telemetry",
            region_name="us-east-1",
            endpoint_url=TELEMETRY_PROD_ENDPOINT,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretKey"],
            aws_session_token=credentials["SessionToken"],
        )

        ## TODO: can use expire time to refresh
        # self.credential_expire_time = credentials["Expiration"]
