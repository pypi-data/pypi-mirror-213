"""
    QuaO Project json_parser_util.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from datetime import datetime
from enum import Enum

import numpy as np


class JsonParserUtils:

    @staticmethod
    def parse(unparsed_input: dict) -> dict:
        data_holder = {}

        for key, value in unparsed_input.items():
            if isinstance(value, (set, tuple)):
                value = list(value)
            if isinstance(value, np.ndarray):
                value = value.tolist()
            if isinstance(value, (complex, datetime)):
                value = value.__str__()

            if isinstance(value, dict):
                data_holder[key] = JsonParserUtils.parse(value)
            elif isinstance(value, (str, int, float, bool, Enum)) or value is None:
                data_holder[key] = value
            elif isinstance(value, (list,)):
                data_list_holder = []
                for data in value:
                    data = JsonParserUtils.__resolve_type(data)
                    if isinstance(data, dict):
                        data_list_holder.append(JsonParserUtils.parse(data))
                    else:
                        data_list_holder.append(data)
                data_holder[key] = data_list_holder
            else:
                data_holder[key] = JsonParserUtils.parse(value.__dict__)

        return data_holder

    @staticmethod
    def __resolve_type(element):
        if isinstance(element, (complex, datetime)):
            return element.__str__()
        if isinstance(element, (dict, str, int, float, bool, Enum)) or element is None:
            return element
        if isinstance(element, np.ndarray):
            return JsonParserUtils.__resolve_type(element.tolist())
        if isinstance(element, (list,)):
            data_holder = []
            for data in element:
                data_holder.append(JsonParserUtils.__resolve_type(data))
            return data_holder
        return element.__dict__
