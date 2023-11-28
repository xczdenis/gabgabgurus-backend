import random
from typing import Generator, Iterable, Type

from django.db.models import Model


# @timer
def make_objects_by_names(model: Type[Model], names: Iterable[str]) -> list[Model]:
    return [model(name=name) for name in names]


# @timer
def save_objects(model: Type[Model], objects: Iterable[Model], batch_size: int = 5000):
    model.objects.bulk_create(objects, batch_size=batch_size, ignore_conflicts=True)


# @timer
def delete_objects(model: Type[Model], objects: Iterable[Model] | None = None):
    if objects is None:
        model.objects.all().delete()
    else:
        model.objects.filter(pk__in=[obj.pk for obj in objects]).delete()


def get_random_objects(model: Type[Model]) -> Generator[Type[Model], None, None]:
    objects = list(model.objects.all())
    random.shuffle(objects)
    for item in objects:
        yield item


def get_next_object(generator):
    try:
        return next(generator)
    except StopIteration:
        return None
