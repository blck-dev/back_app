from django.core.management.base import BaseCommand, CommandError
from polaris.models import Asset
import os
import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_file = os.path.join(BASE_DIR, "environ/.env.local")
if os.path.exists(env_file):
    print("we got env working!!")
    env.read_env(env_file)
    print(env("ASSETS"))


class Command(BaseCommand):
    help = 'Create an asset  with polaris Asset model'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            if not Asset.objects.filter(code="XOF").exists():
                Asset.objects.create(
                    code=env("ASSETS"),
                    issuer=env("ISSUER_PUBLIC_KEY"),
                    distribution_seed=env("DISTRIBUTION_SECRET_KEY"),
                    sep24_enabled=True,
                    sep6_enabled=True,
                    withdrawal_enabled=True,
                    deposit_enabled=True
                )
                self.stdout.write(self.style.SUCCESS('Successfully created XOF asset'))
            else:
                self.stdout.write(self.style.SUCCESS('XOF asset already exist'))
        except:
            self.stdout.write(self.style.SUCCESS('Unable to create XOF asset'))
