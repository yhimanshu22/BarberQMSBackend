from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your models here
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import all models to ensure they are registered with SQLAlchemy
from app.database import Base
from app.models import (
    User,
    Shop,
    Barber,
    Service,
    Appointment,
    Feedback,
    QueueEntry,
    BarberSchedule,
    barber_services
)

# this is the Alembic Config object
config = context.config

# Override sqlalchemy.url with environment variable
section = config.config_ini_section
config.set_section_option(section, "sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    print("The postgre url is: ", url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
