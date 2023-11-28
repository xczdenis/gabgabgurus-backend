from enum import Enum

from django.db import models


class LanguageLevels(models.IntegerChoices):
    BEGINNER = 0, "Beginner"
    ELEMENTARY = 1, "Elementary"
    INTERMEDIATE = 2, "Intermediate"
    ADVANCED = 3, "Advanced"
    PROFICIENCY = 4, "Proficiency"
    NATIVE = 5, "Native"


class LanguageTypes(Enum):
    SPEAKS = "speaks"
    LEARNING = "learning"
