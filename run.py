from app import app
from config import DEBUG, PORT

from source.utils.db import db

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(
        debug = DEBUG,
        port = PORT
    )