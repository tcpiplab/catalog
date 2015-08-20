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

 
# Create two decorators which will wrap our HelloWorld() function in Flask's
# app.route function. The app.route function will call HelloWorld() whenever
# the web server receives a request with a URL that matches either of these
# arguments. Thusly, we bind a function to a URL.
# The decorators work in sequence, a bit like hidden redirects to the next 
# route, ultimately resulting in the call to HelloWorld(). But they're not
# actually HTTP redirects. They're more like aliases.
@app.route('/')
@app.route('/hello')
def HelloWorld():
    # Call SQLalchemy to query the Restaurant table for the first restaurant.
    restaurant = session.query(Restaurant).first()
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


# If this file is called directly, i.e., not called as an include, run the code 
# through the Python interpreter.
if __name__ == '__main__':
    # With debug running, the Flask web server will reload itself each time 
    # it notices a code change. It also provides a debugger in the browser.
    app.debug = True

    # Run the local web server with our application.
    # Listen on all public IPs - required because we're running vagrant.
    app.run(host='0.0.0.0', port=5000)
