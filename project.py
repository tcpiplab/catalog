from flask import Flask
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
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

 
# Create a decorator which will wrap our restaurantMenu() function in Flask's
# app.route function. The app.route function will call restaurantMenu() whenever
# the web server receives a request with a URL that matches the argument. 
# Thusly, we bind a function to a URL.
# Note that the trailing slash will allow inbound URLs with or without a 
# trailing slash. A URL without it will be "redirected" (not HTTP redirect) 
# to the path with it. See http://flask.pocoo.org/docs/0.10/quickstart/#routing
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # Call SQLalchemy to query the Restaurant table by the restaurant_id arg.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # Call SQLalchemy to query for that restaurant's menu items.
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    # Store the outputed HTML in a string called output.
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    # Return output to Flask, which will send it to the client.
    return output


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


# If this file is called directly, i.e., not called as an include, run the code 
# through the Python interpreter.
if __name__ == '__main__':
    # With debug running, the Flask web server will reload itself each time 
    # it notices a code change. It also provides a debugger in the browser.
    app.debug = True

    # Run the local web server with our application.
    # Listen on all public IPs - required because we're running vagrant.
    app.run(host='0.0.0.0', port=5000)
