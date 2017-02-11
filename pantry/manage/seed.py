import flask
import flask_script as script

import pantry.fake as fake
import pantry.v1.backend as backend


class SeedDatabase(script.Command):  # pylint:disable=too-few-public-methods
    "Seeds database with mock data"

    def run(self):  # pylint:disable=no-self-use,method-hidden
        print("seeding database...")

        backend.init(flask.current_app)
        backend.clear()
        backend.db.create_all()

        # targets
        for t in fake.create_targets(100):
            backend.create_target(t)

        # some tags
        # todo

        # leases
        # todo
        print("done!")
