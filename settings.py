import environs

env = environs.Env()
env.read_env(".env")

SECRET_KEY = env("JWT_SECRET")
ALGORITHM = env("JWT_ALGORITHM")
TOKEN_EXPIRED_TIME = 1500

CONFIG = {
    "connections": {
    "default": env("DB_CONNECTION_URL")
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    }
}