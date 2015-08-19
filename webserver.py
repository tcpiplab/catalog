# Luke Sheppard
# lshep.usc[(at)]gmail.com
# August 11, 2015

# Fullstack Nanodegree at Udacity.com.
# Fullstack Foundations course
# Lesson 2, Restaurant menu website
# Objectives:
# 1. Opening http://localhost:8080/restaurants lists all the restaurant names
#    in the database.
# 2. After the name of each database there is a link to edit and delete each
#    restaurant.
# 3. There is a page to create new restaurants at
#    http://localhost:8080/restaurants/new with a form for creating a new
#    restaurant.
# 4. Users can rename a restaurant by visiting
#    http://localhost:8080/restaurant/id/edit.
# 5. Clicking 'delete' takes a user to a confirmation page that then sends a
#    POST command to the database to delete the selected restaurant.


# Dependencies
# Web server:
# https://docs.python.org/2/library/basehttpserver.html
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# https://docs.python.org/2/library/cgi.html
import cgi
# Database ORM and engine:
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# http://docs.sqlalchemy.org/en/latest/orm/internals.html
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
# From our existing database:
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


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # From the BaseHTTPServer.BaseHTTPRequestHandler class, path is an
            # instance variable containing the request path.
            #
            # Inherited from the sqlalchemy.sql.operators.ColumnOperators class,
            # the endswith() method, in a column context, produces the SQL 
            # clause LIKE '%whatever>'.
            if self.path.endswith("/restaurants"):
                # Call the method that uses SQLalchemy to do the query.
                restaurant_list = queryAllRestaurants()

                # Answer the HTTP GET with HTTP headers.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Finish answering the HTTP GET with HTML.
                output = ""
                output += "<html><body>"

                # Objective 3 Step 1 - Create a Link to create a new menu item
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                output += "<h4><ul>"

                # Iterate through the object. Output unordered HTML list of names
                for restaurant in restaurant_list:
                    output += "<li>"
                    output += restaurant.name
                    output += "&nbsp;&nbsp;"
                    output += "<small>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "&nbsp;&nbsp;"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>"
                    output += "</small>"
                    output += "</li>"
                output += "</ul></h4>"
                output += "</body></html>"

                # From the BaseHTTPServer.BaseHTTPRequestHandler() class, wfile
                # is an instance variable that contains the output stream for 
                # writing a response back to the client. Proper adherence to the
                # HTTP protocol must be used when writing to this stream.
                #
                # We're calling the write() file object method to write a string
                # to the wfile file. There is no return value. Due to buffering,
                # the string may not actually show up in the file until the 
                # flush() or close() method is called. See
                # https://docs.python.org/2/library/stdtypes.html#file-objects
                self.wfile.write(output)
                return

            # Create a handler for the Edit page.
            if self.path.endswith("/edit"):
                # Grab the id number of the link they clicked. It is the third
                # element of an indexed array created from the path.
                restaurantIDPath = self.path.split("/")[2]

                # Use SQLalchemy to query the id column of the Restaurant table
                # and set a variable to that value.
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                # If the query returned a value
                if myRestaurantQuery != [] :
                    # Send the response headers and HTML.
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h2>"
                    output += myRestaurantQuery.name
                    output += "</h2>"
                    # Create a POST url link containing the restaurant id.
                    # We define a do_POST handler for it below.
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath

                    # newRestaurantName will contain the user input. The HTML
                    # placholder attribute is a short hint that is displayed in 
                    # the input field before the user enters a value. Set it to
                    # the current name of the restaurant.
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    # Send it all to the client
                    self.wfile.write(output)

             # A confirmation page for deletions
             if self.path.endswith("/delete"):
                # Grab the restaurant ID from the URL they clicked.
                restaurantIDPath = self.path.split("/")[2]

                # Use SQLalchemy to query for that restaurant ID.
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()

                # If the query returned data, send HTTP headers and HTML.
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    # Output the restaurant name we retrieved.
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    # Make the form POST URL contain the ID in the path.
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    # Output the headers and HTML to the client.
                    self.wfile.write(output)


            # Objective 3 Step 2 - Create /restarants/new page
            # Create a page for adding new restaurants to the database.
            # path.endswith() is explained in previous comments.
            if self.path.endswith("/restaurants/new"):
                # See the previous if() block for additional relevant comments.
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2>"

                # Our do_GET handler for /restaurants/new/ needs to send HTML 
                # for a link to a POST at the same address, which will be 
                # handled in do_POST, below.
                output += "<form method = 'POST' enctype='multipart/form-data'  action = '/restaurants/new'>"

                # newRestaurantName contains the user input our POST will need.
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

        # IOError is an exception type external to Python, from the 
        # EnvironmentError class. Raised when an I/O operation (such as a print 
        # statement, the built-in open() function or a method of a file object) 
        # fails for an I/O-related reason, e.g., "file not found" or "disk full".
        # https://docs.python.org/2/library/exceptions.html#exceptions.IOError.
        except IOError:
            # From the BaseHTTPRequestHandler class, the send_error() method
            # sends and logs a complete error reply to the client. The HTTP 
            # error code is mandatory; the message is optional.
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            # Handle POSTS to the restaurants/delete URL.
            if self.path.endswith("/delete"):
                # Grad the id from the inbound URL.
                restaurantIDPath = self.path.split("/")[2]

                # SQLalchemy query to grab that restaurant's ID from the DB.
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()

                # If the query returned data, output HTTP redirect to home page. 
                if myRestaurantQuery:
                    # SQLalchemy query to delete the restaurant by ID.
                    session.delete(myRestaurantQuery)
                    # Write to the database.
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # Handle POSTs to the restaurants/new URL.
            if self.path.endswith("/restaurants/new"):
                # cgi.parse_header() Parse a MIME header (such as Content-Type) 
                # into a main value and a dictionary of parameters.
                # Here ctype means Content-Type, not to be confused with ctypes,
                # and pdict is a dictionary of parameters.
                ctype, pdict = cgi.parse_header(
                    # The headers object is an instance variable of the 
                    # BaseHTTPRequestHandler class.
                    # The getheaders() method seems to come from the 
                    # httplib.HTTPResponse class. If so, I can't find how 
                    # it is inherited. 
                    # https://docs.python.org/2/library/httplib.html
                    self.headers.getheader('content-type'))

                # If the content-type header is multipart/form-data,
                if ctype == 'multipart/form-data':
                    # The arguments to cgi.parse_multipart(): rfile is the input
                    # file; pdict is a dictionary containing other parameters in
                    # the Content-Type header.
                    #
                    # The fields object will be a dictionary. The keys are the 
                    # field names. Each value is a list of values for that field.
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    # Grab the user input from the HTML form. Call the built-in
                    # dictionary function get(). It will return the value for 
                    # the 'newRestaurantName' key if it is in the dictionary.
                    # messagecontent will be a list containing one item.
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object w/ SQLalchemy
                    # Set name to the value of the first/only item in the list.
                    newRestaurant = Restaurant(name=messagecontent[0])
                    
                    # Stage the new object.
                    session.add(newRestaurant)
                    # Write it to the restaurantmenu.db database, as defined in 
                    # the database_setup.Restaurant class. Specifically, create
                    # a new row in the Restaurant table, writing the value of 
                    # messagecontent[0] to the name column.
                    session.commit()

                    # Send the response headers, redirecting the client back to
                    # the page listing all restaurants.
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # Create a handler for POSTs to /restaurants/edit.
            # Similar code is commented above.
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                if myRestaurantQuery != [] :
                    myRestaurantQuery.name = messagecontent[0]
                    # SQLalchemy query to INSERT newRestaurantName into DB.
                    session.add(myRestaurantQuery)
                    # Write to the database.
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


# Objective 1
def queryAllRestaurants():
    """
    Query the Restaurant table and return an object containing the restaurant
    names sorted alphabetically.
    """
    # Create an object containing a list of all rows in the Restaurant table,
    # and sort by name.
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()

    return restaurants


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
