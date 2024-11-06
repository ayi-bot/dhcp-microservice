import importlib
import os
import pkgutil

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

if not os.environ.get("DATABASE_URL"):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_mode = os.environ.get("ENV", "development")
    dotenv_filename = f"{env_mode}.env"
    dotenv_path = os.path.join(project_root, 'environments', dotenv_filename)
    load_dotenv(dotenv_path)

url = os.environ.get("DATABASE_URL")

if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

engine = create_engine(url, echo=True)

def create_db_and_tables():
    import_models("app.models")
    SQLModel.metadata.create_all(engine)

def import_models(package_name):
    package = importlib.import_module(package_name)
    for module_info in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package_name}.{module_info.name}")
