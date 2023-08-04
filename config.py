import os

from dotenv import load_dotenv


def load_environment_variables() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
