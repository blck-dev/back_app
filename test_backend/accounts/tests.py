from django.test import TestCase

# Create your tests here.
import pytest
from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class ClosepollTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        call_command("create_xof_asset", stdout=out)
        self.assertIn('Expected output', out.getvalue())

@pytest.mark.django_db
def test_get_no_args_endpoints(client):
    for endpoint in ["/.well-known/stellar.toml", "/info"]:
        print("GET IT --- ")
        assert client.get(endpoint).status_code == 200
