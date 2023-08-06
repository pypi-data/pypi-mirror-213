"""
    QuaO Project ibm_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qiskit import transpile

from ...model.device.qiskit_device import QiskitDevice
from ...util.json_parser_util import JsonParserUtils
from ...config.logging_config import logging


class IbmQuantumDevice(QiskitDevice):

    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _parse_job_result(self, job_result) -> dict:
        return JsonParserUtils.parse(job_result.to_dict())

    def _create_job(self, circuit, shots):
        logging.info('Create Ibm Quantum job with {0} shots'.format(shots))
        transpile_circuit = transpile(circuit, self.device)

        return self.device.run(transpile_circuit, shots=shots)
