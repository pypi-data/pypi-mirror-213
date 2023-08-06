"""
    QuaO Project job_status.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import QiskitError
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.providers.jobstatus import JobStatus
from json import dumps

from ...data.job.job_response import JobResponse
from ...enum.media_type import MediaType
from ...util.json_parser_util import JsonParserUtils


class Job:
    def __init__(self, channel, token, crn, provider_job_id):
        self.channel = channel if channel else "ibm_quantum"
        self.token = token if token else ""
        self.crn = crn if crn else None
        self.job_id = provider_job_id if provider_job_id else ""
        self.retrieve_job = self.__get_job()

    def fetch_job(self) -> JobResponse:

        content_type = None
        job_histogram = None
        job_result = None
        status = self.retrieve_job.status()
        job_status = status.name

        if status == JobStatus.DONE:
            try:
                result = self.retrieve_job.result()
                # case function `sampler`
                if self.retrieve_job.program_id == 'sampler':
                    job_result = JsonParserUtils.parse(result.__dict__)
                # case function `circuit-runner`

                else:
                    job_result = JsonParserUtils.parse(result.to_dict())
                    # handle case Statevector object not serializable when run with backend `statevector_simulator`
                    if self.retrieve_job.backend().backend_name == 'statevector_simulator':
                        job_result = dumps(job_result, default=str)
                content_type = MediaType.APPLICATION_JSON.value

                # handle circuit has measure
                try:
                    job_histogram = result.get_counts()
                except QiskitError:
                    job_histogram = None

            except Exception as exception:
                job_result = {
                    "error": "Exception when get job result",
                    "exception": str(exception)
                }
                job_status = JobStatus.ERROR.value

        return JobResponse(
            provider_job_id=self.job_id,
            job_status=job_status,
            job_result=job_result,
            content_type=content_type,
            job_histogram=job_histogram
        )

    def __get_job(self):
        service = QiskitRuntimeService(channel=self.channel,
                                       token=self.token,
                                       instance=self.crn)

        return service.job(job_id=self.job_id)
