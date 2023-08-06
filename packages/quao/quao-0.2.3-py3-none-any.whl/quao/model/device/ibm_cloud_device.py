"""
    QuaO Project ibm_cloud_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import Options, Session, Sampler

from ...model.device.qiskit_device import QiskitDevice
from ...util.json_parser_util import JsonParserUtils
from ...config.logging_config import logging


class IbmCloudDevice(QiskitDevice):
    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _parse_job_result(self, job_result) -> dict:
        return JsonParserUtils.parse(job_result.__dict__)

    def _create_job(self, circuit, shots):
        logging.info('Create Ibm Cloud job with {0} shots'.format(shots))
        options = Options(optimization_level=1)
        options.execution.shots = shots

        with Session(service=self.provider.collect_providers(), backend=self.device) as session:
            sampler = Sampler(session=session, options=options)
            job = sampler.run(circuits=circuit)

            return job
