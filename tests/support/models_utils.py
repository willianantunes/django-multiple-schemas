from django_multiple_schemas.apps.core.models import Language


def create_language(language_tag):
    return Language.objects.create(language_tag=language_tag)
