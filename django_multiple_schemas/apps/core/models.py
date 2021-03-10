from typing import List

from django.db import models


class StandardModelMixin(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Language(StandardModelMixin):
    # https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md
    # One example that might be applicable: en-gb-scotland
    language_tag = models.CharField(max_length=20, null=False, blank=False, unique=True)
    # Language: English
    # Accent/Dialect: Scottish
    # Language Family: West Germanic
    language = models.CharField(max_length=50, null=True, blank=True, verbose_name="Language")
    accent_or_dialect = models.CharField(max_length=50, null=True, blank=True, verbose_name="Accent/Dialect")
    family = models.CharField(max_length=50, null=True, blank=True, verbose_name="Family")

    def __str__(self):
        return self.language_tag
