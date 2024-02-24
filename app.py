from flask import Flask
from views.user_view import user
from database.__init__ import database
from views.verb_view import verb_blueprint
import requests


#pip install flask

app = Flask(__name__)
 
app.register_blueprint(user)
app.register_blueprint(verb_blueprint)


print("DATABASE CONNECTION -> ", database.dbConnection)

@app.route("/")
def index():
    return "HOME"

if __name__ == "__main__":
    app.run(debug=True)

#flask --app app run
# x-access-token
