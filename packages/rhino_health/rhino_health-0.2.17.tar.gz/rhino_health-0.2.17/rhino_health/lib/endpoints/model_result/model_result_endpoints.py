from io import BytesIO

from rhino_health.lib.endpoints.endpoint import Endpoint
from rhino_health.lib.endpoints.model_result.model_result_dataclass import ModelResult
from rhino_health.lib.utils import rhino_error_wrapper


class ModelResultEndpoints(Endpoint):
    @property
    def model_result_data_class(self):
        """
        @autoapi False
        """
        return ModelResult

    @rhino_error_wrapper
    def halt_model_run(self, model_action_uid: str):
        """
        Send a halting request to a running aimodel.

        This triggers the halting process but does not wait for halting to complete.

        If triggering the halting process fails, a message specifying the error is returned.

        Parameters
        ----------
        model_result_uid: str
            UID of the ModelResult representing the aimodel run to halt.

        Returns
        -------
        json response in the format of:
          "status": the request's status code -
                - 200: valid request, halting innitiated.
                - 400: invalid request, the model can not be halted, or does not exist.
                - 500: error while initiating halting.
          "data":  message specifying if the halting was initiated or failed. In case the request failed,
           the error message is also displayed.

        Examples
        --------
        >>> session.model_results.halt_model_run(model_action_uid)

        """
        result = self.session.get(f"/federatedmodelactions/{model_action_uid}/halt")
        return result


class ModelResultFutureEndpoints(ModelResultEndpoints):
    @rhino_error_wrapper
    def get_model_result(self, model_result_uid: str):
        """
        Returns a ModelResult dataclass

        Parameters
        ----------
        model_result_uid: str
            UID for the ModelResult

        Returns
        -------
        model_result: ModelResult
            ModelResult dataclass

        Examples
        --------
        >>> session.aimodel.get_model_result(model_result_uid)
        ModelResult()
        """
        result = self.session.get(f"/federatedmodelactions/{model_result_uid}")
        return result.to_dataclass(self.model_result_data_class)

    @rhino_error_wrapper
    def get_model_params(self, model_result_uid: str) -> BytesIO:
        """
        Returns a byte representation of the model params associated with a MODEL_RESULT_UID

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        model_result_uid: str
            UID for the ModelResult

        Returns
        -------
        model_params: BytesIO
            A Python BytesIO Buffer

        Examples
        --------
        >>> with open("my_output_file.out", "wb") as output_file:
        >>>     model_params_buffer = session.model_result.get_model_params(model_result_uid)
        >>>     output_file.write(model_params_buffer.getbuffer())
        """
        result = self.session.get(
            f"/federatedmodelactions/{model_result_uid}/download_model_params"
        )
        return BytesIO(result.raw_response.content)

    # @rhino_error_wrapper
    # def __logs(self, model_result_uid: str):
    #     """
    #     @autoapi False
    #
    #     .. warning:: This feature is under development and the interface may change
    #     """
    #     result = self.session.get(
    #         f"/federatedmodelactions/{model_result_uid}/logs"
    #     )
    #     return result["logs"]
