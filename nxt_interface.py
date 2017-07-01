from RestrictedPython.Guards import safe_builtins
from RestrictedPython import compile_restricted
restricted_globals = dict(__builtins__ = safe_builtins)
import nxt.locator
import dln_rover
import sys
############################################
#     NXT Brick Code
############################################
def exec_safely( source  ):
    code = compile_restricted(source, '<string>', 'exec')
    exec(code) in restricted_globals
    
class NXTCommandError(Exception):
    '''Exception demotes attempt to send invalid command.'''
    pass

class NXTBrick:
    def __init__(self, brickname):
        self.brickname = brickname

    def connect(self):
        '''Connects to NXT brick.'''
        try:
            print("Attempting to connect to brick \"{0}\"...".format(self.brickname))
            # Search for NXT brick on both USB and Bluetooth and connect.
            self.connection = nxt.locator.find_one_brick(name=self.brickname)
            self.brick = self.connection.connect()
            print("Successfully connected to brick.")
        except:
            raw_input("Failed to connect to brick. Press Enter to terminate.")
            raise

    def shutdown(self):
        '''Stops NXT and closes connection.'''
        try:
            self.brick.message_write(0,'stop')
            self.connection.close()
        except:
            raw_input("Failed to close connection to brick. Press Enter to terminate.")
            raise

    def send_command(self,command):
        '''Sends command to NXT brick.'''        
        self.brick.message_write(0,command)

class NxtInterface(object):
    def __init__(self, nxt_name):
        self.nxt_brick = NXTBrick(nxt_name)
        self.nxt_brick.connect()
        # Remind user that client program must be active to receive commands.
        raw_input("Please activate client program on brick, then press Enter.")
	self.robot = dln_rover.Robot(self.nxt_brick)
    
    def run_rover_script( self, rover_script ):
	global robot
	robot = self.robot
	try:
	    #exec_safely( rover_script) not working right now...
	    exec rover_script
	except Exception, err:
	    sys.stderr.write('ERROR:%s\n'%str(err))
	
    def send_command( self, command ):
        try:
            self.nxt_brick.send_command( command )
        except(NXTCommandError): 
            print("Received invalid command.")
        except:
            print("An error occurred. Attempting to retry...")
            #else:
            #print(": ".join((str(i),command)))

    def teardown_brick_connection( self ):
        self.nxt_brick.shutdown()
    
    def get_sensor_data( self ):
        try:
            (inbox, voltage_as_string)= self.nxt_brick.brick.message_read (10, 0, True)
        except:
            voltage_as_string = "Unknown"
        try:
            (inbox, accX_as_string)= self.nxt_brick.brick.message_read (11, 0, True)
        except:
            accX_as_string = "Unknown"
        try:
            (inbox, accY_as_string)= self.nxt_brick.brick.message_read (12, 0, True)
        except:
            accY_as_string = "Unknown"
        try:
            (inbox, distance_as_string) = self.nxt_brick.brick.message_read (14, 0, True)
        except:
            distance_as_string = "Unknown"
        
        try:
            (inbox, gyro_as_string)= self.nxt_brick.brick.message_read (15, 0, True)   
        except:
            gyro_as_string = "Unknown"
            
        try:
            (inbox, camera_heading_as_string) = self.nxt_brick.brick.message_read (16, 0, True)
        except:
            camera_heading_as_string = "Unknown"

        return (voltage_as_string , accX_as_string, accY_as_string, distance_as_string, gyro_as_string, camera_heading_as_string)

