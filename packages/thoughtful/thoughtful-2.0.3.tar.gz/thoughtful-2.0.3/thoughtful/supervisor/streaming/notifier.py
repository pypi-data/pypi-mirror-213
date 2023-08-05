from __future__ import annotations

import logging
import warnings

import requests

from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport
from thoughtful.supervisor.streaming.jwt_auth import JWTAuth
from thoughtful.supervisor.streaming.payloads import ArtifactsUploadedPayload
from thoughtful.supervisor.streaming.payloads import BotManifestStreamingPayload
from thoughtful.supervisor.streaming.payloads import StatusChangePayload
from thoughtful.supervisor.streaming.payloads import StepReportStreamingPayload
from thoughtful.supervisor.streaming.payloads import StreamingPayload
from thoughtful.supervisor.streaming.token import Token

logger = logging.getLogger(__name__)

POST_TIMEOUT_SECONDS = 10


class Notifier(requests.Session):
    """
    Provides run status updates to a third party client (eg, Fabric/Empower)
    by posting requests to its callback URL.
    """

    def __init__(
        self,
        run_id: str,
        callback_url: str,
        auth: JWTAuth,
    ):
        super().__init__()
        self.run_id = run_id
        self.callback_url = callback_url
        self.auth: JWTAuth = auth

    @classmethod
    def from_encoded_tokens(
        cls,
        run_id: str,
        callback_url: str,
        access_token: str,
        refresh_token: str,
        refresh_url: str,
    ) -> Notifier:
        """
        Convenience constructor for creating an instance from the string
        (encoded) JWT tokens.
        """
        new_auth = JWTAuth(
            access_token=Token(access_token) if access_token else None,
            refresh_token=Token(refresh_token) if refresh_token else None,
            refresh_url=refresh_url,
        )
        return cls(
            run_id=run_id,
            callback_url=callback_url,
            auth=new_auth,
        )

    def post(self, payload: StreamingPayload, **kwargs):
        if not (self.callback_url and self.run_id):
            warnings.warn(
                "Notifier not configured with callback URL and run ID; will not post stream update"
            )
            return

        message_json = payload.__json__()

        try:
            logger.info("Posting streaming message")
            logger.info("URL: %s", self.callback_url)
            logger.info("Payload: %s", message_json)
            response = super().post(
                self.callback_url,
                json=message_json,
                timeout=POST_TIMEOUT_SECONDS,
                **kwargs,
            )
        except Exception as ex:
            # A failed stream message shouldn't break a bot, so catch any possible
            # exception and log it
            logger.exception("Could not post step payload to endpoint")
            return

        logger.info(f"Received response: ({response.status_code}): {response.text}")

        return response

    def post_step_update(self, report: StepReport):
        logger.info(f"Posting step update id={report.step_id} status={report.status}")
        return self.post(StepReportStreamingPayload(report, self.run_id))

    def post_manifest(self, manifest: Manifest):
        return self.post(BotManifestStreamingPayload(manifest, self.run_id))

    def post_artifacts_uploaded(self, output_uri: str):
        return self.post(
            ArtifactsUploadedPayload(
                run_id=self.run_id, output_artifacts_uri=output_uri
            )
        )

    def post_status_change(self, status: Status):
        return self.post(StatusChangePayload(run_id=self.run_id, status=status))


if __name__ == "__main__":
    at = "xxxxxx"
    rt = "yyyyyy"
    _id = "1"
    url = "https://YOUR_URL_ID.execute-api.us-east-1.amazonaws.com/STAGE/webhooks/users-processes-updates/jwt"
    ref_ur = (
        "https://YOUR_URL_ID.execute-api.us-east-1.amazonaws.com/STAGE/refresh-token"
    )

    callback = Notifier.from_encoded_tokens(
        run_id=_id,
        callback_url=url,
        access_token=at,
        refresh_token=rt,
        refresh_url=ref_ur,
    )
    callback.post_status_change(Status.SUCCEEDED)
