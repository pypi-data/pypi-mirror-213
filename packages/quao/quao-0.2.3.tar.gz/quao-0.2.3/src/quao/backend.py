"""
    QuaO Project backend.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import io
from json import JSONDecodeError

import requests
from braket.circuits import Circuit
from qbraid import circuit_wrapper

from .data.job.job_response import JobResponse
from .data.request.request_data import RequestData
from .enum.job_status import JobStatus
from .enum.media_type import MediaType
from .enum.sdk import Sdk
from .factory.device_factory import DeviceFactory
from .factory.provider_factory import ProviderFactory
from .config.logging_config import logging


class Backend:
    def __init__(self, request_data: RequestData):
        self.server_url = request_data.server_url
        self.sdk = request_data.sdk
        self.input = request_data.input
        self.shots = request_data.shots
        self.circuit_export_url = request_data.circuit_export_url
        self.device_id = request_data.device_id
        self.backend_data = None

    def submit_job(self, circuit) -> JobResponse:
        """

        @param circuit:
        @return:
        """
        logging.info('Pre-execute job!')
        self.__pre_execute_job(circuit)

        logging.info('Execute job!')
        job_response = self.__execute_job(circuit)

        logging.info('Post-execute job!')
        self.__post_execute_job(circuit)

        return job_response

    @staticmethod
    def __get_qubit_number(circuit, sdk) -> int:
        """

        @param circuit:
        @param sdk:
        @return:
        """

        if Sdk.QISKIT.value.__eq__(sdk):
            return int(circuit.num_qubits)

        if Sdk.BRAKET.value.__eq__(sdk):
            return circuit.qubit_count

        return 0

    @staticmethod
    def __generate_backend_request(device_id, required_qubit):
        """

        @param device_id:
        @param required_qubit:
        @return:
        """

        backend_request = {
            "deviceId": device_id,
            "qubitAmount": required_qubit
        }

        return backend_request

    def __set_backend_data(self, backend_request):
        """

        @param backend_request:
        """

        response = requests.get(
            self.server_url,
            params=backend_request
        )
        if response.status_code == 200:
            try:
                self.backend_data = response.json().get("data")
            except JSONDecodeError:
                pass
        else:
            pass

    def __pre_execute_job(self, circuit):
        """

        @param circuit:
        """

        required_qubit = self.__get_qubit_number(circuit, self.sdk)
        backend_request = self.__generate_backend_request(self.device_id, required_qubit)

        logging.info('Device selection request: {0}'.format(backend_request))

        self.__set_backend_data(backend_request)

    def __execute_job(self, circuit) -> JobResponse:
        """

        @param circuit:
        @return:
        """

        job_response = JobResponse()
        shots = self.shots

        if circuit and self.backend_data:
            device_name = self.backend_data.get("deviceName")
            provider_tag = self.backend_data.get("providerTag")
            authentication = self.backend_data.get("authentication")

            try:
                logging.info('Execute job with provider tag: {0}'.format(provider_tag))
                provider = ProviderFactory().create_provider(provider_tag, authentication)

                logging.info('Execute job with device name: {0}'.format(device_name))
                device = DeviceFactory().create_device(provider, device_name, authentication, self.sdk)

                return device.run_circuit(circuit=circuit, shots=shots)

            except Exception as exception:
                return JobResponse(
                    job_status=JobStatus.ERROR.value,
                    job_result={"error": str(exception)})

        elif self.backend_data is None:
            job_response.job_status = JobStatus.ERROR.value
            job_response.job_result = {"error": "Backend not found"}

        return job_response

    def __post_execute_job(self, circuit):
        """

        @param circuit:
        """

        self.__export_circuit(circuit)

    def __export_circuit(self, circuit):
        """
          Export circuit to svg file then send to QuaO server for saving
          Args:
              circuit: circuit will be exported
              @param circuit:
        """

        logging.info("Preparing circuit figure...")
        if isinstance(circuit, Circuit):
            circuit = circuit_wrapper(circuit).transpile(Sdk.QISKIT.value)



        circuit_figure = circuit.draw(output='mpl', fold=-1)

        logging.info("Converting circuit figure to svg file...")
        figure_buffer = io.BytesIO()
        circuit_figure.savefig(figure_buffer, format='svg')

        logging.info("Sending circuit svg image to [{0}] with POST method ...".format(self.circuit_export_url))

        payload = {'circuit': (
            'circuit_figure',
            figure_buffer.getvalue(),
            MediaType.MULTIPART_FORM_DATA.value)}

        response = requests.post(url=self.circuit_export_url,
                                 files=payload)
        if response.ok:
            logging.info("Sending request successfully!")
        else:
            logging.info("Sending request failed with status {0}!".format(response.status_code))
