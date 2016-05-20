import pantry

from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
import pantry.manage.seed as seed

application = pantry.create_app('pantry.cfg')
manager = Manager(application)
manager.add_command('db', MigrateCommand)
manager.add_command('seed', seed.SeedDatabase)

if __name__ == "__main__":
    manager.run()

