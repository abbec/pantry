import flask
import flask_script as script
import pantry

import pantry.db.fake as fake
import pantry.db.targets as dbtargets
import pantry.db.leases as dbleases

from pantry.db import db as database


class SeedDatabase(script.Command):  # pylint:disable=too-few-public-methods
    "Seeds database with mock data"

    def run(self):  # pylint:disable=no-self-use,method-hidden
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

            # leases
            database.engine.execute(
                dbleases.leases_table.insert(),
                fake.create_leases(1000))

            # todo: set up relations

        print("done!")
