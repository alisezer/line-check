"""Holds configuration and environment variables"""

from environs import Env

# Read environment variables
env = Env()
env.read_env()


# Database configurations
DB_HOST = env.str('DB_HOST', 'localhost')
DB_PORT = env.int('DB_PORT', 5432)
DB_NAME = env.str('DB_DB', 'linecheck')
DB_USER = env.str('DB_USER', 'deploy')
DB_PASSWORD = env.str('DB_PASSWORD', 'docker')
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True

# Gunicorn configurations
WORKERS = env.int('WORKERS', 3)
THREADS = env.int('THREADS', 5)
PORT = env.int('PORT', 8000)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s.%(msecs)03d [%(process)d] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        # used only in local environment
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        # Werkzeug level set to Warning
        'werkzeug': {
            'level': 'WARN',
        },
        'lc': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}