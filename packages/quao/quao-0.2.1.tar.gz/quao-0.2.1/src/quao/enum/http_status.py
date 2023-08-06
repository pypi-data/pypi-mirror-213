"""
    QuaO Project http_status.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class HttpStatus(Enum):
    NOT_YET_FINISHED = 201
    SUCCESS = 200
    ERROR = 400

