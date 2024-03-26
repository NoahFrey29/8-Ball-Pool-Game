import Physics
import phylib

import cgi
import sys
import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl;

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    # def handle_velocity_data():
    #     data = request.json
    #     x_velocity = data['xVelocity']
    #     y_velocity = data['yVelocity']

    #     # Process the velocity data as needed
    #     # For example, you can perform calculations, store it in a database, etc.

    #     # Return a response (optional)
    #     return jsonify({'message': 'Velocity data received successfully'})

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/part1.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            try: # open shoot.html and write data to HTML
                with open('part1.html', 'r') as fp:
                    content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
            except FileNotFoundError:
                # send 404 errors
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Error 404!!! File: %s not found\n404" % self.path, "utf-8"))

            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'): 
            file_path = parsed.path.lstrip("/")

            fp = open( '.'+self.path );
            content = fp.read();

            try:
                split_table = parsed.path.split('-')
                table_number = split_table[1].split('.')[0]
                file_path = f'table-{table_number}.svg'

                if os.path.exists(file_path):
                    fp = open( '.'+self.path );
                    content = fp.read();
                    self.send_response(200)
                    self.send_header('Content-type', 'image/svg+xml')
                    self.send_header("Content-length", len(content))
                    self.end_headers();
                    self.wfile.write(bytes(content, 'utf-8'))
                    fp.close();
            except FileNotFoundError:
                # generate 404 for GET requests that aren't the table.svg files above
                self.send_response(404) # NOT OK
                self.end_headers()
                self.wfile.write(bytes("ERROR 404. File: %s not found\n404" % self.path, "utf-8"))

        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/part1.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                    )

            #for (i = 0; i < MAX_OBJECTS; i+=1):
                #pass;

            #Delete all table-?.svg files
            serv_dir = './'
            for filename in os.listdir(serv_dir):
                if filename.startswith('table-') and filename.endswith('.svg'):
                    file_path = os.path.join(serv_dir, filename)
                    os.remove(file_path) # delete the file

            velocityX = form.getvalue('velocityX')
            velocityY = form.getvalue('velocityY')
            gameName = form.getvalue('gameName');
            player1Name = form.getvalue('player1Name')
            player2Name = form.getvalue('player2Name')
            # Do something with the received data
            print("Received velX:", velocityX)
            print("Received velY:", velocityY)
            print("Received gameName:", gameName)
            print("Received player1Name:", player1Name)
            print("Received player2Name:", player2Name)

            # computing the acceleration in python
            # stillX = float(form['sb_x'].value)
            # stillY = float(form['sb_y'].value)
            # stillPos = Physics.Coordinate(stillX, stillY)
            # sb = Physics.StillBall(int(form['sb_number'].value), stillPos) # int(form['sb_number'].value)

            # rollingX = float(form['rb_x'].value)
            # rollingY = float(form['rb_y'].value)
            # rollingPos = Physics.Coordinate(rollingX, rollingY)
            # rollingVelX = float(form['rb_dx'].value)
            # rollingVelY = float(form['rb_dy'].value)
            # rollingVel = Physics.Coordinate(float(form['rb_dx'].value), float(form['rb_dy'].value))
            # rollingAcc = Physics.Coordinate(0.0, 0.0)
            # rollingSpeed = phylib.phylib_length(rollingVel)

            #manualSpeed = sqrt((rollingVelX*rollingVelX)+(rollingVelY+rollingVelY))

            # rb = Physics.RollingBall(int(form['rb_number'].value), rollingPos, rollingVel, rollingAcc)

            # if (rollingSpeed > Physics.VEL_EPSILON):
            #     rollingAcc.x = ((rollingVel.x * -1.0) / rollingSpeed) * Physics.DRAG
            #     rollingAcc.y = ((rollingVel.y * -1.0) / rollingSpeed) * Physics.DRAG

            # #create the table and put the balls on the table
            # table = Physics.Table()
            # table += sb
            # table += rb

            #while loop similar to A2test2 that writes all svgs to the files and calling segment
            # i = 0
            # while table is not None:
            #     with open(f"table-{i}.svg", "w") as fp:
            #         fp.write(table.svg())
            #     table = table.segment()
            #     i += 1

            # # making an html string
            # htmlString = "<html><head><title>Ball Positions and Velocities</title></head><body>"
            # htmlString += "<h1>Original Ball Positions and Velocities</h1>"

            # #add each ball
            # htmlString += "<ul>"
            # htmlString += f"<li>Still Ball: Position = ({stillX}, {stillY}), Number = {int(form['sb_number'].value)}</li>"
            # htmlString += f"<li>Rolling Ball: Position = ({rollingX}, {rollingY}), Velocity = ({float(form['rb_dx'].value)}, {float(form['rb_dy'].value)}), Number = {int(form['rb_number'].value)}</li>"
            # htmlString += "</ul>"

            # #adding <img> tags for each SVG file
            # i = 0
            # while os.path.exists(f"table-{i}.svg"):
            #     htmlString += f"<img src='table-{i}.svg' alt='Table {i}'><br>"
            #     i += 1

            # #adding a back link
            # htmlString += '<a href="/shoot.html">Back</a>'

            # #end of string
            # htmlString += "</body></html>"

            htmlString = ""

            # writing out with text html content type
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(htmlString, "utf-8"))

            # open file for binary write
            #fp = open( 'table-?.svg', 'wb' );
            # read the file that came in the form and write it to local dir
            #fp.write( form['table'].file.read() );
            #fp.close();

            # read the HTML file and insert the form data
            #fp = open( '.'+parsed.path );
            #content = fp.read() % form;

            # generate the headers
            #self.send_response( 200 ); # OK
            #self.send_header( "Content-type", "image/svg+xml" ); #changed content type
            #self.send_header( "Content-length", len( content ) );
            #self.end_headers();

            # send it to the browser
            #self.wfile.write( bytes( content, "utf-8" ) );
            #fp.close();
        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler);
    print("Server listing in port:  ", int(sys.argv[1]));
    #app.run(debug=True)
    #possibly call the database and set it up here
    httpd.serve_forever();
