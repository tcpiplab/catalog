from flask import Flask

# Create an instance of the Flask class with the name of the running application
# as the argument. 
app = Flask(__name__)
 
# Create two decorators which will wrap our HelloWorld() function in Flask's
# app.route function. The app.route function will call HelloWorld() whenever
# the web server receives a request with a URL that matches either of these
# arguments.
# The decorators work in sequence, a bit like hidden redirects to the next 
# route, ultimately resulting in the call to HelloWorld(). But they're not
# actually HTTP redirects. They're more like aliases.
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

# If this file is called directly, i.e., not called as an include, run the code 
# through the Python interpreter.
if __name__ == '__main__':
    # With debug running, the Flask web server will reload itself each time 
    # it notices a code change. It also provides a debugger in the browser.
    app.debug = True

    # Run the local web server with our application.
    # Listen on all public IPs - required because we're running vagrant.
    app.run(host='0.0.0.0', port=5000)
