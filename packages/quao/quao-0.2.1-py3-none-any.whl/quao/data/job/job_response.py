"""
    QuaO Project job_response.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ...enum.media_type import MediaType
from ...enum.job_status import JobStatus


class JobResponse(object):
    def __init__(
            self,
            provider_job_id: str = "",
            job_status: str = "",
            job_result=None,
            content_type=None,
            job_histogram=None
    ):
        self.provider_job_id = provider_job_id if provider_job_id else ""
        self.job_status = job_status if job_status else JobStatus.ERROR.value
        self.job_result = job_result if job_result else None
        self.content_type = content_type if content_type else MediaType.ALL_TYPE.value
        self.job_histogram = job_histogram if job_histogram else None
