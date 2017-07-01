'''Interface with Web GUI'''

import sys
import time
import httplib
import urllib
import urllib2
import urlparse
from poster.streaminghttp import register_openers

class WebInterface(object):
        def __init__(self, base_url):
                self.base_url = base_url
                # Register the streaming http handlers with urllib2
                register_openers()
                print "establish connection to Web server"
                domain = urlparse.urlparse( base_url ).netloc
                self.connection = httplib.HTTPConnection(domain)
                print "Connection established"

        def get_command( self ):
                print "getting command"
                #connection.putheader("User-Agent","DLNRover") #added from Herb's email
                #connection.putheader("Accept","text/plain") #added from Herb's second email
                self.connection.request('GET', "/scripts/command.php")
                response = self.connection.getresponse()
                command = response.read().strip('\n')
                print "got command", command
                return command

        def set_sensor_data( self,  voltage_as_string, accX_as_string, accY_as_string, distance_as_string, gyro_as_string, camera_heading_as_string):
                values = {'voltage' : voltage_as_string, 'accX' : accX_as_string, 'accY': accY_as_string, 'distance' : distance_as_string, 'gyro' : gyro_as_string, 'cameraHeading' : camera_heading_as_string}
                data = urllib.urlencode(values)
                req = urllib2.Request(self.base_url + '/scripts/upload-sensor-data.php', data)
                response = urllib2.urlopen(req)	 
		
	def get_rover_script( self ):
                print "getting rover script"
                #connection.putheader("User-Agent","DLNRover") #added from Herb's email
                #connection.putheader("Accept","text/plain") #added from Herb's second email
                self.connection.request('GET', "/scripts/upload-rover-script.php")
                response = self.connection.getresponse()
                rover_script = response.read().strip('\n')
                print "got rover_script", rover_script
                return rover_script

        def run(self, nxt,camera_left,camera_right,anaglyph,refresh_interval=1):
                '''Pull commands from web-based interface, send messages to NXT and get camera images'''
                while True:
                        #####  Update Image #####
                        #camera.capture_and_upload_image(captioned =False)
                        camera_left.capture_image(captioned =False)
                        camera_right.capture_image(captioned =False)

                        anaglyph.create()
                        anaglyph.upload()
                        
                        #####  Get Command from Web, send to NXT or handle locally in Python script #####
			command = self.get_command()
			print command
			if ( command == "get_odometry_images" ):
				camera_left.upload_image()
				camera_right.upload_image()
			elif ( command == "run_rover_script" ):
				rover_script = self.get_rover_script()
				nxt.run_rover_script(rover_script)
			else:
				nxt.send_command( command )

                        ##### Get sensor data from NXT and send to Web #####
                        (voltage_as_string , accX_as_string, accY_as_string, distance_as_string, gyro_as_string, camera_heading_as_string) = nxt.get_sensor_data()
                        self.set_sensor_data(voltage_as_string, accX_as_string, accY_as_string, distance_as_string, gyro_as_string, camera_heading_as_string)


                        time.sleep(refresh_interval)

