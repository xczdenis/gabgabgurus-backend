from gabgabgurus.common.utils.api import get_validated_data
from gabgabgurus.config.exceptions import BaseAppException


class AsyncSerializerMixin:
    serializer_class = None
    output_serializer_class = None

    async def get_validated_data(self, data, **kwargs):
        serializer_class = kwargs.get("serializer_class")
        if serializer_class is None:
            serializer_class = await self.get_serializer_class()
        return get_validated_data(serializer_class, data, **kwargs)

    async def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = await self.get_serializer_class()
        kwargs.setdefault("context", await self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    async def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        if self.serializer_class is None:
            raise BaseAppException(
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method." % self.__class__.__name__
            )

        return self.serializer_class

    async def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {"request": getattr(self, "request", None)}

    async def get_output_serialized_data(self, obj, **kwargs):
        if obj is None:
            return None

        kwargs.setdefault("context", await self.get_serializer_context())
        output_serializer = await self.get_output_serializer(obj, **kwargs)
        if output_serializer is None:
            return None

        return output_serializer.data

    async def get_output_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for serializing output.
        """
        serializer_class = await self.get_output_serializer_class()
        if serializer_class:
            return serializer_class(*args, **kwargs)

        return None

    async def get_output_serializer_class(self):
        return self.output_serializer_class
