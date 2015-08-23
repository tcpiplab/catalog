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
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Make an API endpoint for JSON GET requests.
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    # Call SQLalchemy to query the Restaurant table by the restaurant_id arg.
    restaurant = session.query(Restaurant).filter_by(id=
        restaurant_id).one()

    # Call SQLalchemy to query for that restaurant's menu items.
    items = session.query(MenuItem).filter_by(restaurant_id=
        restaurant.id).all()

    return jsonify(MenuItems=[i.serialize for i in items])
 
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

    # Return a template (located in a dir called templates) and pass the 
    # queries so that the escape code in the template has access to the 
    # variables that will populate the template.
    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here
# Create a decorator from Flask.app.route() to bind newMenuItem with the URL
# /restaurants/<restaurant_id>/new/, allow GET or POST methods.
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    '''
    Handles GETs or POSTs to '/restaurants/<restaurant_id>/new/' and writes 
    the user's input to the database, after which, POSTs are redirected to the 
    menu page for the restaurant specified by the original restaurant_id 
    argument.
    
    Args: int restaurant_id
    '''
    # Given the numeric id of a restaurant, answer GETs or POSTs to this URL. 
    # For the latter, grab the user input and write it to the database.
    if request.method == 'POST':
        # Grab the user input from the HTML form.
        newItem = MenuItem(name = request.form['name'], restaurant_id = 
            restaurant_id)
        # Call SQLalchemy to stage the data to be written...
        session.add(newItem)
        # ... and now write the data to the DB.
        session.commit()
        # Alert the user.
        flash("New menu item created.")
        # Redirect the client to the menu page for this restaurant.
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id)
            )

    else:
        # Answer GETs by returning the newmenuitem.html file to the client.
        return render_template('newmenuitem.html', restaurant_id = 
            restaurant_id)


# Task 2: Create route for editMenuItem function here
# Create a decorator from Flask.app.route() to bind editMenuItem with the URL
# /restaurants/<restaurant_id>/<menu_id>/edit/, , allow GET or POST methods.
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=[
    'GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    '''
    Handles GETs or POSTs to '/restaurants/<restaurant_id>/<menu_id>/edit/' 
    and writes the user's input to the database, after which, POSTs are 
    redirected to the menu page for the restaurant specified by the original 
    restaurant_id argument.

    Args: int restaurant_id, int menu_id
    '''
    # Given the numeric ids of a restaurant and menu item, answer GETs or POSTs 
    # to this URL. For the latter, grab the user input and write it to the 
    # database. 
    # Use SQLalchemy to query the MenuItem table for our menu_id.
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        # Grab the user input from the HTML form.
        if request.form['name']:
            # Set the name attribute to the value from the form.
            editedItem.name = request.form['name']
        # Stage for writing to the DB.
        session.add(editedItem)
        # Write to the DB.
        session.commit()
        # Alert the user.
        flash("Menu item edited.")
        # Redirect the client to the menu page for this restaurant, building
        # the URL from that specified by the decorator of restaurantMenu().
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id)
            )
    else:
        # For GETs, return an edit page for that menu item.
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)




# Task 3: Create a route for deleteMenuItem function here
# Create a decorator from Flask.app.route() to bind deleteMenuItem with the URL
# /restaurants/<restaurant_id>/<menu_id>/delete/,  allow GET or POST methods.
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=[
    'GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    '''
    Handles GETs or POSTs to '/restaurants/<restaurant_id>/<menu_id>/delete/' 
    and deletes the specified menu item from the database, after which, POSTs 
    are redirected to the menu page for the restaurant specified by the original 
    restaurant_id argument.

    Args: int restaurant_id, int menu_id
    '''
    # Given the numeric ids of a restaurant and menu item, answer GETs or POSTs 
    # to this URL. For the latter, delete the corresponding record from the 
    # database. 
    # Use SQLalchemy to query the MenuItem table for our menu_id.
    deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        # Stage for persisting to the DB.
        session.delete(deletedItem)
        # Delete the record from the DB.
        session.commit()
        # Alert the user.
        flash("Menu item deleted.")
        # Redirect the client to the menu page for this restaurant, building
        # the URL from that specified by the decorator of restaurantMenu().
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id)
            )
    else:
        # For GETs, return an edit page for that menu item.
        return render_template('deletemenuitem.html', restaurant_id = 
            restaurant_id, menu_id = menu_id, i = deletedItem)



# If this file is called directly, i.e., not called as an include, run the code 
# through the Python interpreter.
if __name__ == '__main__':
    # Flash will use this key to create sessions for our users.
    app.secret_key = 'ylic9[,Tah'
    # With debug running, the Flask web server will reload itself each time 
    # it notices a code change. It also provides a debugger in the browser.
    app.debug = True

    # Run the local web server with our application.
    # Listen on all public IPs - required because we're running vagrant.
    app.run(host='0.0.0.0', port=5000)
