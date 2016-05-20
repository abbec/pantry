import flask
from flask.ext import script
import pantry

import pantry.db.fake as fake
import pantry.db.targets as dbtargets

from pantry.db import db as database


class SeedDatabase(script.Command):  # pylint:disable=too-few-public-methods

    def run(self):  # pylint:disable=no-self-use
        print("seeding database...")
        app = pantry.create_app("pantry.cfg")

        with app.app_context():
            database.init_app(flask.current_app)

            database.reflect()
            database.drop_all()
            database.create_all()

            # targets
            database.engine.execute(
                dbtargets.targets_table.insert(),
                fake.create_targets(100))

        print("done!")
