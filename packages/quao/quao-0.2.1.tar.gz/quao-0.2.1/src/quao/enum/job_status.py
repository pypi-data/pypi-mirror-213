"""
    QuaO Project job_status.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class JobStatus(Enum):
    DONE = 'DONE'
    ERROR = 'ERROR'
    COMPLETED = 'COMPLETED'
