from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from gabgabgurus.common.decorators import default
from gabgabgurus.common.utils.api import get_success_headers


class QueryParamsMixin(APIView):
    query_params_serializer_class = None

    def parse_query_params_to_dict(self) -> dict:
        serializer = self.get_query_params_serializer()
        validated_query_params = self.validate_query_params(serializer)
        if validated_query_params is not None:
            serializer_fields = serializer.fields.keys()
            fields_with_values = {field: validated_query_params.get(field) for field in serializer_fields}
            return fields_with_values

        return {}

    def get_query_params_serializer(self):
        data = self.get_query_params()
        serializer_class = self.get_query_params_serializer_class()
        serializer = serializer_class(data=data)
        return serializer

    def get_query_params(self):
        return self.request.query_params

    def get_query_params_serializer_class(self):
        return self.query_params_serializer_class

    @default(raise_exception=True)
    def validate_query_params(self, serializer=None, **kwargs):
        _serializer = serializer
        if serializer is None:
            _serializer = self.get_query_params_serializer()
        if _serializer.is_valid(raise_exception=kwargs["raise_exception"]):
            return _serializer.validated_data
        return None


class InputOutputSerializerAPIView(GenericAPIView):
    input_serializer_class = None
    output_serializer_class = None

    def get_serializer_class(self):
        return self.get_input_serializer_class() or super().get_serializer_class()

    def get_input_serializer_class(self):
        if self.input_serializer_class and self.request_method_is_unsafe():
            return self.input_serializer_class
        return None

    def request_method_is_unsafe(self):
        return self.request.method in ("POST", "PUT", "PATCH", "DELETE")

    def response(self, serializer, operation_result, **kwargs):
        response_data = self.get_response_data(serializer, operation_result, **kwargs)
        status_code = self.get_status_code(response_data)
        headers = get_success_headers(serializer.data)
        return Response(response_data, status_code, headers=headers)

    def get_response_data(self, default_serializer, operation_result, **kwargs):
        output_serializer_class = self.get_output_serializer_class()

        if output_serializer_class:
            output_serializer = self.get_output_serializer(
                default_serializer,
                output_serializer_class,
                operation_result,
                **kwargs,
            )
            return output_serializer.data

        return default_serializer.data

    def get_output_serializer(
        self,
        default_serializer,
        output_serializer_class,
        operation_result,
        **kwargs,
    ):
        """
        Return the serializer instance that should be used for serializing output after POST request.
        """
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs.pop(self.lookup_field, None)
        return output_serializer_class(operation_result, **kwargs)

    def get_output_serializer_class(self):
        return self.output_serializer_class

    def get_status_code(self, response_data):
        status_code = status.HTTP_200_OK
        if self.request.method == "POST":
            status_code = status.HTTP_201_CREATED if response_data else status.HTTP_200_OK
        return status_code


class ExtendedCreateAPIView(QueryParamsMixin, InputOutputSerializerAPIView, CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_result = self.perform_create(serializer)
        return self.response(serializer, created_result, **kwargs)

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class ExtendedUpdateAPIView(QueryParamsMixin, InputOutputSerializerAPIView, UpdateAPIView):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_result = self.perform_update(serializer)
        return self.response(serializer, updated_result, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
