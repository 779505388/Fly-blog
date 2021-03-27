from flask_script import Manager
from app import create_app
from flask_migrate import Migrate, MigrateCommand
from extension import db
from config.config import DevConfig
from models.Content import Article, Tag, Category
from models.User import User
from models.Commet import Comment
from models.Other import PyLink
app = create_app(DevConfig)
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
