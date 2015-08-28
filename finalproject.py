# Luke Sheppard
# lshep.usc[(at)]gmail.com
# August 28, 2015
#
# Fullstack Nanodegree at Udacity.com.
# Fullstack Foundations course, Final Project.

from flask import Flask, render_template, url_for, request, redirect, \
    flash, jsonify

# Create an instance of the Flask class with the name of the running application
# as the argument. 
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import the classes we created in database_setup.py
from database_setup import Base, Restaurant, MenuItem

# Database connection code needs to run first:
# Specify which database engine to communicate with and which database file.
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# Create a sessionmaker object to establish a link of communications between
# our code executions and the engine object created in the previous statement.
DBSession = sessionmaker(bind = engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit().
session = DBSession()


@app.route('/restaurant/JSON')
def allRestaurantsJSON():
    # An API endpoint for JSON GET requests for a list of all restaurants.
    '''
    For the URL:
    
        /restaurant/JSON
    
    return a JSON formatted structure containing the name and id of all 
    restaurants, sorted by name.
    '''

    # Call SQLalchemy to create an object containing a list of all rows in the 
    # Restaurant table, sorted by name.
    listOfRestaurants = session.query(
        Restaurant).order_by(Restaurant.name).all()

    # Iterate over the list, calling Restaurant.serialize(), 
    # wrap in flask.jsonify() for JSON output.
    return jsonify(MenuItem=[i.serialize for i in listOfRestaurants])


# If this file is called directly, i.e., not called as an import, run the code 
# through the Python interpreter.
if __name__ == '__main__':
    # Flask will use this key to create sessions for our users.
    app.secret_key = 'tB.IWZ3baukJ_'

    # With debug running, the Flask web server will reload itself each time 
    # it notices a code change. It also provides a debugger in the browser.
    app.debug = True

    # Run the local web server with our application.
    # Listen on all public IPs - required because we're running vagrant.
    app.run(host='0.0.0.0', port=5000)

