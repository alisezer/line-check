"""Entry point"""

from flask_migrate import Migrate, upgrade

import os

from lc.main import create_app, db
from lc.schedule import run_scheduler

app = create_app()
migrate = Migrate(app, db)

@app.cli.command()
def deploy():
    upgrade()

@app.cli.command()
def scheduled():
    run_scheduler()