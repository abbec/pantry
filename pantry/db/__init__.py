import flask_sqlalchemy as sqlalchemy
import flask_migrate as migrate

db = sqlalchemy.SQLAlchemy()
migrate = migrate.Migrate()
