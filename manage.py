from flask.ext import script
from flask.ext import migrate

import pantry
import pantry.manage.seed as seed

APP = pantry.create_app('pantry.cfg')
MGR = script.Manager(APP)
MGR.add_command('db', migrate.MigrateCommand)
MGR.add_command('seed', seed.SeedDatabase)

if __name__ == "__main__":
    MGR.run()
