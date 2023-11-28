import random

from django.contrib.auth import get_user_model
from faker import Faker

from gabgabgurus.api.v1.fake.utils import delete_objects, get_next_object, get_random_objects, save_objects
from gabgabgurus.apps.languages.enums import LanguageLevels
from gabgabgurus.apps.languages.models import Language
from gabgabgurus.apps.user_details.models import UserLanguage

User = get_user_model()

fake = Faker()


# @timer
def generate_user_language(n: int):
    """"""
    model_objects = {
        UserLanguage: [],
    }

    for model in model_objects:
        delete_objects(model)

    def get_proficiency():
        return random.choice(list(LanguageLevels.choices))[0]  # noqa: S311

    users = get_random_objects(User)
    languages = get_random_objects(Language)

    for _ in range(n):
        user = get_next_object(users)
        language = get_next_object(languages)
        proficiency = get_proficiency()

        if not user:
            users = get_random_objects(User)
            user = get_next_object(users)

        if not language:
            languages = get_random_objects(Language)
            language = get_next_object(languages)

        for model in model_objects:
            fake_object = model()
            fake_object.user = user
            fake_object.language = language
            fake_object.proficiency = proficiency
            fake_object.is_learning = fake.boolean()
            fake_object.is_speaking = fake.boolean()
            model_objects[model].append(fake_object)

    for model, objects in model_objects.items():
        save_objects(model, objects, 10000)

    created = UserLanguage.objects.count()

    return created
