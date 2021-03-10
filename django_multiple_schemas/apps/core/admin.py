from django.contrib import admin

from django_multiple_schemas.apps.core.models import Language
from django_multiple_schemas.support.django_helpers import CustomModelAdminMixin


@admin.register(Language)
class LanguageAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
