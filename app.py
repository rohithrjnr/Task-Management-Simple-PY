from flask import Flask
from flask_cors import CORS
from models import db
from routes import task_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 
    app.register_blueprint(task_routes)  

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
