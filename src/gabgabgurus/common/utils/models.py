import re
from typing import Any, Iterable, Type, TypeVar

from django.db import IntegrityError, transaction
from django.db.models import Manager, Model

from gabgabgurus.common.decorators import default
from gabgabgurus.config import app_config
from gabgabgurus.config.exceptions import DBError, EntityDoesntExist

T = TypeVar("T")


def get_model_instance(value: Any, model: Type[T], slug_field: str = "pk") -> T:
    if isinstance(value, model):
        return value

    model_instance = model.objects.filter(**{slug_field: value}).first()
    if not model_instance:
        raise EntityDoesntExist(f"Such {model.__name__} does not exist")
    return model_instance


def get_qs_by_names(list_of_names: list[str], model: Type[T]) -> list[T]:
    return model.objects.filter(name__in=list_of_names)


def get_violation_error_message(error_message: str, model: Type[Model]) -> str:
    patterns = (
        "unique constraint",
        "check constraint",
    )
    for pattern in patterns:
        constraint_match = re.search(rf'{pattern} "(.+?)"', error_message)
        if constraint_match:
            constraint_name = constraint_match.group(1)

            for constraint in model._meta.constraints:
                if constraint.name == constraint_name:
                    return str(constraint.violation_error_message)

    return error_message


def save(obj: T) -> T:
    try:
        obj.save()
        return obj
    except IntegrityError as e:
        msg = get_violation_error_message(str(e), type(obj))
        raise DBError(msg)


def get_validators(model: Type[Model], field_name: str) -> Iterable:
    field = model._meta.get_field(field_name)
    return field.validators


@default(batch_size=app_config.BATCH_SIZE_FOR_BULK_ACTION)
def bulk_create(model: Type[T], objects: Iterable, **kwargs):
    objs = model.objects.bulk_create(objects, kwargs["batch_size"])
    return objs


def update_object_from_kwargs(obj: T, **kwargs) -> T:
    fields_to_update = get_fields_to_update(obj, **kwargs)
    with transaction.atomic():
        obj = update_object_fields(obj, kwargs, fields_to_update)
        save(obj)
    return obj


@default(batch_size=app_config.BATCH_SIZE_FOR_BULK_ACTION)
def bulk_update_objects_from_data(model: Type[Model], objs, data: dict, **kwargs):
    fields_to_update = get_fields_to_update(model, **data)
    updated_objects = (update_object_fields(obj, data, fields_to_update) for obj in objs)
    model.objects.bulk_update(updated_objects, fields_to_update, batch_size=kwargs["batch_size"])
    return objs


def get_fields_to_update(obj, **kwargs):
    return [field for field in kwargs.keys() if hasattr(obj, field)]


def update_object_fields(obj, data: dict, fields: Iterable):
    for field in fields:
        field_instance = getattr(obj, field)
        new_value = data[field]
        if isinstance(field_instance, Manager):
            field_instance.set(new_value)
        else:
            setattr(obj, field, new_value)
    return obj
