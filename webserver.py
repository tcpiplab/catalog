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
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
# Database ORM and engine:
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
# From our existing database:
from database_setup import Base, Restaurant, MenuItem


# Database connection code needs to run first:
# Specify which database engine to communicate with and which database file.
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the Base class. This connects our class definitions to
# their corresponding table in the database.
Base.metadata.bind = engine

# Create a sessionmaker object to establish a link of communications between 
# our code executions and the engine object created in the previous statement.
DBSession = sessionmaker(bind = engine)

# This is our session
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurant_list = queryAllRestaurants()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h4><ul>"
                # Iterate through the object. Output unordered HTML list of names
                for restaurant in restaurant_list:
                    output += "<li>"+ restaurant.name + "</li>"
                output += "</ul></h4>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
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
