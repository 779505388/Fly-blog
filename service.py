from app import create_app
from config import DevConfig
from flask_cors import CORS
from logging.handlers import TimedRotatingFileHandler
import logging

app = create_app(DevConfig)
app.jinja_env.auto_reload = True
CORS(app, resources={r"/api/*": {"origins": "*"}})
if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "FlyBlog.log", when="D", interval=15, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    app.run(host="0.0.0.0", port=8080)
