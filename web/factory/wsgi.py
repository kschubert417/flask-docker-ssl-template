import os
from app import create_app
from app.config import ProdConfig, DevConfig, TestConfig

env = os.environ.get("FLASK_ENV", "production")

config_map = {
    "development": DevConfig,
    "test": TestConfig,
    "production": ProdConfig
}

# app = create_app(ProdConfig)
print("====================================================")
print(f"=============== Running in {env} environment ======")
print("====================================================")
app = create_app(config_map[env])
