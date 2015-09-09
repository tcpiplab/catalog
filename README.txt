Luke Sheppard
lshep.usc{(at)}gmail.com
Full Stack Foundations course
Udacity Full Stack Nanodegree
September 8, 2015

This directory contains all files related to assignments from the Udacity.com 
course entitled Full Stack Foundations, a required course for the Full Stack 
Nanodegree. See the FILES section, below.


HOW TO RUN THIS WEB APPLICATION
Any version of Python 2 should work, but this project was created with 2.7.9.

1. SET UP THE VAGRANT ENVIRONMENT
  Although you could install PostgreSQL and SQLalchemy yourself, it is 
  preferable for you to instead install the Vagrant virtual machine supplied 
  in the Udacity course materials for this nanodegree. See Installing the 
  Vagrant VM for Full Stack Foundations:

    https://www.udacity.com/wiki/ud088/vagrant

  Navigate to the directory containing the Vagrantfile file you cloned, start
  the Vagrant VM, SSH to it, navigate to the directory containing the catalog 
  directory:

    cd fullstack/vagrant (depending on where you saved it)
    vagrant up
    vagrant ssh
    cd catalog (depending on where you cloned this dir)

2. BUILD THE DATABASE
  Run database_setup.py to create the database:

    python database_setup.py

3. POPULATE THE DATABASE
  Run lotsofmenus.py to populate the database:

    python lotsofmenus.py

4. RUN THE FLASK WEBSERVER LOCALLY
  Run finalproject.py:

    python finalproject.py

  Navigate to http://localhost:5000 in your browser:

    open http://localhost:5000 (Mac OS X)
    start "link" "http://localhost:5000" (Microsoft Windows)
    xdg-open http://localhost:5000 (Linux)
    

FILES
  database_setup.py
    Defines the database tables as Python classes for SQLalchemy.

  doc/
    Planning documents and diagrams.

  finalproject.py
    The final project for this course (this is not "P3"), using Flask and
    SQLalchemy.

  lotsofmenus.py
    A script written by Udacity for populating the database.

  project.py
    The 2nd project for this course, a subset of the final project, using Flask
    and SQLalchemy.

  static/
    A directory for CSS, optionally images too.

  templates/
    All HTML templates used by Flask.

  webserver.py
    The 1st project for this course, as subset of the final project, using
    SQLalchemy, but no Flask. Instead, it uses Python's BaseHTTPServer module
    to implement a basic HTTP server, handling GETs and POSTs with specific
    URLs handled via BaseHTTPServer.BaseHTTPRequestHandler.path.endswith().

