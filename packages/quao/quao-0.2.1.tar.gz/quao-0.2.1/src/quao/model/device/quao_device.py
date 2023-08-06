"""
    QuaO Project quao_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import transpile
from qiskit import QiskitError

from ...enum.job_status import JobStatus
from ...util.json_parser_util import JsonParserUtils
from ...enum.sdk import Sdk
from ..device.device import Device
from ..provider.provider import Provider
from ...config.logging_config import logging


class QuaoDevice(Device):
    def __init__(self, provider: Provider, device_specification: str, sdk: str):
        super().__init__(provider, device_specification)
        self.sdk = sdk

    def _create_job(self, circuit, shots):
        logging.info('Create Quao job with {0} shots'.format(shots))
        if Sdk.QISKIT.value.__eq__(self.sdk):
            transpiled_circuit = transpile(circuits=circuit, backend=self.device)

            return self.device.run(transpiled_circuit, shots=shots)

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return self.device.run(task_specification=circuit, shots=shots)

        raise Exception("Sdk not supported!")

    def _is_simulator(self) -> bool:
        return True

    def _parse_job_result(self, job_result) -> dict:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return JsonParserUtils.parse(job_result.to_dict())

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return JsonParserUtils.parse(job_result.__dict__)

    def _produce_histogram_data(self, job_result) -> dict:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            try:
                histogram_data = job_result.get_counts()
            except QiskitError as qiskit_error:
                logging.info("Can't produce histogram with error: {0}".format(str(qiskit_error)))
                histogram_data = None

            return histogram_data

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return dict(job_result.measurement_counts)

    def _get_provider_job_id(self, job) -> str:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return job.job_id()

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return job.id

    def _get_job_status(self, job) -> str:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return job.status().name

        if Sdk.BRAKET.value.__eq__(self.sdk):
            job_state = job.state()
            if JobStatus.COMPLETED.value.__eq__(job_state):
                job_state = JobStatus.DONE.value
            return job_state
