import os
from flask import Flask
from web.routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

app.config.update(
    SAVE_DIR = os.getenv("HEX_SAVE_DIR", "games"),
    MAX_SIZE = int(os.getenv("HEX_MAX_SIZE", 13)),
)


if __name__ == "__main__":
    app.run(debug=True)
