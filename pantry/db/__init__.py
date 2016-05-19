import flask.ext.sqlalchemy as sqlalchemy
import flask.ext.migrate as migrate

db = sqlalchemy.SQLAlchemy()
migrate = migrate.Migrate()
