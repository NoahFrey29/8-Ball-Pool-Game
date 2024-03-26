import phylib;
import os;
import sqlite3;
import math;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        str = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return str;

################################################################################
class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position, velocity, and acceleration
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0);

        # this converst the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

        # add an svg method here
    def svg(self):
        str = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return str;

################################################################################
class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires ball number, position
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HOLE, number, pos, None, None, 0.0, 0.0);

        # this converst the phylib_object into a RollingBall class
        self.__class__ = Hole;

        # add an svg method here
    def svg(self):
        str = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return str

################################################################################
class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y coordinate
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCushion, 0, None, None, None, 0.0, y);

        # this converst the phylib_object into a RollingBall class
        self.__class__ = HCushion;

        # add an svg method here
    def svg(self):
        if self.obj.hcushion.y == 0: # excluding ball colours
            str = """ <rect width="%d" height="%d" x="%d" y="%d" fill="darkgreen" />\n""" % (1400, 25, -25, -25) 
        else:
            str = """ <rect width="%d" height="%d" x="%d" y="%d" fill="darkgreen" />\n""" % (1400, 25, -25, 2700)
        return str

################################################################################
class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x coordinate
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCushion, 0, None, None, None, x, 0.0);

        # this converst the phylib_object into a RollingBall class
        self.__class__ = VCushion;

        # add an svg method here
    def svg(self):
        if self.obj.vcushion.x == 0:
            str = """ <rect width="%d" height="%d" x="%d" y="%d" fill="darkgreen" />\n""" % (25, 2750, -25, -25)
        else:
            str = """ <rect width="%d" height="%d" x="%d" y="%d" fill="darkgreen" />\n""" % (25, 2750, 1350, -25)
        return str

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        str = HEADER

        for object in self:
            if object is not None:
                str += object.svg()
        str+= FOOTER

        return str

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                                    Coordinate(0,0),
                                                    Coordinate(0,0),
                                                    Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                                    Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def findCueBall(self):
        for ball in self:
            if isinstance(ball, StillBall): 
                if ball.obj.still_ball.number == 0:
                    return ball
        return None
        

################################################################################
# something goes into this
class Database():

    def __init__( self, reset=False ):
        if reset == True:
            if os.path.exists( 'phylib.db' ): 
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect( 'phylib.db' ); #connect the database
    
    def close( self ):
        if(self.conn): #close and commit
            self.conn.commit();
            self.conn.close();
            

    def pp( listoftuples ): #pp function from lab 3
        if len(listoftuples)==0:
            print( repr( listoftuples ) );
            return;
        columns = len(listoftuples[0]);
        widths = [ max( [ len(str(item[col])) for item in listoftuples ] ) \
                                    for col in range( columns ) ];
        fmt = " | ".join( ["%%-%ds"%width for width in widths] );
        for row in listoftuples:
            print( fmt % row );

    def printDB(self): # helper function I made to print specific parts of the database
        self.cur = self.conn.cursor();

        print("BALL:")
        self.cur = self.conn.execute("""SELECT * FROM Ball;""")
        result = self.cur.fetchall();
        print(result)
        print("TTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM TTable;""")
        result = self.cur.fetchall();
        print(result)
        print("BALLTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM BallTable;""")
        result = self.cur.fetchall();
        print(result)

        self.conn.commit();
        self.cur.close();

    def createDB( self ):
        
        self.cur = self.conn.cursor(); # open the cursor

        #Ball
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Ball(
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
            );""")

        #TTable
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS TTable(
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
            );""")

        #BallTable
        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS BallTable (
           BALLID  INTEGER NOT NULL,
           TABLEID INTEGER NOT NULL,
           FOREIGN KEY (BALLID) REFERENCES Ball ON UPDATE CASCADE,
           FOREIGN KEY (TABLEID) REFERENCES TTable );""");

        # cur = conn.execute("""CREATE TABLE IF NOT EXISTS BALLTABLE AS
        #     SELECT * FROM BALL
        #     INNER JOIN TTABLE ON BALL.BALLID = TTABLE.TABLEID;
        #     )""")
        
        #Game
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Game(
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL
            );""")

        #Player
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Player(
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        #Shot
        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Shot(
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY (PLAYERID) REFERENCES Player,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        #TableShot
        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS TableShot (
           TABLEID  INTEGER NOT NULL,
           SHOTID INTEGER NOT NULL,
           FOREIGN KEY (TABLEID) REFERENCES TTable,
           FOREIGN KEY (SHOTID) REFERENCES Shot );""");
        
        # cur = conn.execute("""CREATE TABLE IF NOT EXISTS TABLESHOT AS
        #     SELECT * FROM TTABLE
        #     INNER JOIN SHOT ON TTABLE.TABLEID = SHOT.SHOTID;
        #     )""")

        #self.printDB()
  
        #commit and close the cursor
        self.conn.commit();
        self.cur.close();

    def readTable(self, tableId):
        
        self.cur = self.conn.cursor(); #open the cursor

        tableId += 1 # increment the tableID
        self.cur.execute("SELECT * FROM BallTable WHERE TABLEID = ?", (tableId,))
        fetched = self.cur.fetchone()
        if fetched == None: #check the TABLEID exists
            self.conn.commit();
            self.cur.close();
            #print("fetched is none!")
            return None

        newTable = Table(); # make a new table
        selectedID = tableId

        # cur = conn.execute(f"""SELECT TABLEID FROM BALLTABLE
        #     WHERE TABLEID='{tableId}';""")
        # selectedID = cur.fetchall();
        # selectedID = selectedID[0][0]
        
        # join Ball with BallTable where the tableIDs match
        self.cur.execute("""SELECT Ball.* FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID=?;""", (tableId,))
        fetched = self.cur.fetchall();
        #print(fetched);
        #print(len(fetched))

        # for loop that loops through each tuple in the list
        for i in range(len(fetched)):
            if fetched[i][4] is None and fetched[i][5] is None: #still ball case
                # sets all the info
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = 0
                yVel = 0
                sPos = Coordinate(xPos, yPos) # makes the coordinate, still ball 
                sBall = StillBall(ballNo, sPos)
                newTable += sBall # adds it to the table
            else: #fetched[i][4] > 0 or fetched[i][5] > 0
                # sets all the info
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = fetched[i][4]
                yVel = fetched[i][5]
                rPos = Coordinate(xPos, yPos) # make the position and velocity
                rVel = Coordinate(xVel, yVel)

                # calculate the acceleration like in A2
                rAcc = Coordinate(0.0, 0.0)
                rSpeed = phylib.phylib_length(rVel)

                if (rSpeed > VEL_EPSILON):
                    rAcc.x = ((xVel * -1.0) / rSpeed) * DRAG
                    rAcc.y = ((yVel * -1.0) / rSpeed) * DRAG

                rBall = RollingBall(ballNo, rPos, rVel, rAcc)
                newTable += rBall # add the new rolling ball to the table

        self.cur.execute("""SELECT TIME FROM TTable
                               WHERE TABLEID = ?""", (tableId,))
        time = self.cur.fetchone()
        newTable.time = time[0] # fetch and add the time to the table
        
        self.conn.commit(); # commit and close the cursor
        self.cur.close();
        return newTable
        
    def writeTable(self, table):
        self.cur = self.conn.cursor() # open the cursor
        #print(type(table.time))
        tableId = 0 # this may need to be set to something else
        counter = 1
        xPos = 0
        yPos = 0 # declaring the variables
        xVel = 0
        yVel = 0
        ballID = 0; # this may need to be set to something else too
        ballStr = ""
        ball_data = (None)

        # add the table (and auto increment tableID)
        tableStr = f"""INSERT INTO TTable (TIME)
            VALUES ({table.time});"""
        self.cur = self.conn.execute(tableStr)

        # grab said tableID
        tableStr = f"""SELECT TABLEID FROM TTable
                    WHERE TIME={table.time};"""
        self.cur = self.conn.execute(tableStr)

        getID = self.cur.fetchone();
        #print(len(getID))
        tableId = getID[0]

        # for loop that loops through the table and looks for still and rolling balls to write
        for ball in table:
            #object.type == phylib.PHYLIB_ROLLING_BALL
            if isinstance( ball, RollingBall ):
                # get all the info
                ballNum = ball.obj.rolling_ball.number
                xPos = ball.obj.rolling_ball.pos.x
                #print("xPos for a rolling ball")
                #print(type(xPos))
                yPos = ball.obj.rolling_ball.pos.y
                xVel = ball.obj.rolling_ball.vel.x
                yVel = ball.obj.rolling_ball.vel.y
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);"""
                #{ballNum}, {xPos}, {yPos}, {xVel}, {yVel}

                # insert said info into ball, also auto incrementing
                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);""", (ballNum, xPos, yPos, xVel, yVel))
                #ball_data = (ballNum, xPos, yPos, xVel, yVel, counter)
                #self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    #VALUES (?, ?, ?, ?, ?);""", (ballNum, xPos, yPos, xVel, yVel))
                
                # get the most recent ballID and insert it into ballTable with tableID
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

            elif isinstance( ball, StillBall ):
                # get the info for a still ball
                ballNum = ball.obj.still_ball.number
                xPos = ball.obj.still_ball.pos.x
                #print("xPos for a still ball")
                #print(xPos)
                yPos = ball.obj.still_ball.pos.y
                xVel = 0
                yVel = 0
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);"""
                #{ballNum}, {xPos}, {yPos}, {xVel}, {yVel}

                # insert said info into ball, also auto incrementing
                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);""", (ballNum, xPos, yPos))

                #ball_data = (ballNum, xPos, yPos, xVel, yVel, counter)
                # ballStr = f"""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                #     VALUES ({ballNum}, {xPos}, {yPos}, {xVel}, {yVel});"""
                # self.cur = self.conn.execute(ballStr)
                

                # get the most recent ballID and insert it into ballTable with tableID
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

        # commit and close the cursor
        self.conn.commit();
        self.cur.close();
        tableId = tableId - 1 # decrement tableID
        return tableId

    def getGame( self, gameID ):
        self.cur = self.conn.cursor() # open the cursor
        # get playerID, name, and gameName with a join
        self.cur = self.conn.execute(f"""SELECT Player.PLAYERID, Player.PLAYERNAME, Game.GAMENAME FROM Player
            JOIN Game ON Player.GAMEID = Game.GAMEID
            WHERE Game.GAMEID={gameID};""")
        gameStatus = self.cur.fetchall()
        return gameStatus

    def setGame( self, gameName, player1Name, player2Name ):
        self.cur = self.conn.cursor() # open the cursor

        #insert gamename (and auto increment ID)
        gameStr = f"""INSERT INTO Game (GAMENAME)
            VALUES ({gameName});"""
        self.cur = self.conn.execute(f"""INSERT INTO Game (GAMENAME)
            VALUES (?);""", (gameName,))
        
        # get the ID just inserted
        gameStr = f"""SELECT GAMEID FROM Game
            WHERE GAMENAME={gameName}"""
        self.cur = self.conn.execute("""SELECT GAMEID FROM Game
            WHERE GAMENAME=?""", (gameName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        #playerStr = f"""INSERT INTO Player (GAMEID, PLAYERNAME)
            #VALUES ({gameID}, {player1Name});"""
        #insert in the two player names with correct IDs and auto increment 
        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player1Name,))
        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player2Name,))
        
        self.conn.commit() # commit and close the cursor
        self.cur.close()

    def newShot(self, playerName):
        self.cur = self.conn.cursor() # open the cursor
        # get the gameID based on player name
        self.cur = self.conn.execute("""SELECT GAMEID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        # get the playerID based on player name
        self.cur = self.conn.execute("""SELECT PLAYERID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        playerID = self.cur.fetchone()
        playerID = playerID[0]

        # insert the shot and grab the shotID to return it to shoot function
        self.cur = self.conn.execute("""INSERT INTO Shot (GAMEID, PLAYERID)
            VALUES (?, ?);""", (gameID, playerID,))
        self.cur = self.conn.execute("""SELECT SHOTID FROM Shot
            ORDER BY SHOTID DESC""")
        shotID = self.cur.fetchone()
        shotID = shotID[0]

        self.conn.commit() # commit and close the cursor
        self.cur.close()

        return shotID

    def newTableShot(self, tableID, shotID):
        self.cur = self.conn.cursor() # open the cursor and insert IDs into tableShot
        self.cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
            VALUES (?, ?)""", (tableID, shotID))

        self.conn.commit()
        self.cur.close()

################################################################################
# something goes into this
class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None, table=None):
        database = Database(reset=True)
        database.createDB() # reset the database and make a new one
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID += 1 # increment gameID if only gameID is passed in
            gameStuff = database.getGame(gameID) # call getGame

            # set player names and game name based on lower playerID values
            if gameStuff[0][0] < gameStuff[1][0]:
                self.player1Name = gameStuff[0][1]
                self.player2Name = gameStuff[1][1]
            elif gameStuff[0][0] > gameStuff[1][0]:
                self.player1Name = gameStuff[1][1]
                self.player2Name = gameStuff[0][1]
            self.gameName = gameStuff[0][2]

        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            #set the names immediately when given
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            #database.writeTable(table)

            # call setGame to insert everything into the databases
            database.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("""Everything must be set to None except gameID\n
                OR Only gameID must be set to None""")
    
    def calcTotalFrames(self, beforeTable, afterTable):
        # floor method for calculating frames in shoot
        totalFrames = math.floor((afterTable.time - beforeTable.time)/FRAME_INTERVAL)
        return totalFrames

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        db = Database(reset=False) # open the database and open the cursor
        cur = db.conn.cursor()

        # call new shot
        shotID = db.newShot(playerName)

        # find the cueball
        foundCueBall = table.findCueBall()

        # initialize position and acceleration
        xPos = 0
        yPos = 0
        xAcc = 0
        yAcc = 0
        xPos = foundCueBall.obj.still_ball.pos.x;
        yPos = foundCueBall.obj.still_ball.pos.y;
        
        # change the type and set number to 0
        foundCueBall.type = phylib.PHYLIB_ROLLING_BALL
        foundCueBall.obj.rolling_ball.number = 0

        totaltotalFrames = 0;

        # get the velocity and the speed
        rVel = Coordinate(xvel, yvel)
        rSpeed = phylib.phylib_length(rVel)

        # recalculate acceleration like in A2
        if (rSpeed > VEL_EPSILON):
            xAcc = ((xvel * -1.0) / rSpeed) * DRAG
            yAcc = ((yvel * -1.0) / rSpeed) * DRAG

        # set all the new values
        foundCueBall.obj.rolling_ball.pos.x = xPos;
        foundCueBall.obj.rolling_ball.pos.y = yPos;
        foundCueBall.obj.rolling_ball.vel.x = xvel;
        foundCueBall.obj.rolling_ball.vel.y = yvel;
        
        foundCueBall.obj.rolling_ball.acc.x = xAcc
        foundCueBall.obj.rolling_ball.acc.y = yAcc
       
        # make a before and after table, and a total time
        beforeTable = table
        afterTable = table
        totalTime = 0.0

        tableList = []

        # while loop that breaks if the table after segment is None
        while (True):
            afterTable = afterTable.segment()
            if afterTable is None:
                break;

            # call total frames method
            totalFrames = self.calcTotalFrames(beforeTable, afterTable)
            totaltotalFrames += totalFrames
            print(totalFrames)
            for frameNum in range(totalFrames): # loop over total frames
                rollValue = frameNum*FRAME_INTERVAL # multiply current frame by frame interval
                newTable = beforeTable.roll(rollValue) # call roll on the state before segment
                # set the temporary table time to total time + what roll returns
                newTable.time = totalTime + rollValue
                tableID = db.writeTable(newTable) # write the table
                #db.newTableShot(tableID, shotID)
                cur = db.conn.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
                    VALUES (?, ?)""", (tableID+1, shotID)) # insert into TableShot
                #tableList += newTable
                

            beforeTable = afterTable # reinstate the before table to the new segment location
            totalTime = afterTable.time # set time

        # commit and close the connection
        #db.conn.commit()
        #cur.close()

        return totaltotalFrames;


    def shootWithDB( self, gameName, playerName, table, xvel, yvel ):
        db = Database(reset=False) # open the database and open the cursor
        cur = db.conn.cursor()

        # call new shot
        shotID = db.newShot(playerName)

        # find the cueball
        foundCueBall = table.findCueBall()

        # initialize position and acceleration
        xPos = 0
        yPos = 0
        xAcc = 0
        yAcc = 0
        xPos = foundCueBall.obj.still_ball.pos.x;
        yPos = foundCueBall.obj.still_ball.pos.y;
        
        # change the type and set number to 0
        foundCueBall.type = phylib.PHYLIB_ROLLING_BALL
        foundCueBall.obj.rolling_ball.number = 0

        totaltotalFrames = 0;

        # get the velocity and the speed
        rVel = Coordinate(xvel, yvel)
        rSpeed = phylib.phylib_length(rVel)

        # recalculate acceleration like in A2
        if (rSpeed > VEL_EPSILON):
            xAcc = ((xvel * -1.0) / rSpeed) * DRAG
            yAcc = ((yvel * -1.0) / rSpeed) * DRAG

        # set all the new values
        foundCueBall.obj.rolling_ball.pos.x = xPos;
        foundCueBall.obj.rolling_ball.pos.y = yPos;
        foundCueBall.obj.rolling_ball.vel.x = xvel;
        foundCueBall.obj.rolling_ball.vel.y = yvel;
        
        foundCueBall.obj.rolling_ball.acc.x = xAcc
        foundCueBall.obj.rolling_ball.acc.y = yAcc
    
        # make a before and after table, and a total time
        beforeTable = table
        afterTable = table
        totalTime = 0.0

        tableList = []

        # while loop that breaks if the table after segment is None
        while (True):
            afterTable = afterTable.segment()
            if afterTable is None:
                break;

            # call total frames method
            totalFrames = self.calcTotalFrames(beforeTable, afterTable)
            totaltotalFrames += totalFrames
            #print(totalFrames)
            for frameNum in range(totalFrames): # loop over total frames
                rollValue = frameNum*FRAME_INTERVAL # multiply current frame by frame interval
                newTable = beforeTable.roll(rollValue) # call roll on the state before segment
                # set the temporary table time to total time + what roll returns
                newTable.time = totalTime + rollValue
                tableID = db.writeTable(newTable) # write the table
                #db.newTableShot(tableID, shotID)
                cur = db.conn.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
                    VALUES (?, ?)""", (tableID+1, shotID)) # insert into TableShot
                #tableList += newTable
                

            beforeTable = afterTable # reinstate the before table to the new segment location
            totalTime = afterTable.time # set time
            tableList += afterTable

        # commit and close the connection
        db.conn.commit()
        cur.close()

        return tableList;


        
        
        
 
        
        
