from io import StringIO

import pytest

from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.mark.django_db
def test_should_do_nothing_when_seed_is_called_with_no_parameters():
    out = StringIO()
    call_command("seed", stdout=out)

    assert not out.getvalue()
    assert User.objects.filter(username="admin").count() == 0


@pytest.mark.django_db
def test_should_create_super_user_only():
    out = StringIO()
    call_command("seed", "--create-super-user", stdout=out)

    assert out.getvalue() == "Creating ADMIN username admin\n"
    assert User.objects.filter(username="admin").count() == 1
