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


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    # An API endpoint for JSON GET requests per restaurant.
    '''
    For the URL:

        /restaurant/<int:restaurant_id>/menu/JSON

    return a JSON formatted structure containing that specific restaurant's
    menu.
    Args:
        int restaurant_id
    '''
    # Call SQLalchemy to query the Restaurant table by the restaurant_id arg.
    restaurant = session.query(Restaurant).filter_by(id=
        restaurant_id).one()

    # Call SQLalchemy to query for that restaurant's menu items.
    items = session.query(MenuItem).filter_by(restaurant_id=
        restaurant.id).all()

    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    # An API endpoint for JSON GET requests per menu item.
    '''
    For the URL:

        /restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON

    return a JSON formatted structure containing that specific menu item's
    data..
    Args:
        int restaurant_id
        int menu_id
    '''
    # Call SQLalchemy to query the MenuItem table by the menu_id arg.
    theMenuItem = session.query(MenuItem).filter_by(id = menu_id).all()

    return jsonify(MenuItem=[i.serialize for i in theMenuItem])


@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    # Display a specific restaurant's menu populating an HTML template.
    # Or return nomenu.html if the menu is empty.
    '''
    For the URL:

        /restaurant/<int:restaurant_id>/

    return an HTML template populated with the menu for that specific
    restaurant. Or return nomenu.html if the menu is empty.
    Args:
        int restaurant_id
    '''
    # Call SQLalchemy to query the Restaurant table by the restaurant_id arg.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    # Call SQLalchemy to query for that restaurant's menu items.
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    # If this restaurant's menu is not empty
    if (len(items.all()) > 0):
        # Return a template (located in a dir called templates) and pass the
        # queries so that the escape code in the template has access to the
        # variables that will populate the template.
        return render_template('menu.html', restaurant=restaurant, items=items)
    else:
        # Return our "there is no menu" page.
        return render_template('nomenu.html', restaurant=restaurant)


# Create a decorator from Flask.app.route() to bind newMenuItem with the URL
# /restaurant/<restaurant_id>/new/, allow GET or POST methods.
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    # Handle creation of new menu items in the database.
    # Answer POSTs by writing user input to the database.
    # Answer GETs by returning the newmenuitem.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurant/<restaurant_id>/new/

    and writes the user's input to the database, after which, POSTs are
    redirected to the menu page for the restaurant specified by the original
    restaurant_id argument.

    Args:
        int restaurant_id
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
        return redirect(url_for('showMenu', restaurant_id = restaurant_id)
            )

    else:
        # Answer GETs by returning the newmenuitem.html file to the client.
        return render_template('newmenuitem.html', restaurant_id =
            restaurant_id)


# Create a decorator from Flask.app.route() to bind editMenuItem with the URL
# /restaurant/<restaurant_id>/<menu_id>/edit/, , allow GET or POST methods.
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=[
    'GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    # Handle updates to existing menu items in the database.
    # Answer POSTs by writing user input to the database.
    # Answer GETs by returning the editmenuitem.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurant/<restaurant_id>/<menu_id>/edit/

    and writes the user's input to the database, after which, POSTs are
    redirected to the menu page for the restaurant specified by the original
    restaurant_id argument. GETs simply return a populated template named
    editmenuitem.html.

    Args:
        int restaurant_id
        int menu_id
    '''
    # Use SQLalchemy to query the MenuItem table for our menu_id.
    editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        # Grab the user input from the HTML form.
        if request.form['name']:
            # Set the name attribute to the value from the form.
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']

        # Stage for writing to the DB.
        session.add(editedItem)
        # Write to the DB.
        session.commit()
        # Alert the user.
        flash("Menu item edited.")
        # Redirect the client to the menu page for this restaurant, building
        # the URL from that specified by the decorator of showMenu().
        return redirect(url_for('showMenu', restaurant_id = restaurant_id)
            )
    else:
        # For GETs, return an edit page for that menu item.
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=[
    'GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # Handle deletions of existing menu items in the database.
    # Answer POSTs by deleting the row in the MenuItem table of the database
    # which the user specified with two numeric arguments.
    # Answer GETs by returning the deletemenuitem.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurants/<restaurant_id>/<menu_id>/delete/

    and deletes the specified menu item from the database, after which, POSTs
    are redirected to the menu page for the restaurant specified by the
    original restaurant_id argument. GETs simply return a populated template
    named deletemenuitem.html.

    Args:
        int restaurant_id
        int menu_id
    '''
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
        # the URL from that specified by the decorator of showMenu().
        return redirect(url_for('showMenu', restaurant_id = restaurant_id)
            )
    else:
        # For GETs, return an edit page for that menu item.
        return render_template('deletemenuitem.html', restaurant_id =
            restaurant_id, menu_id = menu_id, i = deletedItem)


@app.route('/restaurant/')
@app.route('/')
def showRestaurants():
    """
    Query the Restaurant table and return an object containing the restaurant
    names sorted alphabetically.
    """
    # Create an object containing a list of all rows in the Restaurant table,
    # and sort by name.
    restaurant_names = session.query(Restaurant).order_by(Restaurant.name).all()

    return render_template('restaurants.html', restaurant_names = restaurant_names)

# Create a decorator from Flask.app.route() to bind newRestaurant with the URL
# /restaurant/new/, allow GET or POST methods.
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    # Handle creation of new restaurants in the database.
    # Answer POSTs by writing user input to the database.
    # Answer GETs by returning the newmenuitem.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurant/new/

    and writes the user's input to the database, after which, POSTs are
    redirected to the restaurants.html page listing all restaurants.

    Args:
        None.
    '''
    # Answer GETs or POSTs to this URL.
    # For the latter, grab the user input and write it to the database.
    if request.method == 'POST':
        # Grab the user input from the HTML form.
        newRestaurant = Restaurant(name = request.form['name'])
        # Call SQLalchemy to stage the data to be written...
        session.add(newRestaurant)
        # ... and now write the data to the DB.
        session.commit()
        # Alert the user.
        flash("New restaurant created.")
        # Redirect the client to the menu page for this restaurant.
        return redirect(url_for('showRestaurants'))

    else:
        # Answer GETs by returning the newrestaurant.html file to the client.
        return render_template('newrestaurant.html')

# Create a decorator from Flask.app.route() to bind editRestaurant with the URL
# /restaurant/<restaurant_id>/edit/, , allow GET or POST methods.
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    # Handle updates to existing restaurants in the database.
    # Answer POSTs by writing user input to the database.
    # Answer GETs by returning the editrestaurant.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurant/<restaurant_id>/edit/

    and writes the user's input to the database, after which, POSTs are
    redirected to the name edit page for the restaurant specified by the
    original restaurant_id argument. GETs simply return a populated template
    named editrestaurant.html.

    Args:
        int restaurant_id
    '''
    # Call SQLalchemy to query the Restaurant table by the restaurant_id arg.
    #this_restaurant = session.query(Restaurant).filter_by(id=
    #    restaurant_id).one()
    #return render_template('editrestaurant.html', restaurant_id = this_restaurant.id)

    # Use SQLalchemy to query the Restaurant table for our restaurant_id.
    editedRestaurant = session.query(Restaurant).filter_by(
        id = restaurant_id).one()
    if request.method == 'POST':
        # Grab the user input from the HTML form.
        if request.form['name']:
            # Set the name attribute to the value from the form.
            editedRestaurant.name = request.form['name']
        # Stage for writing to the DB.
        session.add(editedRestaurant)
        # Write to the DB.
        session.commit()
        # Alert the user.
        flash("Restaurant name edited.")
        # Redirect the client to the page showing all restaurants.
        return redirect(url_for('showRestaurants', restaurant_id = restaurant_id)
            )
    else:
        # For GETs, return an edit page for that restaurant.
        return render_template('editrestaurant.html',
            restaurant_id = restaurant_id, i = editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    # Handle deletions of existing restaurants in the database.
    # Answer POSTs by deleting the row in the Restaurant table of the database
    # which the user specified with a numeric argument.
    # Answer GETs by returning the deleterestaraunt.html file to the client.
    '''
    Handles GETs or POSTs to the URL:

        /restaurants/<restaurant_id>/delete/

    and deletes the specified restaurant from the database, after which, POSTs
    are redirected to the restaurants.html page listing all restaurants.
    GETs simply return a populated template named deleterestaraunt.html.

    Args:
        int restaurant_id
    '''
    # Use SQLalchemy to query the Restaurant table for our restaurant_id.
    deletedRestaurant = session.query(Restaurant).filter_by(
        id = restaurant_id).one()
    if request.method == 'POST':
        # Stage for persisting to the DB.
        session.delete(deletedRestaurant)
        # Delete the record from the DB.
        session.commit()
        # Alert the user.
        flash("Restaurant deleted.")
        # Redirect the client to the restaurants.html page listing all
        # restaurants.
        return redirect(url_for(
            'showRestaurants', restaurant_id = restaurant_id))
    else:
        # For GETs, return an edit page for that restaurant.
        return render_template('deleterestaraunt.html', restaurant_id =
            restaurant_id, i = deletedRestaurant)


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
