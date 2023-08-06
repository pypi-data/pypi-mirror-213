"""
    QuaO Project aws_braket_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..device.device import Device
from ..provider.provider import Provider
from ...enum.job_status import JobStatus
from ...util.json_parser_util import JsonParserUtils
from ...config.logging_config import logging


class AwsBraketDevice(Device):

    def __init__(self, provider: Provider,
                 device_specification: str,
                 s3_bucket_name: str,
                 s3_prefix: str):
        super().__init__(provider, device_specification)
        self.s3_folder = (s3_bucket_name, s3_prefix)

    def _create_job(self, circuit, shots):
        logging.info('Create AWS Braket job with {0} shots'.format(shots))
        return self.device.run(task_specification=circuit,
                               s3_destination_folder=self.s3_folder,
                               shots=shots)

    def _is_simulator(self) -> bool:
        return 'SIMULATOR'.__eq__(self.device.type.value)

    def _produce_histogram_data(self, job_result) -> dict:
        return dict(job_result.measurement_counts)

    def _get_provider_job_id(self, job) -> str:
        return job.id

    def _get_job_status(self, job) -> str:
        job_state = job.state()
        if JobStatus.COMPLETED.value.__eq__(job_state):
            job_state = JobStatus.DONE.value
        return job_state

    def _parse_job_result(self, job_result) -> dict:
        return JsonParserUtils.parse(job_result.__dict__)
