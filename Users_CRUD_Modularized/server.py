from flask_app import app

from flask_app.models.user import User
import flask_app.controllers.users 

            
if __name__ == "__main__":
    app.run(debug=True)