"""This module is used to run the app"""
from flaskblog import create_app   # Imports the __init__ module from the package 'flaskblog'

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
