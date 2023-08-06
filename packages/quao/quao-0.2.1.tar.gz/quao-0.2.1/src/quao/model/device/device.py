"""
    QuaO Project device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import abstractmethod, ABC

from ...data.job.job_response import JobResponse
from ...enum.job_status import JobStatus
from ...enum.media_type import MediaType
from ...model.provider.provider import Provider
from ...config.logging_config import logging


class Device(ABC):
    def __init__(self, provider: Provider, device_specification: str):
        self.provider = provider
        self.device = provider.get_backend(device_specification)

    def run_circuit(self, circuit, shots: int) -> JobResponse:
        """

        @param circuit:
        @param shots:
        """

        provider_job_id = ''
        content_type = None
        job_histogram = None

        try:
            job = self._create_job(circuit=circuit, shots=shots)
            provider_job_id = self._get_provider_job_id(job)
            job_status = self._get_job_status(job)
            job_result_dictionary = {}

            if self._is_simulator() or JobStatus.DONE.value.__eq__(job_status):
                job_result = job.result()
                job_status = self._get_job_status(job)

                logging.info('Parsing job result....')
                job_result_dictionary = self._parse_job_result(job_result)
                logging.info('Parsing job result completed!')

                content_type = MediaType.APPLICATION_JSON.value

                logging.info('Producing histogram ....')
                job_histogram = self._produce_histogram_data(job_result)
                logging.info('Producing histogram completed!')

        except Exception as exception:
            logging.info('Exception when invoke job on device {0}: {1}'.format(self.device.shots,
                                                                               str(exception)))
            job_result_dictionary = {
                "error": "Exception when invoke job on device: " + self.device.name,
                "exception": str(exception)
            }
            job_status = JobStatus.ERROR.value

        return JobResponse(
            provider_job_id=provider_job_id,
            job_status=job_status,
            job_result=job_result_dictionary,
            content_type=content_type,
            job_histogram=job_histogram
        )

    @abstractmethod
    def _create_job(self, circuit, shots):
        """

        @param circuit:
        @param shots:
        """
        pass

    @abstractmethod
    def _is_simulator(self) -> bool:
        """

        """
        pass

    @abstractmethod
    def _produce_histogram_data(self, job_result) -> dict:
        """

        @param job_result:
        """
        pass

    @abstractmethod
    def _get_provider_job_id(self, job) -> str:
        """

        """
        pass

    @abstractmethod
    def _get_job_status(self, job) -> str:
        """

        """
        pass

    @abstractmethod
    def _parse_job_result(self, job_result) -> dict:
        """

        """
        pass
