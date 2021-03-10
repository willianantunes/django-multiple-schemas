import pytest

from django_multiple_schemas.apps.core.models import Language
from tests.support.models_utils import create_language


@pytest.mark.django_db
def test_should_create_languages():
    lang_1, lang_2 = "en-us", "en-gb"

    persisted_lang_1, persisted_lang_2 = create_language(lang_1), create_language(lang_2)

    assert persisted_lang_1.language_tag == lang_1
    assert persisted_lang_2.language_tag == lang_2
    assert Language.objects.count() == 2
