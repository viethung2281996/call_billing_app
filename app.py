import os
from flask_migrate import Migrate
from dotenv import load_dotenv
from src import create_app, db


load_dotenv()

app = create_app(flask_env=os.getenv('FLASK_ENV', 'development'))
alembic_migrate = Migrate(app, db)
