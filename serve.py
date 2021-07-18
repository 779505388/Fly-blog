from app import create_app
from config import DevConfig
from flask_cors import CORS


app = create_app(DevConfig)
app.jinja_env.auto_reload = True

CORS(app, resources={
     r"/api/*": {"origins": "*"}}, supports_credentials=True)
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
