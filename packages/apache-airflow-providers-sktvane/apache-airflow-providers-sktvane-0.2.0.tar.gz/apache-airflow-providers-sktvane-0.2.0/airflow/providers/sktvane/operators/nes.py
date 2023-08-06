import logging
from abc import ABCMeta, abstractmethod
from time import sleep

import requests
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults

logger = logging.getLogger(name=__name__)


class BaseProcessor(metaclass=ABCMeta):
    @abstractmethod
    def pre_process(self):
        pass

    @abstractmethod
    def notebook_path(self):
        pass

    @abstractmethod
    def post_process(self):
        pass

    @staticmethod
    def generate_processor(input_nb: str):
        if input_nb.startswith("https://github.com"):
            return GitHubProcessor(input_nb=input_nb)
        else:
            return GCSProcessor(input_nb=input_nb)


class GitHubProcessor(BaseProcessor):
    def __init__(self, input_nb: str):
        self.input_nb = input_nb

    def pre_process(self) -> None:
        pass

    def notebook_path(self) -> str:
        return self.input_nb

    def post_process(self) -> None:
        pass


class GCSProcessor(BaseProcessor):
    import uuid
    from datetime import datetime

    from ..macros import gcp

    _client = gcp.gcs_client()
    _bucket = _client.get_bucket("nes_notebooks_seoul_28d")
    _filename = f"{datetime.now().date()}/{uuid.uuid4()}.ipynb"
    _gcs_blob = _bucket.blob(_filename)

    def __init__(self, input_nb: str):
        self.input_nb = input_nb

    def pre_process(self) -> None:
        self._gcs_blob.upload_from_filename(self.input_nb)

    def notebook_path(self) -> str:
        return f"gs://{self._bucket.name}/{self._filename}"

    def post_process(self) -> None:
        self._gcs_blob.delete()


class NesOperator(BaseOperator):
    template_fields = ("input_nb", "parameters")

    nes = "http://nes.sktai.io/v1/runs"
    poll_interval = 60
    run_id = None
    output_url = None

    @apply_defaults
    def __init__(
        self,
        input_nb: str,
        parameters: dict = None,
        runtime: str = None,
        profile: str = None,
        host_network: bool = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.input_nb = input_nb
        self.parameters = parameters
        self.runtime = runtime
        self.profile = profile
        self.host_network = host_network
        self.processor = BaseProcessor.generate_processor(input_nb=self.input_nb)

    def pre_execute(self, context):
        self.processor.pre_process()

    def execute(self, context):
        def submit_job() -> tuple[str, str]:
            request_body = dict(
                input_url=self.processor.notebook_path(),
                parameters=self.parameters,
                runtime=self.runtime,
                profile=self.profile,
                host_network=self.host_network,
            )
            response = requests.post(url=self.nes, json=request_body)
            logger.info(f"Job submitted with: {request_body}")
            response.raise_for_status()
            response = response.json()
            return response["id"], response["output_url"]

        def get_status() -> str:
            response = requests.get(url=f"{self.nes}/{self.run_id}")
            response.raise_for_status()
            response = response.json()
            return response["status"]

        self.run_id, self.output_url = submit_job()
        logger.info(
            f"""--------------------------------------------------------------------------------\n\n{self.output_url}\n\n--------------------------------------------------------------------------------"""
        )

        while (status := get_status()) != "Succeeded":
            if status in ["Failed", "Error"]:
                raise AirflowException(f'Job {self.run_id} exited with "{status}"')
            else:
                logger.info(f'Polling job status... current status: "{status}"')
                sleep(self.poll_interval)

        logger.info(f'Job {id} successfully finished with "{status}"')

    def post_execute(self, context: Context, result=None):
        self.processor.post_process()

    def on_kill(self):
        while True:
            res = requests.delete(f"{self.nes}/{self.run_id}")
            if res.status_code == 404:
                break
            status = res.json()["status"]
            logger.info(f'Deleting job... current status: "{status}"')
            sleep(self.poll_interval)
        self.processor.post_process()
