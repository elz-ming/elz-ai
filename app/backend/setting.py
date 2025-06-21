import os
import yaml
from pathlib import Path


def Setting() -> dict:
    env_name = os.getenv("APP_ENV", "dev").lower()
    config_path = Path(__file__).resolve(
    ).parents[2] / "env" / f"{env_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file '{config_path}' not found for env '{env_name}'")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config
