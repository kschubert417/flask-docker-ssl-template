import logging
from logging.config import fileConfig
import os
import sys

from alembic import context
from flask import current_app

# --- Ensure project root (/app) is importable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Alembic config and logging ---
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# --- Flask app setup ---
try:
    # Works when Alembic is invoked via Flask-Migrate (flask db ...)
    target_db = current_app.extensions["migrate"].db
    config.set_main_option("sqlalchemy.url", str(target_db.engine.url))
    logger.info("Running Alembic with active Flask app context.")
except Exception:
    # Works when Alembic runs directly in Docker or from CLI
    logger.info("No Flask app context detected — creating app manually.")
    from app import create_app
    from app.config import ProdConfig, DevConfig, TestConfig

    # Match wsgi.py’s logic
    env = os.getenv("FLASK_ENV", "production")
    config_map = {
        "development": DevConfig,
        "test": TestConfig,
        "production": ProdConfig,
    }

    config_class = config_map.get(env, ProdConfig)
    app = create_app(config_class)
    app.app_context().push()

    from app import db
    config.set_main_option("sqlalchemy.url", str(db.engine.url))
    target_db = db

# --- Metadata helper ---
def get_metadata():
    if hasattr(target_db, "metadatas"):
        return target_db.metadatas[None]
    return target_db.metadata

# --- Migration functions ---
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    migrate_ext = getattr(current_app, "extensions", {}).get("migrate") if current_app else None
    conf_args = getattr(migrate_ext, "configure_args", {}) or {}

    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = target_db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args,
        )

        with context.begin_transaction():
            context.run_migrations()



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
