from polaris.models import Asset
import os
import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve()

env_file = os.path.join("", ".env.local")

if os.path.exists(env_file):
    print("we got env working!!")
    env.read_env(env_file)
    print(env("ASSETS"))

Asset.objects.create(
    code=env("ASSETS"),
    issuer=env("ISSUER_PUBLIC_KEY"),
    distribution_seed=env("DISTRIBUTION_SECRET_KEY"),
    sep24_enabled=True,
    sep6_enabled=True,
    withdrawal_enabled=True,
    deposit_enabled=True
)
